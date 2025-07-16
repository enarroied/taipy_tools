from pathlib import Path
from typing import Optional, Tuple

from moviepy import VideoFileClip, video

# Helper functions


def _clip_file(clip, duration, start_time):
    if duration is not None:
        clip = clip.subclipped(start_time, start_time + duration)
    else:
        clip = clip.subclipped(start_time)
    return clip


def _resize_clip(clip, resize_factor):
    if resize_factor != 1.0:
        return clip.resized(resize_factor)
    return clip


def _process_clip(clip, input_path, duration, start_time, resize_factor, fps):
    clip = _clip_file(clip, duration, start_time)
    clip = _resize_clip(clip, resize_factor)
    _log_results(input_path, clip, fps)
    return clip


def _is_input_file_missing(input_path):
    input_file = Path(input_path)
    if not input_file.is_file():
        print(f"Error: Input file '{input_path}' not found.")
        return True


def _create_dir_if_not_exist(output_path):
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)


def _log_results(input_path, clip, fps):
    print(f"Converting '{input_path}' to GIF...")
    print(f"Duration: {clip.duration:.2f} seconds")
    print(f"Size: {clip.size}")
    print(f"FPS: {fps}")


def get_clip_duration(input_path):
    with VideoFileClip(input_path) as clip:
        print(f"Video duration: {clip.duration:.2f} seconds")
        return clip.duration


def video_to_gif(
    input_path: str,
    output_path: str,
    start_time: float = 0,
    duration: Optional[float] = None,
    fps: int = 10,
    resize_factor: float = 1.0,
) -> bool:
    try:
        if _is_input_file_missing(input_path):
            return False
        _create_dir_if_not_exist(output_path)

        with VideoFileClip(input_path) as clip:
            clip = _process_clip(
                clip, input_path, duration, start_time, resize_factor, fps
            )
            clip.write_gif(output_path, fps=fps)
        print(f"GIF created successfully: '{output_path}'")
        return True

    except Exception as e:
        print(f"Error converting video to GIF: {str(e)}")
        return False
