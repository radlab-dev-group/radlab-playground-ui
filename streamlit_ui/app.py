import streamlit as st

from src.language import LanguageTranslator
from src.constants import ApplicationIcons


def main():
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
            "pages/public_chat.py",
            title=LanguageTranslator.translate(code_name="menu_public_chat"),
            icon=ApplicationIcons.PUBLIC_CHAT_ICO,
        ),
        st.Page(
            "pages/statistics.py",
            title=LanguageTranslator.translate(code_name="menu_statistics"),
            icon=ApplicationIcons.STATISTICS_ICO,
        ),
        st.Page(
            "pages/administration.py",
            title=LanguageTranslator.translate(code_name="menu_administration"),
            icon=ApplicationIcons.ADMINISTRATION_ICO,
        ),
    ]
    nav = st.navigation(pages)
    nav.run()


main()
