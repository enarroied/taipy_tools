from dataclasses import dataclass


@dataclass
class QRCodeConfig:
    message: str = ""
    add_logo: bool = False
    dark_color: str = "black"
    light_color: str = "white"
    transparent_background: bool = False
    scale: int = 8
    border: int = 4
    file_output_name: str = "qr_code.png"
