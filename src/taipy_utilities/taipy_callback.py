from functools import wraps

from taipy.gui import notify


def taipy_callback(func):
    """Decorator that translates Python exceptions to Taipy notifications"""

    @wraps(func)
    def wrapper(state):
        with state as s:
            try:
                return func(s)
            except ValueError as e:
                notify(s, "w", str(e))
            except Exception as e:
                notify(s, "e", f"Unexpected error: {str(e)}")
                raise

    return wrapper
