import streamlit as st
import json
from pathlib import Path
from jinja2 import Template

from complaint_generator import generate_complaint

BASE_DIR = Path(__file__).parent

# Now correctly resolve prompts path relative to this file
STYLES_PATH = BASE_DIR / "prompts" / "styles_prompts.json"
BASE_PROMPT_PATH = BASE_DIR / "prompts" / "base_prompt.txt"

# --- Завантаження шаблону ---
with BASE_PROMPT_PATH.open(encoding="utf-8") as f:
    base_prompt_template = Template(f.read())

# --- Завантаження стилів ---
with STYLES_PATH.open(encoding="utf-8") as f:
    styles_list = json.load(f)
    style_map = {style["name"]: style for style in styles_list}
    style_description_map = {style["name"]: style["description"] for style in styles_list}
    style_names = list(style_map.keys())

# --- Інтерфейс ---
st.title("📝 Розумна Скарга")

selected_style = st.selectbox(
    "Оберіть стиль скарги:",
    style_names,
    format_func=lambda name: f"{name} — {style_description_map[name]}"
)

user_input = st.text_area(
    "Коротко опишіть проблему:",
    height=150,
    placeholder="Наприклад: Мені третій день не приносять доставку..."
)

if st.button("✍️ Згенерувати скаргу"):
    complaint = generate_complaint(
        user_input=user_input,
        style=selected_style,
        base_prompt_template=base_prompt_template,
        styles_set=style_map
    )

    st.subheader("✉️ Згенерована скарга:")
    st.write(complaint)

    #st.markdown("---")
    #st.subheader("🧠 Аналіз тону:")
    #st.write(tone)
