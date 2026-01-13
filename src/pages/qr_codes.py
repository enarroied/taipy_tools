import taipy.gui.builder as tgb

from callbacks.qr_code_callbacks import make_qr_code

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
