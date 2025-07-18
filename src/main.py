from pages import *

from taipy.gui import Gui
from taipy.gui import builder as tgb

tool_pages = {
    "/": root,
    "uuid_generator": uuid_page,
    "video_to_gif": video_gif_page,
    "QR_code_generator": qr_code_page,
}

stylekit = {"color_primary": "#1e3a8a", "color_secondary": "#a8dadc"}

if __name__ == "__main__":

    # uuid page:
    uuid_type = "1"
    selected_uuid = ""
    name_for_uuid = ""
    select_name = False

    # Video to Gif
    content = None
    content_path = None
    file_size = " - "  # For Display, this is "None"
    file_name = " - "
    video_is_selected = False
    start_time = 0
    duration = 1
    fps = 5
    resize_factor = 1.0
    video_duration = 0
    gif_is_ready = False
    content_download = None

    # QR Code page
    qr_code_input = ""
    transparent_background = False
    dark_color = "black"
    light_color = "white"
    add_logo = True
    qr_scale = 8
    qr_border = 4
    image_path = None

    gui = Gui(pages=tool_pages, css_file="./css/main.css")
    gui.run(
        title="Taipy 🛠️ Tools",
        favicon="./img/logo.png",
        dark_mode=False,
        stylekit=stylekit,
        use_reloader=True,
    )
