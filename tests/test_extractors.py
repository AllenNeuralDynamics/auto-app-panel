import pathlib

import pytest

from auto_app_panel.extractors import ArgparseExtractor, PydanticSettingsExtractor
from auto_app_panel.types import Parameter


def test_argparse_extractor():
    extractor = ArgparseExtractor()
    example_path = pathlib.Path(__file__).parent / "resources" / "argparse_example.py"
    parameters = extractor.extract_parameters(str(example_path))

    assert len(parameters) == 12

    override_date = next(p for p in parameters if p.name == "override_date")
    assert override_date.type == "string"
    assert override_date.description

    intervals_table = next(p for p in parameters if p.name == "intervals_table")
    assert intervals_table.type == "string"
    assert intervals_table.default_value == "trials"

    pre = next(p for p in parameters if p.name == "pre")
    assert pre.type == "number"
    assert pre.default_value == "0.5"

    default_qc_only = next(p for p in parameters if p.name == "default_qc_only")
    assert default_qc_only.type == "integer"
    assert default_qc_only.default_value == "1"


def test_pydantic_settings_extractor():
    extractor = PydanticSettingsExtractor()
    example_path = (
        pathlib.Path(__file__).parent / "resources" / "pydantic_settings_example.py"
    )
    parameters = extractor.extract_parameters(str(example_path))

    assert len(parameters) == 13
    assert all(isinstance(p, Parameter) for p in parameters)

    override_date = next(p for p in parameters if p.name == "override_date")
    assert override_date.type == "string"
    assert override_date.description

    intervals_table = next(p for p in parameters if p.name == "intervals_table")
    assert intervals_table.type == "string"
    assert intervals_table.default_value == "trials"

    pre = next(p for p in parameters if p.name == "pre")
    assert pre.type == "number"
    assert pre.default_value == "0.5"

    default_qc_only = next(p for p in parameters if p.name == "default_qc_only")
    assert default_qc_only.type == "integer"
    assert default_qc_only.default_value == "1"

    bin_size_s = next(p for p in parameters if p.name == "bin_size_s")
    assert bin_size_s.type == "number"
    assert bin_size_s.default_value == "0.001"

    max_workers = next(p for p in parameters if p.name == "max_workers")
    assert max_workers.type == "integer"
    assert max_workers.default_value is None


def test_argparse_extractor_rejects_bool_type(tmp_path):
    extractor = ArgparseExtractor()
    example_path = tmp_path / "bool_type_test.py"

    with open(example_path, "w") as f:
        f.write(
            """import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test-field", type=bool, default=True)
"""
        )

    with pytest.raises(
        ValueError, match=r"uses type=bool.*will not work as expected.*use type=int"
    ):
        extractor.extract_parameters(str(example_path))


def test_argparse_extractor_rejects_flag_actions(tmp_path):
    extractor = ArgparseExtractor()

    test_cases = [
        ("store_true", 'parser.add_argument("--flag", action="store_true")'),
        ("store_false", 'parser.add_argument("--flag", action="store_false")'),
        (
            "BooleanOptionalAction",
            'parser.add_argument("--flag", action=argparse.BooleanOptionalAction)',
        ),
    ]

    for action_name, code in test_cases:
        example_path = tmp_path / f"{action_name}_test.py"
        with open(example_path, "w") as f:
            f.write(
                f"""import argparse

parser = argparse.ArgumentParser()
{code}
"""
            )

        with pytest.raises(
            ValueError, match=r"uses a flag-type action.*not compatible with app panels"
        ):
            extractor.extract_parameters(str(example_path))
