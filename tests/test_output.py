import json
from pathlib import Path

import pytest

# Base directory is the project root where this test runs
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "smart_complaint" / "prompts"

def test_prompts_folder_contains_required_files():
    base_prompt = PROMPTS_DIR / "base_prompt.txt"
    styles_json = PROMPTS_DIR / "styles_prompts.json"

    assert base_prompt.exists(), "base_prompt.txt is missing in prompts/"
    assert styles_json.exists(), "styles_prompts.json is missing in prompts/"

def test_styles_json_has_required_fields():
    styles_json_path = PROMPTS_DIR / "styles_prompts.json"

    with styles_json_path.open(encoding="utf-8") as f:
        styles = json.load(f)

    assert isinstance(styles, list), "styles_prompts.json should contain a dictionary"
    assert len(styles) > 0, "styles_prompts.json is empty"

    for style in styles:
        assert "name" in style, "Each style must have a 'name'"
        assert "prompt" in style, "Each style must have a 'prompt'"
