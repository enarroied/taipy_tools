from taipy_utils import taipy_callback

from algorithms.uuid_functions import get_uuid


@taipy_callback
def select_uuid(state):
    state.selected_uuid = get_uuid(state.uuid_type, state.name_for_uuid)


@taipy_callback
def change_name_select(state):
    with state as s:
        if s.uuid_type in ("3", "5"):
            s.select_name = True
        else:
            s.select_name = False
            s.name_for_uuid = ""
