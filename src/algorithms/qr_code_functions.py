from dataclasses import asdict
from pathlib import Path

import segno
from PIL import Image

from context.qrcodeconfig import QRCodeConfig


def generate_qr_code(
    config: QRCodeConfig,
) -> str:
    """
    Generate a QR code image from a message with optional logo and styling.
    Args:
        config (QRCodeConfig): Parameters to create the QR Code
    Returns:
        str: Path to the generated QR code image
    """
    message = config.message
    if len(message) > 1500:
        raise ValueError("Text too long")

    if not message.strip():
        raise ValueError("Message cannot be empty")

    create_qr_code(**asdict(config))
    return config.file_output_name


def create_qr_code(
    message,
    add_logo=None,
    dark_color="black",
    light_color="white",
    transparent_background=False,
    scale=8,
    border=4,
    file_output_name="qr_code.png",
):
    """
    Create a QR code with optional center image and custom styling.

    Args:
        message (str): The text/data to encode in the QR code
        add_logo (bool, optional): If True, adds a logo at the center of the QR code
        dark_color (str, optional): Color for dark areas (default: "black")
        light_color (str, optional): Color for light areas (default: "white")
        transparent_background (bool, optional): If True, background will be transparent
            (default: False)
        scale (int, optional): Scale factor for QR code size (default: 8)
        border (int, optional): Border size around QR code (default: 4)

    Returns:
        str: Path to the generated QR code image
    """

    qr = segno.make(message, error="H")
    center_image_path = "./img/logo.png" if add_logo else None

    if not center_image_path or not Path(center_image_path).exists():
        _save_qr_code(
            qr,
            file_output_name,
            scale,
            border,
            dark_color,
            transparent_background,
            light_color,
        )
        return file_output_name

    temp_path = Path("temp_qr.png")

    try:
        _save_qr_code(
            qr,
            temp_path,
            scale,
            border,
            dark_color,
            transparent_background,
            light_color,
        )

        qr_img = Image.open(temp_path)
        center_img = _prepare_center_image(
            center_image_path,
            qr_img.size,
        )

        final_img = _add_center_image(qr_img, center_img)
        final_img.save(file_output_name)

    finally:
        _cleanup_temp_file(temp_path)
    return file_output_name


def _save_qr_code(
    qr, path, scale, border, dark_color, transparent_background, light_color
):
    """Save QR code to temporary file."""
    background = None if transparent_background else light_color
    qr.save(path, scale=scale, border=border, dark=dark_color, light=background)


def _prepare_center_image(center_image_path, qr_size):
    """Prepare center image with proper sizing, preserving original colors."""
    center_img = Image.open(center_image_path)
    if center_img.mode != "RGBA":
        center_img = center_img.convert("RGBA")
    qr_width, qr_height = qr_size
    center_size = min(qr_width, qr_height) // 5
    return center_img.resize((center_size, center_size), Image.Resampling.LANCZOS)


def _add_center_image(qr_img, center_img):
    """Add center image to QR code."""
    final_img = qr_img.copy()
    center_pos = _calculate_center_position(qr_img.size, center_img.size)
    if final_img.mode != "RGBA":
        final_img = final_img.convert("RGBA")
    final_img.paste(center_img, center_pos, center_img)
    return final_img


def _calculate_center_position(qr_size, center_size):
    """Calculate position to center the image."""
    qr_width, qr_height = qr_size
    center_width, center_height = center_size

    if center_width > qr_width or center_height > qr_height:
        raise ValueError("Center image too large for QR code")

    center_x = _center(qr_width, center_width)
    center_y = _center(qr_height, center_height)

    return (center_x, center_y)


def _center(outer_dimension, inner_dimension):
    return (outer_dimension - inner_dimension) // 2


def _cleanup_temp_file(temp_path):
    """Clean up temporary file."""
    if temp_path.exists():
        temp_path.unlink()
