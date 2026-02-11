# app.py
"""
App entry point:
- Sets Streamlit theme/page config
- Injects Streamlit CSS + App component CSS
- Renders: Header, Hero, Services, Chat/Tabs (local), Footer
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from assets import HERO_URI
from streamlit_css import inject_streamlit_css
from ubs_components import inject_app_css, render_header, render_hero, render_services, render_footer
from helpers import section_spacer

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

# --------------------------- Local-only: Chat & Tabs ---------------------------
def render_chat_and_tabs() -> None:
    with st.container(key="chat_band"):
        with st.container(key="chat_rail"):
            col1, col2 = st.columns([3, 1], gap="small")
            with col1:
                st.header("Chat with us")
                st.write("Ask us anything about our services, investments, or financial planning.")
                st.chat_input("Type a message here...")
            with col2:
                st.subheader("Quick Links")
                tab_a, tab_b, tab_c = st.tabs(["Tab A", "Tab B", "Tab C"])
                with tab_a:
                    st.write("Content for Tab A")
                with tab_b:
                    st.write("Content for Tab B")
                with tab_c:
                    st.write("Content for Tab C")

            st.divider()

# --------------------------- Page render ---------------------------
def main() -> None:
    render_header()
    render_hero()
    section_spacer()
    render_services()
    section_spacer()
    render_chat_and_tabs()  # kept out of ui_components.py by request
    section_spacer()
    render_footer()
    st.write("")

if __name__ == "__main__":
    main()