from pages import *

from taipy.gui import Gui
from taipy.gui import builder as tgb

tool_pages = {"/": root, "uuid_generator": uuid_page}

if __name__ == "__main__":

    # uuid page:
    uuid_type = "1"
    selected_uuid = ""
    name_for_uuid = ""
    select_name = False

    gui = Gui(pages=tool_pages)
    gui.run(title="Taipy 🛠️ Tools", dark_mode=False, use_reloader=True)
