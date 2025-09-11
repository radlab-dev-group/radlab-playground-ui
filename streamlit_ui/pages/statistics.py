import streamlit as st

from src.language import LanguageTranslator
from src.constants import DEFAULT_UI_CONFIG_PATH
from src.api_public import PublicNewsStreamAPI
from src.ui_utils_public import show_stats_window, initialize_page


def main():
    settings_id = 1
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="stats_page_title"),
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    publ_api = PublicNewsStreamAPI(config_path=DEFAULT_UI_CONFIG_PATH)
    show_stats_window(publ_api=publ_api, settings_id=settings_id)


if __name__ == "__main__":
    main()
