import taipy.gui.builder as tgb

import taipy_utilities.builder_extension as tgb_ext
from callbacks.qr_code_callbacks import make_qr_code

with tgb.Page() as qr_code_page:
    tgb_ext.mdtext("## Create **QR** Codes")
    with tgb.layout("1 5"):
        tgb_ext.mdtext("### Enter your string:")
        tgb_ext.fullwidth_input("{qr_code_input}")
    with tgb.layout("1 1 1"):
        tgb.toggle("{transparent_background}", label="Transparent Background")
        tgb.toggle("{dark_color}", lov=["black", "blue", "red"], label="Dark Color")
        tgb.toggle(
            "{light_color}", lov=["white", "yellow", "pink"], label="Light Color"
        )
        tgb.toggle("{add_logo}", label="Add Logo")
        with tgb.part():
            tgb_ext.mdtext("**Scale:**")
            tgb.slider("{qr_scale}", min=5, max=10)
        with tgb.part():
            tgb_ext.mdtext("**Border:**")
            tgb.slider("{qr_border}", min=0, max=10)
    tgb_ext.fullwidth_button("Get QR Code!", on_action=make_qr_code)
    with tgb.part(class_name="image-output"):
        tgb.image("{image_path}")
    tgb.file_download(
        "{image_path}",
        label="Download QR Code",
        active="{image_path}",
        class_name="fullwidth",
    )
