import streamlit as st

from src.language import LanguageTranslator
from src.constants import DEFAULT_UI_CONFIG_PATH

from src.api_public import PublicConversationWithModelAPI  # , PublicNewsStreamAPI
from src.ui_utils_public import (
    prepare_generation_params_public,
    prepare_public_state_options,
    prepare_public_chat,
    initialize_page,
)


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="public_chat_page_title"),
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    p_c_api = PublicConversationWithModelAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )

    # when RAG is available through public chat, then uncomment
    # p_ns_api = PublicNewsStreamAPI(
    #     config_path=DEFAULT_UI_CONFIG_PATH,
    # )

    available_models = p_c_api.list_available_models()
    if not len(available_models):
        st.write(available_models)
    else:
        gen_model, gen_options, conv_options = prepare_generation_params_public(
            generative_models=available_models, expanded_model_options=False
        )

        # when RAG is available through public chat, then uncomment
        categories_with_pages = []
        # categories_with_pages = p_ns_api.list_available_categories_with_pages()

        state_options, rag_search_options, last_msg_summary_options = (
            prepare_public_state_options(
                force_use_rag_supervisor=False,
                force_use_content_supervisor=True,
                categories_with_pages=categories_with_pages,
                force_show_options=False,
            )
        )

        prepare_public_chat(
            generative_model=gen_model,
            generation_options=gen_options,
            conversation_options=conv_options,
            public_conv_with_model=p_c_api,
            public_state_options=state_options,
            rag_search_options=rag_search_options,
            force_use_rag_supervisor=False,
        )


if __name__ == "__main__":
    main()
