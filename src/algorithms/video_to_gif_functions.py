import tempfile
from pathlib import Path

import ffmpeg


def select_video(content: str):
    """Handles video selection and retrieves its properties."""
    content_path = Path(content)
    video_duration = get_clip_duration(content)
    file_size = _calculate_file_size(content_path)
    file_name = content_path.name
    return content_path, video_duration, file_size, file_name


def _calculate_file_size(content_path):
    """Calculates the size of the file in a human-readable format."""
    if not content_path.is_file():
        return " - "

    size_bytes = content_path.stat().st_size

    for factor, suffix in [(1024**3, "GB"), (1024**2, "MB"), (1024, "KB")]:
        if size_bytes >= factor:
            return f"{size_bytes / factor:.2f} {suffix}"

    return f"{size_bytes} B"


def get_clip_duration(input_path: str) -> float:
    """Gets the duration of a video file using ffprobe"""
    try:
        return _get_clip_duration(input_path)
    except ffmpeg.Error as e:
        raise ValueError(
            f"ffprobe error: Could not get duration for '{input_path}'.\
                  {e.stderr.decode('utf8')}"
        ) from e
    except (FileNotFoundError, KeyError) as e:
        raise ValueError(
            f"Could not get duration. Is '{input_path}' a valid video file?"
        ) from e


def _get_clip_duration(input_path: str) -> float:
    probe = ffmpeg.probe(input_path)
    duration = float(probe["format"]["duration"])
    print(f"Video duration: {duration:.2f} seconds")
    return duration


def video_to_gif(
    input_path: str,
    output_path: str,
    start_time: float = 0,
    duration: float = None,
    fps: int = 10,
    resize_factor: float = 1.0,
) -> bool:
    try:
        _video_to_gif(
            input_path,
            output_path,
            start_time,
            duration,
            fps,
            resize_factor,
        )
        print(f"GIF created successfully: '{output_path}'")
        return True
    except ffmpeg.Error as e:
        raise ValueError(f"Error converting video to GIF: {e.stderr.decode('utf8')}")
    except Exception as e:
        raise ValueError(f"Error converting video to GIF: {str(e)}")


def _video_to_gif(
    input_path: str,
    output_path: str,
    start_time: float = 0,
    duration: float = None,
    fps: int = 10,
    resize_factor: float = 1.0,
):
    _validate_input_file(input_path)
    clip_info = _get_clip_info(input_path)
    _log_results(input_path, clip_info, fps)
    palette_path = _generate_palette(input_path, start_time, duration, resize_factor)
    _create_gif(
        input_path,
        output_path,
        start_time,
        duration,
        fps,
        resize_factor,
        palette_path,
    )
    _cleanup_file(palette_path)


def _validate_input_file(input_path: str):
    input_file = Path(input_path)
    if not input_file.is_file():
        raise FileNotFoundError(f"Input file '{input_path}' not found.")


def _create_dir_if_not_exist(output_path: str):
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)


def _get_clip_info(input_path: str):
    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe["format"]["duration"])
        width = int(probe["streams"][0]["width"])
        height = int(probe["streams"][0]["height"])
        return {"duration": duration, "size": (width, height)}
    except ffmpeg.Error as e:
        raise ValueError(
            f"ffprobe error: Could not get info for '{input_path}'.\
                  {e.stderr.decode('utf8')}"
        )
    except (FileNotFoundError, KeyError) as e:
        raise ValueError(f"Could not get video info. Is '{input_path}' valid?") from e


def _log_results(input_path: str, clip_info: dict, fps: int):
    print(f"Converting '{input_path}' to GIF...")
    print(f"Duration: {clip_info['duration']:.2f} seconds")
    print(f"Size: {clip_info['size']}")
    print(f"FPS: {fps}")


def _generate_palette(
    input_path: str, start_time: float, duration: float, resize_factor: float
) -> Path:
    input_stream = ffmpeg.input(input_path, ss=start_time)
    scaled_stream = input_stream.filter(
        "scale",
        f"iw*{resize_factor}",
        f"ih*{resize_factor}",
        flags="lanczos",
    )
    if duration:
        scaled_stream = scaled_stream.filter("trim", duration=duration)
    palette_stream = scaled_stream.filter(
        "palettegen",
        max_colors=256,
        reserve_transparent=0,
        stats_mode="full",
    )
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_palette:
        palette_path = Path(temp_palette.name)
    ffmpeg.run(
        ffmpeg.output(palette_stream, str(palette_path)),
        overwrite_output=True,
        quiet=True,
    )
    return palette_path


def _create_gif(
    input_path: str,
    output_path: str,
    start_time: float,
    duration: float,
    fps: int,
    resize_factor: float,
    palette_path: Path,
):
    video_stream = ffmpeg.input(input_path, ss=start_time)
    video_stream = video_stream.filter(
        "scale", f"iw*{resize_factor}", f"ih*{resize_factor}", flags="lanczos"
    )
    if duration:
        video_stream = video_stream.filter("trim", duration=duration)
    video_stream = video_stream.filter("fps", fps=fps)
    palette_input = ffmpeg.input(str(palette_path))
    gif_stream = ffmpeg.filter(
        [video_stream, palette_input],
        "paletteuse",
        dither="floyd_steinberg",
        diff_mode="rectangle",
        new=1,
    )
    _create_dir_if_not_exist(output_path)
    ffmpeg.run(
        ffmpeg.output(gif_stream, output_path, format="gif"),
        overwrite_output=True,
        quiet=True,
    )


def _cleanup_file(file_path: Path):
    if file_path.exists():
        file_path.unlink()
