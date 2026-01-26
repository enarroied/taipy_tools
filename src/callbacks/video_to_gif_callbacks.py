import uuid_utils as uuid
from taipy.gui import notify
from taipy_utils import hold_control_during_execution, taipy_callback

from algorithms.video_to_gif_functions import select_video, video_to_gif


def _delete_file(content_path):
    if content_path.is_file():
        content_path.unlink()


def _clean_video_to_gif_parameters(state):
    with state as s:
        s.video_duration = 0
        _delete_file(s.content_path)
        s.content_path = ""
        s.content = ""
        s.video_is_selected = False
        s.file_size = " - "  # For display as None but as string
        s.file_name = " - "


@taipy_callback
def select_video_callback(state):
    with state as s:
        s.content_path, s.video_duration, s.file_size, s.file_name = select_video(
            content=s.content
        )
        s.gif_is_ready = False
        s.video_is_selected = True


@hold_control_during_execution(message="Generating GIF")
@taipy_callback
def convert_to_gif_callback(state):
    with state as s:
        file_output_name = f"./deposit_files/{uuid.uuid4()}.gif"

        try:
            video_to_gif(
                input_path=s.content,
                output_path=file_output_name,
                start_time=s.start_time,
                duration=s.duration,
                fps=int(s.fps),
                resize_factor=s.resize_factor,
            )
            _assert_gif_ready(s, file_output_name)
        except ValueError as e:
            notify(s, "e", str(e))
        finally:
            _clean_video_to_gif_parameters(state)


def _assert_gif_ready(state, file_output_name):
    with state as s:
        s.gif_is_ready = True
        s.content_download = file_output_name
        notify(s, "s", "GIF Generated Successfully!")
