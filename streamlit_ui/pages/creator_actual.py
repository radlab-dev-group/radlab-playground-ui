import streamlit as st

from src.language import LanguageTranslator
from src.constants import DEFAULT_UI_CONFIG_PATH
from src.api_public import PublicNewsStreamAPI, PublicNewsCreatorAPI
from src.ui_utils_public import prepare_info_creator_public, initialize_page

from src.actual_creator import (
    add_about_creator_to_sidebar,
    show_creator_search_window,
)


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="creator_page_title"),
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    add_about_creator_to_sidebar()
    # token_str = SessionConfig.get_session_auth_token()
    # token_info = SessionConfig.get_session_auth_token_full_info()

    p_ns_api = PublicNewsStreamAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )

    p_nc_api = PublicNewsCreatorAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )

    categories_with_pages = p_ns_api.list_available_categories_with_pages()
    news_options = prepare_info_creator_public(
        categories_with_pages=categories_with_pages
    )

    # show_examples(SAMPLE_SSE_QUERIES)
    categories_sorted = list(news_options["filter_pages"].keys())
    show_creator_search_window(
        news_options=news_options,
        publ_news_api=p_ns_api,
        publ_creator_api=p_nc_api,
        categories_sorted=categories_sorted,
    )


if __name__ == "__main__":
    main()
