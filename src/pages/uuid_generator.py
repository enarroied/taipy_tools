import taipy.gui.builder as tgb

from callbacks.uuid_callbacks import (
    change_name_select,
    select_uuid,
)

with tgb.Page() as uuid_page:
    tgb.text("## **UUID** Generator", mode="md")

    with tgb.layout("1 1 1"):
        tgb.toggle(
            "{uuid_type}",
            lov=["1", "3", "4", "5", "6", "7"],
            on_change=change_name_select,
        )
        tgb.input("{name_for_uuid}", label="Name for UUID", active="{select_name}")
        tgb.button(label="Get UUID!", on_action=select_uuid, class_name="plain")

    tgb.text("## {selected_uuid}", mode="md")
