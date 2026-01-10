import pytest

from src.algorithms.uuid_functions import get_uuid


class TestGetUUID:
    """Test suite for get_uuid function"""

    def test_uuid1_generation(self):
        """Test UUID version 1 generation"""
        result = get_uuid("1")
        assert result is not None

    def test_uuid1_version(self):
        """Test UUID version 1 has correct version"""
        result = get_uuid("1")
        assert result.version == 1

    def test_uuid3_generation(self):
        """Test UUID version 3 generation returns valid UUID"""
        result = get_uuid("3", name="example.com")
        assert result is not None

    def test_uuid3_version(self):
        """Test UUID version 3 has correct version"""
        result = get_uuid("3", name="example.com")
        assert result.version == 3

    def test_uuid3_deterministic(self):
        """Test UUID version 3 is deterministic with same name"""
        name = "example.com"
        result1 = get_uuid("3", name=name)
        result2 = get_uuid("3", name=name)
        assert result1 == result2

    def test_uuid4_generation(self):
        """Test UUID version 4 generation"""
        result = get_uuid("4")
        assert result is not None
        assert result.version == 4

        # UUID4 should be random
        result2 = get_uuid("4")
        assert result != result2

    def test_uuid5_generation(self):
        """Test UUID version 5 generation with name"""
        name = "example.com"
        result = get_uuid("5", name=name)
        assert result is not None
        assert result.version == 5

        # UUID5 should be deterministic
        result2 = get_uuid("5", name=name)
        assert result == result2

    def test_uuid6_generation(self):
        """Test UUID version 6 generation"""
        result = get_uuid("6")
        assert result is not None
        assert result.version == 6

    def test_uuid7_generation(self):
        """Test UUID version 7 generation"""
        result = get_uuid("7")
        assert result is not None
        assert result.version == 7

    def test_invalid_uuid_type(self):
        """Test that invalid UUID type returns ValueError"""
        with pytest.raises(ValueError, match="Unsupported UUID type"):
            get_uuid("99")

    def test_uuid3_different_names(self):
        """Test that different names produce different UUID3s"""
        result1 = get_uuid("3", name="example.com")
        result2 = get_uuid("3", name="different.com")
        assert result1 != result2

    def test_uuid5_different_names(self):
        """Test that different names produce different UUID5s"""
        result1 = get_uuid("5", name="example.com")
        result2 = get_uuid("5", name="different.com")
        assert result1 != result2

    def test_empty_string_type(self):
        """Empty string raises ValueErro"""
        with pytest.raises(ValueError, match="UUID value is empty"):
            get_uuid("")

    def test_uuid_format(self):
        """Test that returned UUIDs have valid format"""
        for uuid_type in ["1", "3", "4", "5", "6", "7"]:
            if uuid_type in ["3", "5"]:
                result = get_uuid(uuid_type, name="test")
            else:
                result = get_uuid(uuid_type)

            if result:
                uuid_str = str(result)
                assert len(uuid_str) == 36
                assert uuid_str.count("-") == 4
