import pytest

from source.config import Config

from json import JSONDecodeError


def test_init_config_no_file():
    with pytest.raises(FileNotFoundError):
        cfg = Config("test_files/no_file.json")


def test_init_config_no_json():
    with pytest.raises(JSONDecodeError):
        cfg1 = Config("test_files/file.txt")


def test_init_incorrect_json():
    with pytest.raises(JSONDecodeError):
        cfg1 = Config("test_files/incorrect.json")
