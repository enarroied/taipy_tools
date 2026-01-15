from dataclasses import asdict

from algorithms.qr_code_functions import generate_qr_code
from context.qrcodeconfig import QRCodeConfig
from taipy_utilities.taipy_callback import taipy_callback


def state_to_qr_config(state) -> QRCodeConfig:
    """Convert flat state variables to QRCodeConfig dataclass"""
    return QRCodeConfig(
        message=state.qr_code_input,
        add_logo=state.add_logo,
        dark_color=state.dark_color,
        light_color=state.light_color,
        transparent_background=state.transparent_background,
        scale=state.qr_scale,
        border=state.qr_border,
    )


@taipy_callback
def make_qr_code(s):
    config = state_to_qr_config(s)
    s.image_path = generate_qr_code(**asdict(config))
