from algorithms.qr_code_functions import generate_qr_code
from taipy_utilities.taipy_callback import taipy_callback


@taipy_callback
def make_qr_code(s):
    s.image_path = generate_qr_code(
        message=s.qr_code_input,
        add_logo=s.add_logo,
        dark_color=s.dark_color,
        light_color=s.light_color,
        transparent_background=s.transparent_background,
        qr_scale=s.qr_scale,
        qr_border=s.qr_border,
    )
