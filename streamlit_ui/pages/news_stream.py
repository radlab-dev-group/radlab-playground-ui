import streamlit as st

from src.token_utils import TokenValidator
from src.language import LanguageTranslator
from src.session_config import SessionConfig
from src.constants import DEFAULT_UI_CONFIG_PATH
from src.api_public import (
    PublicNewsStreamAPI,
    PlaygroundAuthenticationAPI,
    PlaygroundAdministrationAPI,
)
from src.ui_utils_public import (
    prepare_news_stream_params_public,
    prepare_news_stream_public_news_tab,
    initialize_page,
)


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="stream_page_title"),
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    token_str = SessionConfig.get_session_auth_token()
    token_info = SessionConfig.get_session_auth_token_full_info()

    if token_info is None:
        token_str = None

    if token_str is not None:
        _tv = TokenValidator()
        if not _tv.validate_token_string(token_str=token_str):
            st.error("Token is not valid")
            return

    p_ns_api = PublicNewsStreamAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )
    auth_api = PlaygroundAuthenticationAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )
    categories_with_pages = p_ns_api.list_available_categories_with_pages()
    news_options = prepare_news_stream_params_public(
        categories_with_pages=categories_with_pages,
        token_str=token_str,
        token_info=token_info,
    )

    only_with_messages = news_options.get("admin", {}).get(
        "show_only_with_message", False
    )

    if token_str is not None and len(token_str) and only_with_messages:
        admin_api = PlaygroundAdministrationAPI(config_path=DEFAULT_UI_CONFIG_PATH)
        all_news_in_categories = admin_api.show_news_to_check_correctness(
            number_of_news=news_options["news_in_category"],
            filter_pages=news_options["filter_pages"],
            token_str=token_str,
            token_info=token_info,
            auth_api=auth_api,
        )
    else:
        all_news_in_categories = p_ns_api.all_news_from_all_categories(
            news_in_category=news_options["news_in_category"],
            filter_pages=news_options["filter_pages"],
            polarity_3c=news_options["polarity_3c"],
            pli_from=news_options["pli_from"],
            pli_to=news_options["pli_to"],
        )

    if len(all_news_in_categories):
        # Filter pages for SSE
        prepare_news_stream_public_news_tab(
            categories=categories_with_pages,
            news_in_categories=all_news_in_categories,
            sort_date_by=news_options["sort_news_by"],
            number_of_news=news_options["news_in_category"],
            user_token=token_str,
            token_info=token_info,
            publ_news_api=p_ns_api,
            auth_api=auth_api,
            admin_opts=news_options["admin"],
            filter_pages=news_options["filter_pages"],
        )


if __name__ == "__main__":
    main()
