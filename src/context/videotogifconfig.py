from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoToGifConfig:
    input_path: str
    output_path: Optional[str] = None
    output_dir: str = "./deposit_files"
    start_time: float = 0
    duration: Optional[float] = None
    fps: int = 10
    resize_factor: float = 1.0
