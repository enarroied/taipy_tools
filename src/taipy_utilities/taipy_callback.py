import inspect
from functools import wraps

from taipy.gui import hold_control, notify, resume_control


def taipy_callback(func):
    """Decorator that translates Python exceptions to Taipy notifications"""

    @wraps(func)
    def wrapper(state, var_name=None, payload=None):
        with state as s:
            try:
                return _call_with_appropriate_args(func, s, var_name, payload)
            except ValueError as e:
                notify(s, "w", str(e))
            except Exception as e:
                notify(s, "e", f"Unexpected error: {str(e)}")
                raise

    return wrapper


def hold_control_during_execution(message: str = "Processing..."):
    """Decorator to hold control before the callback execution
    and resume it afterwards."""

    def decorator(func):
        @wraps(func)
        def wrapper(state, var_name=None, payload=None):
            hold_control(state, message=message)
            try:
                return _call_with_appropriate_args(func, state, var_name, payload)
            finally:
                resume_control(state)

        return wrapper

    return decorator


def _call_with_appropriate_args(func, state, var_name=None, payload=None):
    """Utility to call a function with the correct number of arguments"""
    sig = inspect.signature(func)
    num_params = len(sig.parameters)

    if num_params == 1:
        return func(state)
    elif num_params == 2:
        return func(state, var_name)
    else:
        return func(state, var_name, payload)
