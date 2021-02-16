from backpack.core.derivatives.conv_transpose3d import ConvTranspose3DDerivatives
from backpack.extensions.secondorder.diag_hessian.convtransposend import (
    DiagHConvTransposeND,
    BatchDiagHConvTransposeND,
)


class DiagHConvTranspose3d(DiagHConvTransposeND):
    def __init__(self):
        super().__init__(
            derivatives=ConvTranspose3DDerivatives(),
            N=3,
            params=["bias", "weight"],
        )


class BatchDiagHConvTranspose3d(BatchDiagHConvTransposeND):
    def __init__(self):
        super().__init__(
            derivatives=ConvTranspose3DDerivatives(),
            N=3,
            params=["bias", "weight"],
        )
