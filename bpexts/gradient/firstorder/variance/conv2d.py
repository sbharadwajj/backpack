import torch.nn
from ...backpropextension import BackpropExtension
from ...gradient.conv2d import GradConv2d
from ...extensions import VARIANCE
from ..sumgradsquared.conv2d import SGSConv2d
from .base import variance_from


class VarianceConv2d(BackpropExtension):

    def __init__(self):
        super().__init__(
            torch.nn.Conv2d, VARIANCE,
            req_inputs=[0], req_output=True
        )

    def apply(self, module, grad_input, grad_output):
        N = grad_output[0].shape[0]
        if module.bias is not None and module.bias.requires_grad:
            module.bias.variance = self.bias(module, grad_output, N)
        if module.weight.requires_grad:
            module.weight.variance = self.weight(module, grad_output, N)

    def bias(self, module, grad_output, N):
        return variance_from(
            GradConv2d().bias_grad(module, grad_output),
            SGSConv2d().bias_sum_grad_squared(module, grad_output),
            N
        )

    def weight(self, module, grad_output, N):
        return variance_from(
            GradConv2d().weight_grad(module, grad_output),
            SGSConv2d().weight_sum_grad_squared(module, grad_output),
            N
        )


EXTENSIONS = [VarianceConv2d()]
