"""

Module that defines the Streamlit UI for the news article creator feature. It
leverages translation utilities, public APIs for fetching news streams and
generating articles, and UI helper functions to present results to the user.

Functions
---------
add_about_creator_to_sidebar():
    Adds an informational expander to the sidebar describing the creator.

add_technical_info_for_gen_full_article(new_article_response, answer_container,
                                         number_of_news_used_to_generate):
    Renders technical metadata (generation time, model, source count, etc.) for
    a generated article.

call_generate_article_api_and_show_response(user_query_str, type_of_new_article,
                                            answer_column, search_in_category,
                                            publ_creator_api, query_response_id):
    Calls the PublicNewsCreatorAPI to generate an article based on selected news
    IDs and displays the result together with technical info.

show_creator_search_window(news_options, publ_news_api, publ_creator_api,
                           categories_sorted):
    Builds the main UI where the user enters a query, selects options, and
    triggers the generation workflow.
"""

import time
import streamlit as st

from typing import List

from src.language import LanguageTranslator
from src.api_public import PublicNewsStreamAPI, PublicNewsCreatorAPI
from src.ui_utils_public_search import call_search_api_and_show_result


def add_about_creator_to_sidebar():
    """
    Add an informational expander to the sidebar.

    The expander contains a short description of the “creator” feature,
    using translated strings obtained from :class:`LanguageTranslator`.

    Returns
    -------
    None
    """
    general_info_cont = st.sidebar.expander(
        LanguageTranslator.translate(code_name="act_creator_what_is_expander"),
        expanded=False,
    )

    general_info_cont.info(
        LanguageTranslator.translate(code_name="act_creator_what_is_description")
    )


def add_technical_info_for_gen_full_article(
    new_article_response, answer_container, number_of_news_used_to_generate
):
    """
    Render technical metadata for a generated article.

        Parameters
        ----------
        new_article_response : dict
            The API response containing generation details (timestamp, duration,
            model name, etc.).
        answer_container : streamlit.container
            The Streamlit container where the information will be written.
        number_of_news_used_to_generate : int
            How many news items were fed to the generation model.

        The function writes a visual divider followed by several ``write`` calls
        that display when the article was generated, how long it took, which model
        was used, and how many source news items contributed to the output.

        Returns
        -------
        None
    """
    answer_container.divider()
    # when
    when_generated = new_article_response.get("when_generated", "?")
    answer_container.write(
        LanguageTranslator.translate(code_name="act_creator_when_generated").replace(
            "{when_generated}", str(when_generated)
        )
    )
    # time
    generation_time = new_article_response.get("generation_time", "?")
    answer_container.write(
        LanguageTranslator.translate(code_name="act_creator_gen_time").replace(
            "{generation_time}", str(generation_time)
        )
    )
    # model
    model_used_to_generate = new_article_response.get("model_used_to_generate", "")
    answer_container.write(
        LanguageTranslator.translate(code_name="act_creator_gen_model").replace(
            "{model_used_to_generate}", model_used_to_generate
        )
    )

    # num of news
    answer_container.write(
        LanguageTranslator.translate(
            code_name="act_creator_news_to_generate"
        ).replace(
            "{number_of_news_used_to_generate}", str(number_of_news_used_to_generate)
        )
    )


def call_generate_article_api_and_show_response(
    user_query_str: str,
    type_of_new_article: str,
    answer_column,
    search_in_category: dict,
    publ_creator_api: PublicNewsCreatorAPI,
    query_response_id: int,
):
    """
    Call the article‑generation API and display the result.

        This helper aggregates all news IDs from the ``search_in_category`` mapping,
        invokes :meth:`PublicNewsCreatorAPI.generate_article_from_search_result`,
        writes the generated article text to the UI, and finally calls
        :func:`add_technical_info_for_gen_full_article` to show generation metadata.

        Parameters
        ----------
        user_query_str : str
            The original query entered by the user.
        type_of_new_article : str
            A textual prompt describing the desired article style (e.g., “simple”,
            “formal”).
        answer_column : streamlit.column
            The column where the article text and metadata will be rendered.
        search_in_category : dict
            Mapping of category names to lists of news dictionaries; each dict must
            contain an ``id`` key.
        publ_creator_api : PublicNewsCreatorAPI
            API client responsible for article generation.
        query_response_id : int
            Identifier of the search query, forwarded to the generation endpoint.

        Returns
        -------
        None
    """
    answer_container = answer_column.container(border=False)
    all_news_ids = []
    for category_news in search_in_category.values():
        all_news_ids.extend(n["id"] for n in category_news)

    new_article_response = publ_creator_api.generate_article_from_search_result(
        news_ids=all_news_ids,
        user_query_str=user_query_str,
        type_of_new_article=type_of_new_article,
        query_response_id=query_response_id,
        api_call_url=None,
    )

    new_article = new_article_response["article_str"]
    answer_container.write(new_article)

    # Add technical info
    add_technical_info_for_gen_full_article(
        new_article_response=new_article_response,
        answer_container=answer_container,
        number_of_news_used_to_generate=len(all_news_ids),
    )


def show_creator_search_window(
    news_options: dict,
    publ_news_api: PublicNewsStreamAPI,
    publ_creator_api: PublicNewsCreatorAPI,
    categories_sorted: List[str],
):
    """
    Build the main Streamlit UI for the article‑creation workflow.

        The UI consists of:
        * A text area for the user’s query.
        * Controls for selecting article style (simple / formal) and the look‑back
          window (last 1‑2 days).
        * A “Create” button that triggers a search via
          :func:`call_search_api_and_show_result` and, upon success, calls
          :func:`call_generate_article_api_and_show_response`.

        Parameters
        ----------
        news_options : dict
            Configuration for the available news sources; passed unchanged to the
            search helper.
        publ_news_api : PublicNewsStreamAPI
            API client used to retrieve news streams based on the user query.
        publ_creator_api : PublicNewsCreatorAPI
            API client used to generate the final article.
        categories_sorted : List[str]
            Ordered list of category names that determines the presentation order
            of search results.

        Returns
        -------
        None
    """
    main_container = st.container(border=False)
    progress_container = main_container.container(border=False)
    query_rag_column, answer_column = main_container.columns([1, 2])

    user_query_container = query_rag_column.container(border=True)
    user_query_str = user_query_container.text_area(
        label=LanguageTranslator.translate(
            code_name="act_creator_describe_news_label"
        ),
        label_visibility="hidden",
        placeholder=LanguageTranslator.translate(
            code_name="act_creator_describe_news_placeholder"
        ),
    )

    query_options_column, last_days_column = user_query_container.columns([4, 1])
    type_of_new_article_show = query_options_column.selectbox(
        LanguageTranslator.translate(code_name="act_creator_news_style_choose"),
        [
            LanguageTranslator.translate(code_name="act_creator_news_style_simple"),
            LanguageTranslator.translate(code_name="act_creator_news_style_formal"),
        ],
    )
    last_days = last_days_column.selectbox(
        LanguageTranslator.translate(code_name="act_creator_news_last_days"),
        [1, 2],
        index=0,
    )

    type_of_new_article = LanguageTranslator.translate(
        code_name="act_creator_model_prompt_p1"
    )

    if "formal" in type_of_new_article_show:
        type_of_new_article += " " + LanguageTranslator.translate(
            code_name="act_creator_model_prompt_formal"
        )
    else:
        type_of_new_article += " " + LanguageTranslator.translate(
            code_name="act_creator_model_prompt_simple"
        )

    btn_create_news = user_query_container.button(
        LanguageTranslator.translate(code_name="act_creator_btn_run")
    )
    if btn_create_news:
        if not len(user_query_str):
            user_query_container.error(
                LanguageTranslator.translate(code_name="act_creator_model_no_query")
            )
            return

        whole_process_bar = progress_container.progress(
            0.1,
            text=LanguageTranslator.translate(
                code_name="act_creator_creation_progress"
            ),
        )

        search_n_in_cat, query_response_id = call_search_api_and_show_result(
            user_query_str=user_query_str,
            query_rag_column=query_rag_column,
            publ_news_api=publ_news_api,
            news_options=news_options,
            categories_sorted=categories_sorted,
            num_of_results=0,
            last_days=int(last_days),
        )
        if not len(search_n_in_cat):
            query_rag_column.info(
                LanguageTranslator.translate(
                    code_name="act_creator_no_data_found_db"
                )
            )
            return

        progress_text_gen = LanguageTranslator.translate(
            code_name="act_creator_in_progress_gen"
        )
        whole_process_bar.progress(0.3, text=progress_text_gen)
        call_generate_article_api_and_show_response(
            user_query_str=user_query_str,
            type_of_new_article=type_of_new_article,
            search_in_category=search_n_in_cat,
            answer_column=answer_column,
            publ_creator_api=publ_creator_api,
            query_response_id=query_response_id,
        )

        whole_process_bar.progress(
            1.0, text=LanguageTranslator.translate(code_name="act_creator_ready")
        )
        time.sleep(1)
        whole_process_bar.empty()
