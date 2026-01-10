import ffmpeg


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
