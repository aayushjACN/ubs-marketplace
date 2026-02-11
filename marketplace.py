# app.py
"""
App entry point:
- Sets Streamlit theme/page config
- Injects Streamlit CSS + App component CSS
- Renders: Header, Hero, Services, Chat/Tabs (local), Footer
"""
from __future__ import annotations

from pathlib import Path
import json
import streamlit as st

from assets import HERO_URI
from streamlit_css import inject_streamlit_css
from ubs_components import inject_app_css, render_header, render_hero, render_services, render_footer
from helpers import section_spacer, ubs_container, render_app_card

# --------------------------- Streamlit setup (theme + page) ---------------------------
def _write_theme_config() -> None:
    Path(".streamlit").mkdir(parents=True, exist_ok=True)
    (Path(".streamlit") / "config.toml").write_text(
        """
[theme]
base = "light"
primaryColor = "#e60000"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f4f3ee"
textColor = "#1c1c1c"
font = "sans serif"
""".strip()
    )

_write_theme_config()
st.set_page_config(page_title="UBS – United Kingdom (PoC)", layout="wide")

# --------------------------- CSS injection ---------------------------
inject_app_css(HERO_URI)       # App component CSS (header/hero/services/footer)
inject_streamlit_css()         # Streamlit-only CSS (titles/tabs/chat_input/etc.)

# --------------------------- Page render ---------------------------
render_header()

hero_header_text = "How can AI transform global wealth?"
hero_paragraph_text = "The world of AI is evolving rapidly. Discover how UBS leverages cutting-edge AI technologies to enhance your wealth management experience."
hero_button_text = "Explore more"
render_hero(hero_header_text, hero_paragraph_text, hero_button_text)

section_spacer()

services_header_text = "The UBS Innovation Lab"
services_items = [
    (
        "Who we are",
        "A dedicated team of technologists and financial experts driving innovation in wealth management.",
        "More about us"
    ),
    (
        "What the Lab does",
        "We explore emerging technologies like AI, blockchain, and data analytics to create next-gen financial solutions.",
        "Our projects"
    ),
    (
        "How we work",
        "Collaborating with startups, academia, and industry leaders to bring cutting-edge solutions to our clients.",
        "Partnerships"
    ),
]
render_services(services_header_text, services_items)

# Load apps from JSON
with open("apps.json", "r") as f:
    app_cards = []
    app_cards = json.load(f)

section_spacer()

# Toolbar band — give it breathing room below
with ubs_container(background="grey", name="ubs_toolbar"):
    st.header("AI Application Marketplace")
    st.write("Discover innovative AI applications tailored for wealth management, asset management, and investment banking.")
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    search_col, filter_col = st.columns([5,1], gap="small")
    with search_col:
        search_query = st.text_input("Search applications", placeholder="Search AI applications", label_visibility="collapsed")
    with filter_col:
        with st.popover("Filter by", use_container_width=True):
            selected_ai_types = st.pills("AI Type", ["Generative AI","Predictive Analytics","NLP"], selection_mode="multi")
            selected_business_lines = st.pills("Business Line", ["Wealth Management","Asset Management","Investment Bank"], selection_mode="multi")
            selected_functions = st.pills("Function", ["Advisory","Research","KYC & Risk","Productivity"], selection_mode="multi")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# # Featured (single)
# with ubs_container(background="white"):
#     c1, c2, c3 = st.columns([1, 5, 1], gap="large")
#     with c2:
#         render_app_card(app_card, variant="feature", clamp_width=False, top_margin_px=0)

# apps = [app_card, {**app_card,"title":"UBS AgentForge"}, {**app_card,"title":"Risk Summarizer"},  {**app_card,"title":"Client Signals"},
#         {**app_card,"title":"Portfolio Copilot"}, {**app_card,"title":"Entity Extractor"}, {**app_card,"title":"KYC Assistant"}]

# # Grid (3-up tiles) — a bit of top air
# with ubs_container(background="white"):
#     st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
#     cols = st.columns(3, gap="medium")
#     for i, a in enumerate(apps):
#         with cols[i % 3]:
#             render_app_card(a, variant="tile", top_margin_px=16)
#     # --- Responsible AI line (below grid) ---
#     section_spacer()
#     st.write("These applications provide insights and simulations and are governed by UBS Responsible AI principles.")


# # Featured card (always the first)
# with ubs_container(background="white"):
#     c1, c2, c3 = st.columns([1, 5, 1], gap="large")
#     with c2:
#         render_app_card(app_cards[0], variant="feature", clamp_width=False, top_margin_px=0)


# Filter + search apps dynamically
filtered_apps = []
for app in app_cards:
    if search_query and search_query.lower() not in app["title"].lower():
        continue
    if selected_ai_types and app["ai_type"] not in selected_ai_types:
        continue
    if selected_business_lines and app["business_line"] not in selected_business_lines:
        continue
    if selected_functions and app["function"] not in selected_functions:
        continue
    filtered_apps.append(app)

# Display app cards dynamically
with ubs_container(background="white"):
    st.subheader("All Applications")
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    for i, a in enumerate(filtered_apps):
        with cols[i % 3]:
            render_app_card(a, variant="tile", top_margin_px=16)
    section_spacer()
    st.write("These applications provide insights and simulations and are governed by UBS Responsible AI principles.")
section_spacer()
render_footer()
