import torch
from torch.nn.functional import conv_transpose1d, conv_transpose2d, conv_transpose3d


def unfold_by_conv_transpose(input, module):
    """Return the unfolded input using transpose convolution."""
    N, C_in = input.shape[0], input.shape[1]
    kernel_size = module.kernel_size
    kernel_size_numel = int(torch.prod(torch.Tensor(kernel_size)))

    def make_weight():
        weight = torch.zeros(1, kernel_size_numel, *kernel_size)

        for i in range(kernel_size_numel):
            extraction = torch.zeros(kernel_size_numel)
            extraction[i] = 1.0
            weight[0, i] = extraction.reshape(*kernel_size)

        repeat = [C_in, 1] + [1 for _ in kernel_size]
        weight = weight.repeat(*repeat)
        return weight.to(module.weight.device)

    def get_conv_transpose():
        functional_for_module_cls = {
            torch.nn.ConvTranspose1d: conv_transpose1d,
            torch.nn.ConvTranspose2d: conv_transpose2d,
            torch.nn.ConvTranspose3d: conv_transpose3d,
        }
        return functional_for_module_cls[module.__class__]

    conv_transpose = get_conv_transpose()
    unfold = conv_transpose(
        input,
        make_weight(),
        bias=None,
        stride=module.stride,
        padding=module.padding,
        dilation=module.dilation,
        groups=C_in,
    )

    return unfold.reshape(N, -1, kernel_size_numel)
