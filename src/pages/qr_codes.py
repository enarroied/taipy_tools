import taipy.gui.builder as tgb

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


with tgb.Page() as qr_code_page:
    tgb.text("## Create **QR** Codes", mode="md")
    with tgb.layout("1 5"):
        tgb.text("### Enter your string:", mode="md")
        tgb.input("{qr_code_input}", class_name="fullwidth")
    with tgb.layout("1 1 1"):
        tgb.toggle("{transparent_background}", label="Transparent Background")
        tgb.toggle("{dark_color}", lov=["black", "blue", "red"], label="Dark Color")
        tgb.toggle(
            "{light_color}", lov=["white", "yellow", "pink"], label="Light Color"
        )
        tgb.toggle("{add_logo}", label="Add Logo")
        with tgb.part():
            tgb.text("**Scale:**", mode="md")
            tgb.slider("{qr_scale}", min=5, max=10)
        with tgb.part():
            tgb.text("**Border:**", mode="md")
            tgb.slider("{qr_border}", min=0, max=10)
    tgb.button("Get QR Code!", on_action=make_qr_code, class_name="fullwidth plain")
    with tgb.part(class_name="image-output"):
        tgb.image("{image_path}")
    tgb.file_download(
        "{image_path}",
        label="Download QR Code",
        active="{image_path}",
        class_name="fullwidth",
    )
