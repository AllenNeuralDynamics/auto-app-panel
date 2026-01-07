from pathlib import Path

import pytest

from auto_app_panel.detector import detect_arg_parser_type


def test_detect_pydantic_settings():
    example_file = Path(__file__).parent / "resources" / "pydantic_settings_example.py"
    parser_type = detect_arg_parser_type(str(example_file))
    assert parser_type == "pydantic_settings"


def test_detect_argparse():
    example_file = Path(__file__).parent / "resources" / "argparse_example.py"
    parser_type = detect_arg_parser_type(str(example_file))
    assert parser_type == "argparse"


def test_detect_no_parser():
    example_file = Path(__file__).parent / "resources" / "no_parser.py"
    with pytest.raises(ValueError, match="No supported argument parsing found"):
        detect_arg_parser_type(str(example_file))
