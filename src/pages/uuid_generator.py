from algorithms.uuid_functions import get_uuid

import taipy.gui.builder as tgb


def select_uuid(state):
    state.selected_uuid = get_uuid(state.uuid_type, state.name_for_uuid)


def change_name_select(state):
    with state as s:
        if s.uuid_type in ("3", "5"):
            s.select_name = True
        else:
            s.select_name = False
            s.name_for_uuid = ""


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
