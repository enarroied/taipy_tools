from pathlib import Path
from typing import Optional, Tuple

import uuid_utils as uuid
from algorithms.video_to_gif_functions import get_clip_duration, video_to_gif

import taipy.gui.builder as tgb
from taipy.gui import notify


def _delete_file(content_path):
    if content_path.is_file():
        content_path.unlink()


def _calculate_file_size(content_path):
    if content_path.is_file():
        size_bytes = content_path.stat().st_size
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{size_bytes / (1024 ** 3):.2f} GB"
    else:
        return " - "  # For display as None but as string


def _clean_parameters(state):
    with state as s:
        s.video_duration = 0
        _delete_file(s.content_path)
        s.content_path = None
        s.content = None
        s.video_is_selected = False
        s.file_size = " - "  # For display as None but as string
        s.file_name = " - "


def video_is_too_long(state, video_duration):
    if video_duration > 60:
        with state as s:
            _clean_parameters(s)
            notify(
                s, "error", f"Video Should not exceed 60s, duration is {video_duration}"
            )
        return True


def select_video(state):
    with state as s:
        s.content_path = Path(s.content)
        s.gif_is_ready = False
        s.video_duration = get_clip_duration(s.content)
        if video_is_too_long(s, s.video_duration):
            return
        s.file_size = _calculate_file_size(s.content_path)
        s.video_is_selected = True
        s.file_name = s.content_path.name


def _check_and_notify(state, condition, message):
    if condition:
        notify(state, "e", message)
        return True
    return False


def _parameters_are_wrong(state):
    with state as s:
        return (
            _check_and_notify(
                s,
                s.duration > s.video_duration,
                "Duration shouldn't be longer than total file duration",
            )
            or _check_and_notify(
                s,
                s.start_time > s.video_duration,
                "Start Time shouldn't be after video ends!",
            )
            or _check_and_notify(
                s,
                s.duration + s.start_time > s.video_duration,
                "Duration + Start Time can't be longer than total file duration",
            )
        )


def _assert_gif_ready(state, file_output_name):
    with state as s:
        s.gif_is_ready = True
        s.content_download = file_output_name
        notify(s, "s", "GIF Generated Successfully!")


def convert_to_gif(state):
    with state as s:
        if _parameters_are_wrong(s):
            return
        file_output_name = f"./deposit_files/{uuid.uuid4()}.gif"
        if video_to_gif(
            input_path=s.content,
            output_path=file_output_name,
            start_time=s.start_time,
            duration=s.duration,
            fps=int(s.fps),
            resize_factor=s.resize_factor,
        ):
            _assert_gif_ready(s, file_output_name)


with tgb.Page() as video_gif_page:
    tgb.text("## Video to Gif Converter", mode="md")
    tgb.html("hr")

    with tgb.part():
        tgb.text("### Upload Video:", mode="md")
        tgb.file_selector(
            "{content}",
            label="Select Video",
            on_action=select_video,
            extensions=".mp4,.avi",
            drop_message="Drop Message",
            class_name="fullwidth",
        )
        with tgb.layout("1 1 1"):
            tgb.text("#### Total duration of: {video_duration} s:", mode="md")
            tgb.text(
                "#### Size: {file_size}",
                mode="md",
            )
            tgb.text(
                "#### Video File Name: {file_name}",
                mode="md",
            )

    with tgb.part(render="{video_is_selected}"):
        tgb.text("### Select Parameters:", mode="md")
        with tgb.layout("1 1 1 1"):
            tgb.number("{start_time}", label="Start time", min=0, max=60)
            tgb.number("{duration}", label="Clip Duration", min=1, max=60)
            tgb.number("{resize_factor}", min=0.1, max=1.0, step=0.1)
            with tgb.layout("1 1"):
                tgb.text("#### FPS: ", mode="md")
                tgb.slider("{fps}", lov=[5, 7, 10, 15, 20, 25, 30, 35])
        tgb.button(
            label="Convert to GIF!",
            on_action=convert_to_gif,
            class_name="fullwidth",
        )

    with tgb.part(render="{gif_is_ready}"):
        tgb.text("### Convert to GIF:", mode="md")
        tgb.file_download(
            "{content_download}",
            active="{gif_is_ready}",
            class_name="fullwidth",
        )
