import taipy.gui.builder as tgb


def empty_callback(state):
    pass


def mdtext(content: str):
    tgb.text(content, mode="md")


def fullwidth_button(label: str, on_action=None):
    tgb.button(label, on_action=on_action, class_name="fullwidth plain")


def fullwidth_input(
    value: str, active: str = "{True}", label: str = "", on_change=None
):
    kwargs = {
        "value": value,
        "active": active,
        "label": label,
        "class_name": "fullwidth",
    }
    # If on_change = None, we get a warning:
    if on_change is not None:
        kwargs["on_change"] = on_change

    tgb.input(**kwargs)
