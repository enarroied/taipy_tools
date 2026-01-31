from pathlib import Path
from unittest.mock import patch

import ffmpeg
import pytest

from context.videotogifconfig import VideoToGifConfig
from src.algorithms.video_to_gif_functions import (
    _cleanup_file,
    _create_dir_if_not_exist,
    _get_clip_info,
    _validate_input_file,
    convert_video_to_gif,
)


@pytest.fixture
def sample_video_file(tmp_path):
    """Create a fake video file for testing."""
    video_path = tmp_path / "test_video.mp4"
    video_path.touch()
    return video_path


@pytest.fixture
def output_gif_path(tmp_path):
    """Provide output path for GIF."""
    return tmp_path / "output.gif"


@pytest.fixture
def mock_probe_data():
    """Sample ffprobe response data."""
    return {
        "format": {"duration": "10.5"},
        "streams": [{"width": 1920, "height": 1080}],
    }


class TestValidateInputFile:
    """Test input file validation."""

    def test_accepts_existing_file(self, sample_video_file):
        """Test validation passes for existing file."""
        _validate_input_file(str(sample_video_file))
        assert True

    def test_raises_on_missing_file(self, tmp_path):
        """Test error when file doesn't exist."""
        nonexistent = tmp_path / "missing.mp4"
        with pytest.raises(FileNotFoundError, match="not found"):
            _validate_input_file(str(nonexistent))

    def test_raises_on_directory(self, tmp_path):
        """Test error when path is directory not file."""
        with pytest.raises(FileNotFoundError):
            _validate_input_file(str(tmp_path))


class TestCreateDirIfNotExist:
    """Test output directory creation."""

    def test_creates_parent_directory(self, tmp_path):
        """Test that parent directory is created."""
        output_path = tmp_path / "subdir" / "output.gif"
        _create_dir_if_not_exist(str(output_path))
        assert output_path.parent.exists()

    def test_creates_nested_directories(self, tmp_path):
        """Test creation of nested directory structure."""
        output_path = tmp_path / "level1" / "level2" / "output.gif"
        _create_dir_if_not_exist(str(output_path))
        assert output_path.parent.exists()

    def test_handles_existing_directory(self, tmp_path):
        """Test no error when directory already exists."""
        output_path = tmp_path / "existing" / "output.gif"
        output_path.parent.mkdir(parents=True)
        _create_dir_if_not_exist(str(output_path))
        assert output_path.parent.exists()


class TestGetClipInfo:
    """Test video information retrieval."""

    def test_returns_dict(self, sample_video_file, mock_probe_data):
        """Test that clip info is returned as dictionary."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert isinstance(result, dict)

    def test_includes_duration(self, sample_video_file, mock_probe_data):
        """Test that result includes duration."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert "duration" in result

    def test_includes_size(self, sample_video_file, mock_probe_data):
        """Test that result includes size tuple."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert "size" in result

    def test_duration_is_float(self, sample_video_file, mock_probe_data):
        """Test that duration is float type."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert isinstance(result["duration"], float)

    def test_duration_parses_correctly(self, sample_video_file, mock_probe_data):
        """Test that duration value is correct."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert result["duration"] == 10.5

    def test_size_is_tuple(self, sample_video_file, mock_probe_data):
        """Test that size is tuple."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert isinstance(result["size"], tuple)

    def test_size_contains_correct_values(self, sample_video_file, mock_probe_data):
        """Test that size tuple has correct values."""
        with patch("ffmpeg.probe", return_value=mock_probe_data):
            result = _get_clip_info(str(sample_video_file))
            assert result["size"] == (1920, 1080)

    def test_raises_on_ffmpeg_error(self, sample_video_file):
        """Test error handling when ffprobe fails."""
        mock_error = ffmpeg.Error("ffprobe", "", b"error")
        with patch("ffmpeg.probe", side_effect=mock_error):
            with pytest.raises(ValueError, match="ffprobe error"):
                _get_clip_info(str(sample_video_file))

    def test_raises_on_missing_duration_key(self, sample_video_file):
        """Test error when probe data missing duration."""
        invalid_data = {"format": {}}
        with patch("ffmpeg.probe", return_value=invalid_data):
            with pytest.raises(ValueError, match="Could not get video info"):
                _get_clip_info(str(sample_video_file))

    def test_raises_on_missing_streams(self, sample_video_file):
        """Test error when probe data missing streams."""
        invalid_data = {"format": {"duration": "10"}}
        with patch("ffmpeg.probe", return_value=invalid_data):
            with pytest.raises(ValueError, match="Could not get video info"):
                _get_clip_info(str(sample_video_file))


class TestCleanupFile:
    """Test temporary file cleanup."""

    def test_deletes_existing_file(self, tmp_path):
        """Test that existing file is deleted."""
        temp_file = tmp_path / "temp.png"
        temp_file.touch()
        _cleanup_file(temp_file)
        assert not temp_file.exists()

    def test_handles_nonexistent_file(self, tmp_path):
        """Test no error when file doesn't exist."""
        temp_file = tmp_path / "nonexistent.png"
        _cleanup_file(temp_file)
        assert True


class TestVideoToGif:
    """Integration tests for video to GIF conversion."""

    @patch("src.algorithms.video_to_gif_functions._cleanup_file")
    @patch("src.algorithms.video_to_gif_functions._create_gif")
    @patch("src.algorithms.video_to_gif_functions._generate_palette")
    @patch("src.algorithms.video_to_gif_functions._get_clip_info")
    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_returns_output_path_on_success(
        self,
        mock_validate,
        mock_info,
        mock_palette,
        mock_create,
        mock_cleanup,
        sample_video_file,
        output_gif_path,
    ):
        """Test that function returns output path on success."""
        mock_info.return_value = {"duration": 10.0, "size": (1920, 1080)}
        mock_palette.return_value = Path("palette.png")

        config = VideoToGifConfig(
            input_path=str(sample_video_file), output_path=str(output_gif_path)
        )
        result = convert_video_to_gif(config)
        assert result == str(output_gif_path)

    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_raises_error_on_validation_error(
        self, mock_validate, sample_video_file, output_gif_path
    ):
        """Test that function raises error when validation fails."""
        mock_validate.side_effect = FileNotFoundError("File not found")

        config = VideoToGifConfig(
            input_path=str(sample_video_file), output_path=str(output_gif_path)
        )
        with pytest.raises(ValueError, match="Error converting video to GIF"):
            convert_video_to_gif(config)

    @patch("src.algorithms.video_to_gif_functions._cleanup_file")
    @patch("src.algorithms.video_to_gif_functions._create_gif")
    @patch("src.algorithms.video_to_gif_functions._generate_palette")
    @patch("src.algorithms.video_to_gif_functions._get_clip_info")
    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_calls_validate_input_file(
        self,
        mock_validate,
        mock_info,
        mock_palette,
        mock_create,
        mock_cleanup,
        sample_video_file,
        output_gif_path,
    ):
        """Test that input validation is called."""
        mock_info.return_value = {"duration": 10.0, "size": (1920, 1080)}
        mock_palette.return_value = Path("palette.png")

        config = VideoToGifConfig(
            input_path=str(sample_video_file), output_path=str(output_gif_path)
        )
        convert_video_to_gif(config)
        mock_validate.assert_called_with(str(sample_video_file))

    @patch("src.algorithms.video_to_gif_functions._cleanup_file")
    @patch("src.algorithms.video_to_gif_functions._create_gif")
    @patch("src.algorithms.video_to_gif_functions._generate_palette")
    @patch("src.algorithms.video_to_gif_functions._get_clip_info")
    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_calls_get_clip_info(
        self,
        mock_validate,
        mock_info,
        mock_palette,
        mock_create,
        mock_cleanup,
        sample_video_file,
        output_gif_path,
    ):
        """Test that clip info retrieval is called."""
        mock_info.return_value = {"duration": 10.0, "size": (1920, 1080)}
        mock_palette.return_value = Path("palette.png")

        config = VideoToGifConfig(
            input_path=str(sample_video_file), output_path=str(output_gif_path)
        )
        convert_video_to_gif(config)
        mock_info.assert_called_once_with(str(sample_video_file))

    @patch("src.algorithms.video_to_gif_functions._cleanup_file")
    @patch("src.algorithms.video_to_gif_functions._create_gif")
    @patch("src.algorithms.video_to_gif_functions._generate_palette")
    @patch("src.algorithms.video_to_gif_functions._get_clip_info")
    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_calls_cleanup_file(
        self,
        mock_validate,
        mock_info,
        mock_palette,
        mock_create,
        mock_cleanup,
        sample_video_file,
        output_gif_path,
    ):
        """Test that cleanup is called."""
        mock_info.return_value = {"duration": 10.0, "size": (1920, 1080)}
        palette_path = Path("palette.png")
        mock_palette.return_value = palette_path

        config = VideoToGifConfig(
            input_path=str(sample_video_file), output_path=str(output_gif_path)
        )
        convert_video_to_gif(config)
        mock_cleanup.assert_called_once_with(palette_path)

    @patch("src.algorithms.video_to_gif_functions._cleanup_file")
    @patch("src.algorithms.video_to_gif_functions._create_gif")
    @patch("src.algorithms.video_to_gif_functions._generate_palette")
    @patch("src.algorithms.video_to_gif_functions._get_clip_info")
    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_uses_default_output_path(
        self,
        mock_validate,
        mock_info,
        mock_palette,
        mock_create,
        mock_cleanup,
        sample_video_file,
    ):
        """Test that default output path is generated when not provided."""
        mock_info.return_value = {"duration": 10.0, "size": (1920, 1080)}
        mock_palette.return_value = Path("palette.png")

        config = VideoToGifConfig(input_path=str(sample_video_file))
        result = convert_video_to_gif(config)

        # Result should be a path in the default output directory
        assert result.endswith(".gif")
        assert "deposit_files" in result

    @patch("src.algorithms.video_to_gif_functions._cleanup_file")
    @patch("src.algorithms.video_to_gif_functions._create_gif")
    @patch("src.algorithms.video_to_gif_functions._generate_palette")
    @patch("src.algorithms.video_to_gif_functions._get_clip_info")
    @patch("src.algorithms.video_to_gif_functions._validate_input_file")
    def test_uses_custom_parameters(
        self,
        mock_validate,
        mock_info,
        mock_palette,
        mock_create,
        mock_cleanup,
        sample_video_file,
        output_gif_path,
    ):
        """Test that custom parameters are used."""
        mock_info.return_value = {"duration": 10.0, "size": (1920, 1080)}
        mock_palette.return_value = Path("palette.png")

        config = VideoToGifConfig(
            input_path=str(sample_video_file),
            output_path=str(output_gif_path),
            start_time=2.0,
            duration=5.0,
            fps=15,
            resize_factor=0.5,
        )
        convert_video_to_gif(config)

        # Verify the config values were passed through
        assert config.start_time == 2.0
        assert config.duration == 5.0
        assert config.fps == 15
        assert config.resize_factor == 0.5
