import streamlit as st

from src.language import LanguageTranslator
from src.ui_utils_public import initialize_page


def show_info(elem):
    tab_general, tab_description = elem.tabs(
        [
            LanguageTranslator.translate(code_name="info_explorer_main_info"),
            LanguageTranslator.translate(code_name="info_explorer_short_about"),
        ]
    )

    tab_general.markdown(
        LanguageTranslator.translate(code_name="info_explorer_main_description_pt1")
    )

    # yesterday = datetime.datetime.today() - datetime.timedelta(days=1, hours=3)
    # yesterday_str = yesterday.strftime("%d.%m.%Y")
    yesterday_str = "28.06.2025"

    tab_general.info(
        LanguageTranslator.translate(
            code_name="info_explorer_main_description_pt2"
        ).replace("{yesterday_str}", yesterday_str)
    )
    tab_general.markdown(
        LanguageTranslator.translate(code_name="info_explorer_main_description_pt3")
    )
    tab_general.markdown(
        LanguageTranslator.translate(code_name="info_explorer_main_description_pt4")
    )

    tab_general.markdown(
        LanguageTranslator.translate(code_name="info_explorer_main_description_pt5")
    )

    tab_description.write(
        LanguageTranslator.translate(code_name="info_explorer_how_works")
    )

    tab_description.markdown(
        LanguageTranslator.translate(code_name="info_explorer_how_works_descr_pt1")
    )
    full_g_in_exp = tab_description.expander(
        LanguageTranslator.translate(code_name="info_explorer_sample_full_g_info")
    )
    full_g_in_exp.image("resources/images/graphs/main_full_20250606.jpg")

    tab_description.markdown(
        LanguageTranslator.translate(code_name="info_explorer_how_works_descr_pt2")
    )

    sample_g_in_exp = tab_description.expander(
        LanguageTranslator.translate(code_name="info_explorer_sample_continuous_g")
    )
    sample_g_in_exp.image("resources/images/graphs/papiez_franciszek_20250606.jpg")
    sample_g_in_exp.markdown(
        LanguageTranslator.translate(code_name="info_explorer_how_works_descr_pt3")
    )

    tab_description.markdown(
        LanguageTranslator.translate(code_name="info_explorer_how_works_descr_pt4")
    )
    sample_ncg_in_exp = tab_description.expander(
        LanguageTranslator.translate(
            code_name="info_explorer_sample_noncontinuous_g"
        )
    )
    sample_ncg_in_exp.image("resources/images/graphs/papiez_franciszek_general.png")

    tab_description.markdown(
        LanguageTranslator.translate(code_name="info_explorer_how_works_descr_pt5")
    )


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(
            code_name="info_explorer_page_title"
        ),
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    _, g_logo, _ = st.columns(3)
    g_logo.image("resources/images/graphs/eksplorator_informacji_logo.jpg")

    main_container = st.container(border=True)
    show_info(main_container)


if __name__ == "__main__":
    main()
