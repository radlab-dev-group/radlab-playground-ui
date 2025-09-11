import streamlit as st

from src.language import LanguageTranslator
from src.session_config import SessionConfig
from src.ui_utils_public import initialize_page
from src.api_public import PublicNewsBrowserAPI
from src.constants import DEFAULT_UI_CONFIG_PATH
from src.news_browser import (
    add_menu,
    show_summaries_for_day,
    select_which_summary,
)


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="news_browser_page_title"),
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    token_str = SessionConfig.get_session_auth_token()
    if token_str is not None and not len(token_str.strip()):
        token_str = None

    # if token_str is None or not len(token_str):
    #     st.write("**Testujemy nową funkcjonalność** -- zapraszamy wkrótce! :)")
    #     return

    p_ns_api = PublicNewsBrowserAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )

    settings, menu_container = add_menu(
        is_logged=token_str is not None and len(token_str)
    )
    selected_day = settings["selected_day"]
    if selected_day is None:
        st.write(LanguageTranslator.translate(code_name="news_browser_select_date"))
        return

    with st.spinner(
        LanguageTranslator.translate(code_name="news_browser_data_loading")
    ):
        summaries = p_ns_api.get_summary_of_day(date=selected_day)

    if "summaries" not in summaries:
        LanguageTranslator.translate(
            code_name="news_browser_select_date_no_data"
        ).replace("{selected_day}", selected_day)
        return

    summaries = summaries["summaries"]
    summary_number = 0
    if len(summaries) > 1:
        summary_number = select_which_summary(
            summaries, menu_container=menu_container
        )

    show_summaries_for_day(
        day=selected_day,
        summaries=summaries,
        summary_number=summary_number,
        menu_container=menu_container,
        is_admin_logged=token_str is not None,
    )


if __name__ == "__main__":
    main()
