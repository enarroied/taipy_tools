import taipy.gui.builder as tgb

import taipy_utilities.builder_extension as tgb_ext
from callbacks.uuid_callbacks import (
    change_name_select,
    select_uuid,
)

with tgb.Page() as uuid_page:
    tgb_ext.mdtext("## **UUID** Generator")

    with tgb.layout("1 1 1"):
        tgb.toggle(
            "{uuid_type}",
            lov=["1", "3", "4", "5", "6", "7"],
            on_change=change_name_select,
        )
        tgb_ext.fullwidth_input(
            "{name_for_uuid}",
            label="Name for UUID",
            active="{select_name}",
        )
        tgb_ext.fullwidth_button(label="Get UUID!", on_action=select_uuid)

    tgb_ext.mdtext("## {selected_uuid}")
