from pathlib import Path

import pytest
from PIL import Image

from src.algorithms.qr_code_functions import (
    _add_center_image,
    _calculate_center_position,
    _cleanup_temp_file,
    _prepare_center_image,
    create_qr_code,
)


@pytest.fixture
def sample_center_image(tmp_path):
    """Create a sample center image for testing."""
    img_path = tmp_path / "center.png"
    img = Image.new("RGBA", (100, 100), color="blue")
    img.save(img_path)
    return img_path


@pytest.fixture
def qr_output_path(tmp_path):
    """Provide a temporary output path for QR codes."""
    return tmp_path / "test_qr.png"


class TestBasicQRCreation:
    """Test basic QR code creation without center image."""

    def test_creates_qr_code_file(self, qr_output_path):
        """Test that QR code file is created."""
        create_qr_code("test data", output_path=str(qr_output_path))
        assert qr_output_path.exists()

    def test_returns_output_path(self, qr_output_path):
        """Test that function returns the output path."""
        result = create_qr_code("test data", output_path=str(qr_output_path))
        assert result == str(qr_output_path)

    def test_creates_valid_image(self, qr_output_path):
        """Test that created file is a valid image."""
        create_qr_code("test data", output_path=str(qr_output_path))
        img = Image.open(qr_output_path)
        assert img is not None

    def test_default_output_path(self):
        """Test QR code creation with default output path."""
        result = create_qr_code("test data")
        try:
            assert Path(result).exists()
        finally:
            Path(result).unlink()


class TestQRWithCenterImage:
    """Test QR code creation with center image."""

    def test_creates_qr_with_center_image(self, qr_output_path, sample_center_image):
        """Test QR code is created with center image."""
        create_qr_code(
            "test data",
            output_path=str(qr_output_path),
            center_image_path=str(sample_center_image),
        )
        assert qr_output_path.exists()

    def test_handles_missing_center_image(self, qr_output_path):
        """Test graceful handling when center image doesn't exist."""
        create_qr_code(
            "test data",
            output_path=str(qr_output_path),
            center_image_path="nonexistent.png",
        )
        assert qr_output_path.exists()

    def test_handles_none_center_image(self, qr_output_path):
        """Test handling when center_image_path is None."""
        create_qr_code(
            "test data",
            output_path=str(qr_output_path),
            center_image_path=None,
        )
        assert qr_output_path.exists()

    def test_temp_file_cleaned_up(self, qr_output_path, sample_center_image):
        """Test temporary file is cleaned up after creation."""
        create_qr_code(
            "test data",
            output_path=str(qr_output_path),
            center_image_path=str(sample_center_image),
        )
        assert not Path("temp_qr.png").exists()


class TestCustomStyling:
    """Test custom color and styling options."""

    def test_custom_dark_color(self, qr_output_path):
        """Test QR code with custom dark color."""
        create_qr_code("test data", output_path=str(qr_output_path), dark_color="red")
        assert qr_output_path.exists()

    def test_custom_light_color(self, qr_output_path):
        """Test QR code with custom light color."""
        create_qr_code(
            "test data",
            output_path=str(qr_output_path),
            light_color="yellow",
        )
        assert qr_output_path.exists()

    def test_transparent_background(self, qr_output_path):
        """Test QR code with transparent background."""
        create_qr_code(
            "test data",
            output_path=str(qr_output_path),
            transparent_background=True,
        )
        assert qr_output_path.exists()

    def test_custom_scale(self, qr_output_path):
        """Test QR code with custom scale."""
        create_qr_code("test data", output_path=str(qr_output_path), scale=10)
        assert qr_output_path.exists()

    def test_custom_border(self, qr_output_path):
        """Test QR code with custom border."""
        create_qr_code("test data", output_path=str(qr_output_path), border=2)
        assert qr_output_path.exists()


class TestCalculateCenterPosition:
    """Test center position calculation."""

    def test_centers_image_correctly(self):
        """Test center position calculation."""
        pos = _calculate_center_position((100, 100), (20, 20))
        assert pos == (40, 40)

    def test_handles_different_sizes(self):
        """Test center position with different sizes."""
        pos = _calculate_center_position((200, 150), (50, 30))
        assert pos == (75, 60)

    def test_returns_tuple(self):
        """Test that function returns a tuple."""
        pos = _calculate_center_position((100, 100), (10, 10))
        assert isinstance(pos, tuple)


class TestPrepareCenterImage:
    """Test center image preparation."""

    def test_converts_to_rgba(self, sample_center_image):
        """Test image is converted to RGBA."""
        result = _prepare_center_image(str(sample_center_image), (500, 500))
        assert result.mode == "RGBA"

    def test_resizes_image(self, sample_center_image):
        """Test image is resized correctly."""
        qr_size = (500, 500)
        result = _prepare_center_image(str(sample_center_image), qr_size)
        expected_size = min(qr_size) // 5
        assert result.size == (expected_size, expected_size)

    def test_returns_image_object(self, sample_center_image):
        """Test function returns PIL Image object."""
        result = _prepare_center_image(str(sample_center_image), (500, 500))
        assert isinstance(result, Image.Image)


class TestAddCenterImage:
    """Test adding center image to QR code."""

    def test_returns_image(self):
        """Test function returns an image."""
        qr_img = Image.new("RGB", (100, 100), color="white")
        center_img = Image.new("RGBA", (20, 20), color="blue")
        result = _add_center_image(qr_img, center_img)
        assert isinstance(result, Image.Image)

    def test_converts_to_rgba(self):
        """Test result is RGBA mode."""
        qr_img = Image.new("RGB", (100, 100), color="white")
        center_img = Image.new("RGBA", (20, 20), color="blue")
        result = _add_center_image(qr_img, center_img)
        assert result.mode == "RGBA"

    def test_preserves_qr_size(self):
        """Test final image has same size as QR code."""
        qr_img = Image.new("RGB", (100, 100), color="white")
        center_img = Image.new("RGBA", (20, 20), color="blue")
        result = _add_center_image(qr_img, center_img)
        assert result.size == qr_img.size


class TestCleanupTempFile:
    """Test temporary file cleanup."""

    def test_deletes_existing_file(self, tmp_path):
        """Test that existing temp file is deleted."""
        temp_file = tmp_path / "temp_test.png"
        temp_file.touch()
        _cleanup_temp_file(temp_file)
        assert not temp_file.exists()

    def test_handles_nonexistent_file(self, tmp_path):
        """Test handling when temp file doesn't exist."""
        temp_file = tmp_path / "nonexistent.png"
        _cleanup_temp_file(temp_file)
        assert True


class TestQRCodeIntegration:
    """Integration tests for complete QR code creation."""

    def test_full_workflow_with_all_options(self, qr_output_path, sample_center_image):
        """Test complete workflow with all options."""
        create_qr_code(
            "https://example.com",
            output_path=str(qr_output_path),
            center_image_path=str(sample_center_image),
            dark_color="blue",
            light_color="lightblue",
            transparent_background=False,
            scale=10,
            border=2,
        )
        assert qr_output_path.exists()

    def test_multiple_qr_codes_created(self, tmp_path):
        """Test creating multiple QR codes in sequence."""
        path1 = tmp_path / "qr1.png"
        path2 = tmp_path / "qr2.png"

        create_qr_code("data1", output_path=str(path1))
        create_qr_code("data2", output_path=str(path2))

        assert path1.exists()

    def test_second_qr_code_created(self, tmp_path):
        """Test that second QR code is also created."""
        path1 = tmp_path / "qr1.png"
        path2 = tmp_path / "qr2.png"

        create_qr_code("data1", output_path=str(path1))
        create_qr_code("data2", output_path=str(path2))

        assert path2.exists()

    def test_overwrites_existing_file(self, qr_output_path):
        """Test that existing file is overwritten."""
        create_qr_code("first", output_path=str(qr_output_path))
        create_qr_code("second data with more content", output_path=str(qr_output_path))
        assert qr_output_path.exists()
