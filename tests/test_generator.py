from __future__ import annotations

from pathlib import Path

from auto_app_panel.extractors import PydanticSettingsExtractor
from auto_app_panel.generator import generate_app_panel


def test_extract_parameters_from_example():
    extractor = PydanticSettingsExtractor()
    example_file = Path(__file__).parent / "resources" / "pydantic_settings_example.py"

    parameters = extractor.extract_parameters(str(example_file))

    assert len(parameters) == 13
    assert any(p.name == "intervals_table" for p in parameters)
    assert any(p.name == "pre" for p in parameters)

    pre_param = next(p for p in parameters if p.name == "pre")
    assert pre_param.type == "number"
    assert pre_param.default_value == "0.5"


def test_generate_app_panel_new_file(tmp_path):
    extractor = PydanticSettingsExtractor()
    example_file = Path(__file__).parent / "resources" / "pydantic_settings_example.py"
    parameters = extractor.extract_parameters(str(example_file))

    output_file = tmp_path / "app-panel.json"
    generate_app_panel(parameters, output_file)

    assert output_file.exists()


def test_generate_app_panel_merge_with_existing(tmp_path):
    import json

    extractor = PydanticSettingsExtractor()
    example_file = Path(__file__).parent / "resources" / "pydantic_settings_example.py"
    parameters = extractor.extract_parameters(str(example_file))

    existing_file = Path(__file__).parent / "resources" / "app-panel.json"
    output_file = tmp_path / "app-panel.json"

    with open(existing_file) as f:
        existing_data = json.load(f)
    with open(output_file, "w") as f:
        json.dump(existing_data, f)

    generate_app_panel(parameters, output_file, strategy="overwrite", backup=False)

    with open(output_file) as f:
        result = json.load(f)

    assert len(result["parameters"]) > 0

    intervals_param = next(
        p for p in result["parameters"] if p["name"] == "intervals_table"
    )
    assert intervals_param["id"] == "7any1TAR5nwy12pj"
    assert (
        "description" not in intervals_param or intervals_param["description"] is None
    )
