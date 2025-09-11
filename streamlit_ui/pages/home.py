import streamlit as st

from src.language import LanguageTranslator
from src.ui_utils_public import initialize_page


def add_stram_description(elem):
    elem.markdown(
        LanguageTranslator.translate(code_name="home_stream_description_pt1")
    )
    elem_exp = elem.expander(
        LanguageTranslator.translate(code_name="home_stream_more_info")
    )
    elem_exp.markdown(
        LanguageTranslator.translate(code_name="home_stream_description_pt2")
    )


def add_creator_description(elem):
    elem.markdown(LanguageTranslator.translate(code_name="home_creator_description"))


def add_news_browser_description(elem):
    elem.markdown(
        LanguageTranslator.translate(code_name="home_news_browser_description")
    )


def add_information_extractor_description(elem):
    elem.markdown(
        LanguageTranslator.translate(code_name="home_info_extr_description")
    )


def add_chat_description(elem):
    elem.markdown(LanguageTranslator.translate(code_name="home_chat_description"))


def add_stats_description(elem):
    elem.markdown(LanguageTranslator.translate(code_name="home_stats_description"))


def add_admin_description(elem):
    elem.markdown(LanguageTranslator.translate(code_name="home_admin_description"))


def home():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="home_page_title"),
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    _, cent_co, _ = st.columns(3)
    cent_co.image("resources/images/logo-home.png", width=200)

    st.markdown(LanguageTranslator.translate(code_name="home_plg_descr"))

    more_info_exp = st.expander(
        LanguageTranslator.translate(code_name="home_plg_more_info")
    )
    more_info_exp.markdown(
        LanguageTranslator.translate(code_name="home_plg_descr_detailed_p1")
    )

    instruct_exp = st.expander(
        LanguageTranslator.translate(code_name="home_plg_more_info_p2")
    )
    instruct_exp.markdown(
        LanguageTranslator.translate(code_name="home_plg_descr_detailed_p2")
    )
    sections = [
        LanguageTranslator.translate(code_name="home_tab_news_stream"),
        LanguageTranslator.translate(code_name="home_tab_creator_actual"),
        LanguageTranslator.translate(code_name="home_tab_info_viewer"),
        LanguageTranslator.translate(code_name="home_tab_info_explorator"),
        LanguageTranslator.translate(code_name="home_tab_public_chat"),
        LanguageTranslator.translate(code_name="home_tab_statistics"),
        LanguageTranslator.translate(code_name="home_tab_admin"),
    ]

    apps_desc_container = st.container(border=True)

    stream, creator, n_browser, i_explorator, chat, stats, admin = (
        apps_desc_container.tabs(sections)
    )
    add_stram_description(stream)
    add_creator_description(creator)
    add_news_browser_description(n_browser)
    add_information_extractor_description(i_explorator)
    add_chat_description(chat)
    add_stats_description(stats)
    add_admin_description(admin)


if __name__ == "__main__":
    home()
