from pages import *

from taipy.gui import Gui
from taipy.gui import builder as tgb

tool_pages = {
    "/": root,
    "uuid_generator": uuid_page,
    "video_to_gif": video_gif_page,
}

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

    gui = Gui(pages=tool_pages)
    gui.run(title="Taipy 🛠️ Tools", dark_mode=False, use_reloader=True)
