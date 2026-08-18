import streamlit as st

from src.constants import ApplicationIcons
from src.token_utils import TokenValidator
from src.language import LanguageTranslator
from src.session_config import SessionConfig


def main():
    token_str = SessionConfig.get_session_auth_token()
    # token_info = SessionConfig.get_session_auth_token_full_info()
    # if token_info is None:
    #     token_str = None
    if token_str is not None:
        _tv = TokenValidator()
        if not _tv.validate_token_string(token_str=token_str):
            st.error("Token is not valid")
            return

    pages = [
        st.Page(
            "pages/home.py",
            title=LanguageTranslator.translate(code_name="menu_home"),
            icon=ApplicationIcons.HOME_ICO,
        ),
        st.Page(
            "pages/news_stream.py",
            title=LanguageTranslator.translate(code_name="menu_news_stream"),
            icon=ApplicationIcons.STREAM_ICO,
        ),
        st.Page(
            "pages/creator_actual.py",
            title=LanguageTranslator.translate(code_name="menu_actual_info_creator"),
            icon=ApplicationIcons.CREATOR_ICO,
        ),
        st.Page(
            "pages/news_browser.py",
            title=LanguageTranslator.translate(code_name="menu_info_browser"),
            icon=ApplicationIcons.BROWSER_ICO,
        ),
        st.Page(
            "pages/info_explorator.py",
            title=LanguageTranslator.translate(code_name="menu_info_explorer"),
            icon=ApplicationIcons.EXPLORER_ICO,
        ),
        st.Page(
            "pages/administration.py",
            title=LanguageTranslator.translate(code_name="menu_administration"),
            icon=ApplicationIcons.ADMINISTRATION_ICO,
        ),
    ]

    if token_str is not None and len(token_str.strip()):
        last_page = pages[-1]

        pages[-1] = st.Page(
            "pages/public_chat.py",
            title=LanguageTranslator.translate(code_name="menu_public_chat"),
            icon=ApplicationIcons.PUBLIC_CHAT_ICO,
        ),
        pages.append(
            st.Page(
                "pages/statistics.py",
                title=LanguageTranslator.translate(code_name="menu_statistics"),
                icon=ApplicationIcons.STATISTICS_ICO,
            )
        )
        pages.append(last_page)

    nav = st.navigation(pages)
    nav.run()


main()
