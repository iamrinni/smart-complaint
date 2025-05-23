import json
import os
from pathlib import Path

from openai import OpenAI

from jinja2 import Template
from dotenv import load_dotenv

load_dotenv('.env')

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("ORGANIZATION")
)

BASE_DIR = Path(__file__).parent

# Now correctly resolve prompts path relative to this file
STYLES_PATH = BASE_DIR / "prompts" / "styles_prompts.json"
BASE_PROMPT_PATH = BASE_DIR / "prompts" / "base_prompt.txt"


# --- Load styles from JSON ---
with STYLES_PATH.open(encoding="utf-8") as f:
    STYLES = {style["name"]: style for style in json.load(f)}

# --- Load base Jinja2 prompt template ---
with BASE_PROMPT_PATH.open(encoding="utf-8") as f:
    BASE_PROMPT_TEMPLATE = Template(f.read())


def build_final_prompt(user_input: str, style: dict, base_prompt_template: Template) -> str:
    """Render final prompt using Jinja2 template"""
    context = {
        "situation_description": user_input.strip(),
        "persona_style": style.get("prompt", ""),
        "persona_description": style.get("description", ""),
        "negative_prompt": style.get("negative_prompt", "")
    }
    return base_prompt_template.render(context)


def generate_complaint(user_input: str, style: str, base_prompt_template: Template, styles_set: dict) -> str:
    """Генерує скаргу за допомогою OpenAI API"""

    # Формуємо фінальний промпт, використовуючи шаблон та стиль
    prompt = build_final_prompt(user_input=user_input, style=styles_set[style],
                                base_prompt_template=base_prompt_template)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ти помічник, який генерує скарги у вибраному стилі."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )

    return response.choices[0].message.content.strip()