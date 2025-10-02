import datetime
import pandas as pd

import streamlit as st
import plotly.express as px

from typing import List, Dict

from src.session_config import SessionConfig
from src.language import LanguageTranslator, _LanguageDefinitions
from src.api_public import (
    PublicConversationWithModelAPI,
    PublicNewsStreamAPI,
    PlaygroundAdministrationAPI,
    PlaygroundAuthenticationAPI,
)
from src.constants import (
    ICON_NOT_SET_NEWS_INFO,
    ICON_NEWS_POLARITY_3C_P,
    ICON_NEWS_POLARITY_3C_N,
    ICON_NEWS_POLARITY_3C_A,
    ICON_FLAG_PL_LANG,
    ICON_FLAG_EN_LANG,
    ICON_FLAG_FR_LANG,
    ICON_FLAG_RU_LANG,
    ICON_FLAG_UA_LANG,
    ICON_FLAG_DE_LANG,
    PLI_DESC_ICONS2VALUE,
    ICON_NEWS_PLI_GOOD,
    ICON_DEFAULT_VALUE_UI,
    DEF_PLI_VALUE_TO_ICON,
    MIN_ARTICLE_LEN,
    DEFAULT_LANGUAGE,
)
from src.data_utils import (
    prepare_news_to_user,
    convert_admin_pages_stats_news_p_day,
    convert_admin_pages_stats_to_polarity_3c,
)


def set_on_change_state() -> None:
    SessionConfig.set_session_free_chat_chat_id(None, None)


def add_category_and_pages_ui(
    categories_with_pages: dict, element, info_creator_window: bool
) -> dict:
    if info_creator_window:
        pages_checkboxes = {}
        for c_name, cat_info in categories_with_pages.items():
            pages_checkboxes[c_name] = [
                {p["main_url"]: True} for p in cat_info["category_pages"]
            ]
        return pages_checkboxes

    if element is None:
        raise TypeError("element to add category page cannot be None")

    selected_sites = element.radio(
        LanguageTranslator.translate(code_name="which_site_to_show"),
        [
            LanguageTranslator.translate(code_name="select_all_sites"),
            LanguageTranslator.translate(code_name="unselect_all_sites"),
        ],
    )

    select_all_pages_opt = selected_sites.lower()
    if "wszystkie" in select_all_pages_opt:
        select_all = "zaznacz" in select_all_pages_opt
    else:
        select_all = "unsel" not in select_all_pages_opt

    pages_checkboxes = {}
    for c_name, cat_info in categories_with_pages.items():
        pages_checkboxes[c_name] = []
        # element.write(cat_info["category_info"]["display_name"])
        all_category_pages = [p["main_url"] for p in cat_info["category_pages"]]
        all_category_pages = list(set(all_category_pages))
        for category_page in all_category_pages:
            if select_all:
                pages_checkboxes[c_name].append(
                    {category_page: element.checkbox(category_page, value=True)}
                )
            else:
                pages_checkboxes[c_name].append(
                    {category_page: element.checkbox(category_page, value=False)}
                )
    return pages_checkboxes


def prepare_public_state_options(
    force_use_rag_supervisor: bool,
    force_use_content_supervisor: bool,
    categories_with_pages,
    force_show_options: bool = False,
):
    state_options = None
    use_content_supervisor = force_use_content_supervisor
    if not force_use_rag_supervisor and not force_use_content_supervisor:
        state_options = st.sidebar.container(border=True)
        state_options.write(
            LanguageTranslator.translate(code_name="general_news_settings")
        )

        use_content_supervisor = state_options.toggle(
            LanguageTranslator.translate(
                code_name="general_work_with_content_supervisor"
            ),
            value=True,
            on_change=set_on_change_state,
        )
    else:
        if force_show_options:
            state_options = st.sidebar.container(border=True)

    use_rag_supervisor = True
    if not force_use_rag_supervisor:
        use_rag_supervisor = False
        # use_rag_supervisor = state_options.toggle(
        #     "Rozmowa z newsami", value=False, on_change=set_on_change_state
        # )

    rag_search_options = None
    last_msg_summary_options = None
    if use_rag_supervisor:
        results_count = 10
        if state_options is None:
            raise Exception("state_options is None!")

        last_days_to_answer = state_options.number_input(
            LanguageTranslator.translate(
                code_name="general_work_rag_supervisor_num_days"
            ),
            value=2,
            min_value=1,
            max_value=5,
            on_change=set_on_change_state,
        )

        cat_www_exp = state_options.expander(
            LanguageTranslator.translate(
                code_name="general_work_rag_supervisor_cat_sites"
            ),
            expanded=True,
        )
        pages_checkboxes = add_category_and_pages_ui(
            categories_with_pages=categories_with_pages,
            element=cat_www_exp,
            info_creator_window=False,
        )

        rerank_results = state_options.toggle(
            LanguageTranslator.translate(
                code_name="general_work_rag_supervisor_use_rerank"
            ),
            value=False,
            on_change=set_on_change_state,
        )

        percentage_rank_mass = 100
        if not force_use_rag_supervisor:
            percentage_rank_mass = state_options.number_input(
                LanguageTranslator.translate(
                    code_name="general_work_rag_supervisor_per_mass"
                ),
                value=80,
                min_value=1,
                max_value=100,
                on_change=set_on_change_state,
            )

        selected_cat_documents = {}
        if len(pages_checkboxes):
            for cat, pages in pages_checkboxes.items():
                for p in pages:
                    for www_url, is_activated in p.items():
                        if is_activated:
                            if cat not in selected_cat_documents:
                                selected_cat_documents[cat] = []
                            selected_cat_documents[cat].append(www_url)

        rag_search_options = {
            "categories": [],
            "documents": [],
            "max_results": results_count,
            "rerank_results": rerank_results,
            "percentage_rank_mass": percentage_rank_mass,
            "return_with_factored_fields": False,
        }

        last_msg_summary_options = {
            "last_days_to_answer": last_days_to_answer,
            "categories_and_pages": selected_cat_documents,
        }

    state_options_dict = {
        "use_content_supervisor": use_content_supervisor,
        "use_rag_supervisor": use_rag_supervisor,
    }

    return state_options_dict, rag_search_options, last_msg_summary_options


def show_public_info_about_rag_supervisor_in_news_conversation():
    st.info(
        LanguageTranslator.translate(
            code_name="general_work_rag_supervisor_main_info"
        )
    )


def prepare_generation_params_public(
    generative_models: List[str], expanded_model_options: bool = False
):
    top_k = 50
    top_p = 0.95
    typical_p = 1.0
    temperature = 0.75
    max_new_tokens = 512
    generative_model = ""
    detailed_expl = False
    explanation_in_list = False
    creative_temperature = 1.1
    repetition_penalty = 1.07
    manual_set_generation_params = False

    if expanded_model_options:
        search_container = st.sidebar.expander(
            LanguageTranslator.translate(code_name="gen_model_spec_expander")
        )
    else:
        search_container = st.sidebar.container(border=True)
        search_container.write(
            LanguageTranslator.translate(code_name="gen_model_spec_expander")
        )

    if len(generative_models):
        generative_model = search_container.selectbox(
            LanguageTranslator.translate(code_name="gen_model_spec_selected_model"),
            generative_models,
            0,
            on_change=set_on_change_state,
        )
    if manual_set_generation_params:
        gen_model_opt_expander = search_container.expander(
            LanguageTranslator.translate(code_name="gen_model_gen_options_expander"),
            expanded=False,
        )
        top_k = gen_model_opt_expander.slider(
            "top_k",
            value=top_k,
            max_value=500,
            min_value=0,
            step=1,
            on_change=set_on_change_state,
        )
        top_p = gen_model_opt_expander.slider(
            "top_p",
            value=0.95,
            max_value=1.0,
            min_value=0.0,
            step=0.01,
            on_change=set_on_change_state,
        )
        temperature = gen_model_opt_expander.slider(
            "temperature",
            value=temperature,
            max_value=2.0,
            min_value=0.0,
            step=0.01,
            on_change=set_on_change_state,
        )
        typical_p = gen_model_opt_expander.slider(
            "typical_p",
            value=typical_p,
            max_value=2.0,
            min_value=0.0,
            step=0.01,
            on_change=set_on_change_state,
        )
        repetition_penalty = gen_model_opt_expander.slider(
            "repetition_penalty",
            value=repetition_penalty,
            max_value=2.0,
            min_value=0.0,
            step=0.01,
            on_change=set_on_change_state,
        )
        set_max_new_tokens = gen_model_opt_expander.toggle(
            LanguageTranslator.translate(
                code_name="gen_model_gen_options_max_tokens_tgl"
            ),
            value=False,
            on_change=set_on_change_state,
        )

        if set_max_new_tokens:
            max_new_tokens = gen_model_opt_expander.slider(
                "max_new_tokens",
                value=max_new_tokens,
                max_value=2048,
                min_value=32,
                step=1,
                on_change=set_on_change_state,
            )
    generation_options = {
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "typical_p": typical_p,
        "repetition_penalty": repetition_penalty,
        "max_new_tokens": max_new_tokens,
    }

    answer_type = search_container.radio(
        LanguageTranslator.translate(
            code_name="gen_model_gen_options_model_verbose"
        ),
        [
            LanguageTranslator.translate(
                code_name="gen_model_gen_options_model_verbose_standard"
            ).replace("{ICON_DEFAULT_VALUE_UI}", ICON_DEFAULT_VALUE_UI),
            LanguageTranslator.translate(
                code_name="gen_model_gen_options_model_verbose_more"
            ),
        ],
        on_change=set_on_change_state,
    )
    if "okład" in answer_type:
        detailed_expl = True

    conversation_options = {
        "detailed_explanation": detailed_expl,
        "explanation_in_list": explanation_in_list,
    }

    return generative_model, generation_options, conversation_options


def prepare_info_creator_public(categories_with_pages):
    pages_checkboxes = add_category_and_pages_ui(
        categories_with_pages=categories_with_pages,
        element=st,
        info_creator_window=True,
    )
    return {"filter_pages": pages_checkboxes}


def prepare_news_stream_params_public(
    categories_with_pages,
    token_str: str | None,
    token_info: dict | None,
    show_news_in_category_count: bool = True,
):
    news_config_container = st.sidebar.container(border=True)
    news_config_container.write(
        LanguageTranslator.translate(code_name="news_stream_params_public")
    )

    show_only_with_message = False
    filter_news_to_show = [50, 100, 150]
    if token_str is not None and len(token_str):
        filter_news_to_show = [20, 50, 100, 5, 10]
        show_only_with_message = news_config_container.toggle(
            LanguageTranslator.translate(
                code_name="news_stream_params_public_show_with_message"
            ),
            value=True,
        )

    news_in_category = 25
    if show_news_in_category_count:
        news_in_category = news_config_container.selectbox(
            LanguageTranslator.translate(
                code_name="news_stream_params_public_news_count"
            ),
            filter_news_to_show,
            on_change=set_on_change_state,
        )

    sort_date_by = news_config_container.selectbox(
        LanguageTranslator.translate(code_name="news_stream_params_public_sort_by"),
        [
            LanguageTranslator.translate(
                code_name="news_stream_params_public_sort_by_newsest"
            ),
            LanguageTranslator.translate(
                code_name="news_stream_params_public_sort_by_oldest"
            ),
        ],
        on_change=set_on_change_state,
    )

    filter_options = news_config_container.expander(
        LanguageTranslator.translate(code_name="news_stream_filter_news_expander"),
        expanded=True,
    )
    which_polarity3c = filter_options.radio(
        LanguageTranslator.translate(code_name="news_stream_filter_news_radio"),
        [
            LanguageTranslator.translate(
                code_name="news_stream_filter_news_radio_all"
            ).replace("{ICON_DEFAULT_VALUE_UI}", ICON_DEFAULT_VALUE_UI),
            LanguageTranslator.translate(
                code_name="news_stream_filter_news_radio_pos"
            ).replace("{ICON_NEWS_POLARITY_3C_P}", ICON_NEWS_POLARITY_3C_P),
            LanguageTranslator.translate(
                code_name="news_stream_filter_news_radio_neg"
            ).replace("{ICON_NEWS_POLARITY_3C_N}", ICON_NEWS_POLARITY_3C_N),
            LanguageTranslator.translate(
                code_name="news_stream_filter_news_radio_amb"
            ).replace("{ICON_NEWS_POLARITY_3C_A}", ICON_NEWS_POLARITY_3C_A),
        ],
    )

    pli_icons = [i for i in PLI_DESC_ICONS2VALUE.keys()]
    pli_icon_selected = filter_options.radio(
        LanguageTranslator.translate(code_name="news_stream_filter_news_pli_value"),
        pli_icons,
    )
    if ICON_DEFAULT_VALUE_UI in pli_icon_selected:
        pli_from = None
        pli_to = 1.01
    else:
        pli_from, pli_to, ico_to_write_pli = convert_pli_value_to_icon(
            PLI_DESC_ICONS2VALUE[pli_icon_selected] - 0.001
        )

    cat_www_exp = news_config_container.expander(
        LanguageTranslator.translate(code_name="news_stream_filter_news_sites"),
        expanded=False,
    )
    pages_checkboxes = add_category_and_pages_ui(
        categories_with_pages=categories_with_pages,
        element=cat_www_exp,
        info_creator_window=False,
    )

    if ICON_NEWS_POLARITY_3C_A in which_polarity3c:
        which_polarity3c = "ambivalent"
    elif ICON_NEWS_POLARITY_3C_P in which_polarity3c:
        which_polarity3c = "positive"
    elif ICON_NEWS_POLARITY_3C_N in which_polarity3c:
        which_polarity3c = "negative"
    else:
        which_polarity3c = None

    options = {
        "news_in_category": news_in_category,
        "sort_news_by": sort_date_by,
        "filter_pages": pages_checkboxes,
        "polarity_3c": which_polarity3c,
        "pli_from": pli_from,
        "pli_to": pli_to,
        "admin": {"show_only_with_message": show_only_with_message},
    }

    return options


def convert_pli_value_to_icon(pli_value) -> (float, float, str):
    prev_pli_conv = {"below_value": 0, "icon": ICON_NOT_SET_NEWS_INFO}
    for pli_conv in DEF_PLI_VALUE_TO_ICON:
        if pli_value < pli_conv["below_value"]:
            return (
                prev_pli_conv["below_value"],
                pli_conv["below_value"],
                pli_conv["icon"],
            )
        prev_pli_conv = pli_conv
    return 0, 1.0, ICON_NEWS_PLI_GOOD


def prepare_admin_messages_to_article(
    article_txt: str,
    sim_to_original_article: float,
    num_of_generated_news: int,
    language: str | None,
    min_article_len: int,
):
    messages = []
    if sim_to_original_article is not None:
        if sim_to_original_article < 0.401:
            messages.append(
                {
                    "type": "error",
                    "txt": LanguageTranslator.translate(
                        code_name="news_stream_admin_msg_401"
                    ),
                }
            )
        elif sim_to_original_article < 0.501:
            messages.append(
                {
                    "type": "warning",
                    "txt": LanguageTranslator.translate(
                        code_name="news_stream_admin_msg_501"
                    ),
                }
            )
        elif sim_to_original_article < 0.635:
            messages.append(
                {
                    "type": "info",
                    "txt": LanguageTranslator.translate(
                        code_name="news_stream_admin_msg_635"
                    ),
                }
            )
        elif sim_to_original_article > 0.9:
            messages.append(
                {
                    "type": "error",
                    "txt": LanguageTranslator.translate(
                        code_name="news_stream_admin_msg_plag"
                    ),
                }
            )

    if len(article_txt) < min_article_len:
        messages.append(
            {
                "type": "warning",
                "txt": LanguageTranslator.translate(
                    code_name="news_stream_admin_msg_short"
                ).replace("{min_article_len}", str(min_article_len)),
            }
        )

    if num_of_generated_news > 2:
        messages.append(
            {
                "type": "error",
                "txt": LanguageTranslator.translate(
                    code_name="news_stream_admin_msg_num_gen"
                ).replace("{num_of_generated_news}", str(num_of_generated_news)),
            }
        )
    elif num_of_generated_news > 1:
        messages.append(
            {
                "type": "warning",
                "txt": LanguageTranslator.translate(
                    code_name="news_stream_admin_msg_num_gen"
                ).replace("{num_of_generated_news}", str(num_of_generated_news)),
            }
        )

    if language is not None and language != "pl":
        messages.append(
            {
                "type": "error",
                "txt": LanguageTranslator.translate(
                    code_name="news_stream_admin_msg_lang"
                ).replace("{language}", language),
            }
        )

    if article_txt.strip()[-1] not in [".", "!", "?", ";"]:
        messages.append(
            {
                "type": "info",
                "txt": LanguageTranslator.translate(
                    code_name="news_stream_admin_msg_not_full_article"
                ),
            }
        )

    return messages


def convert_to_lang_icon(language: str | None) -> str:
    if language is None:
        return ICON_NOT_SET_NEWS_INFO
    elif language == "en":
        return ICON_FLAG_EN_LANG
    elif language == "pl":
        return ICON_FLAG_PL_LANG
    elif language == "fr":
        return ICON_FLAG_FR_LANG
    elif language == "ru":
        return ICON_FLAG_RU_LANG
    elif language == "ua":
        return ICON_FLAG_UA_LANG
    elif language == "de":
        return ICON_FLAG_DE_LANG
    return ICON_DEFAULT_VALUE_UI


def add_news_to_public_news_stream(
    news_list,
    user_token: str | None = None,
    token_info: dict | None = None,
    publ_news_api: PublicNewsStreamAPI | None = None,
    auth_api: PlaygroundAuthenticationAPI | None = None,
    admin_opts: dict | None = None,
):
    if admin_opts is None:
        admin_opts = {}
    show_only_with_message = admin_opts.get("show_only_with_message", False)
    for news in news_list:
        news_id = news["id"]
        news_text = news["generated_text"]
        model_name = news["model_used_to_generate_news"]
        polarity_3c = news["polarity_3c"]
        pli_value = news["pli_value"]
        show_news_admin_msg = news["show_admin_message"]
        generation_time = news["generation_time"]
        sim_to_original_article = news["similarity_to_original"]
        when_generated = news["when_generated"]
        news_url = news["news_sub_page"]["news_url"]
        num_of_generated_news = news["news_sub_page"]["num_of_generated_news"]

        news_language_ico = convert_to_lang_icon(news["language"])
        main_page_language_ico = convert_to_lang_icon(news["main_page_language"])

        if when_generated is not None:
            when_generated = datetime.datetime.strptime(
                when_generated, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            when_generated = when_generated.strftime("%Y-%m-%d %H:%M:%S")

        news_container = None
        action_on_news = None
        admin_news_id = None
        user_news_text = prepare_news_to_user(news_text=news_text)
        if (
            user_token is not None
            and len(user_token.strip())
            and publ_news_api is not None
        ):
            admin_news_id = news_id
            hide_key = f"hide_{news_id}"
            generate_key = f"generate_{news_id}"
            hide_admin_msg_key = f"hide_admin_msg_{news_id}"

            if show_news_admin_msg:
                msg_to_news = prepare_admin_messages_to_article(
                    article_txt=user_news_text,
                    sim_to_original_article=sim_to_original_article,
                    num_of_generated_news=num_of_generated_news,
                    language=news["language"],
                    min_article_len=MIN_ARTICLE_LEN,
                )
            else:
                msg_to_news = []

            if show_only_with_message and not len(msg_to_news):
                continue

            news_container = st.container(border=True)
            for message in msg_to_news:
                if message["type"] == "warning":
                    news_container.warning(message["txt"])
                elif message["type"] == "error":
                    news_container.error(message["txt"])
                elif message["type"] == "info":
                    news_container.info(message["txt"])

            hide_toggle = news_container.toggle(
                LanguageTranslator.translate(
                    code_name="news_stream_admin_hide_news"
                ),
                key=hide_key,
            )
            if hide_toggle:
                action_on_news = "hide"

            generate_toggle = news_container.toggle(
                LanguageTranslator.translate(
                    code_name="news_stream_admin_re_gen_news"
                ),
                key=generate_key,
            )
            if generate_toggle:
                action_on_news = "regenerate"

            if len(msg_to_news):
                hide_admin_msg = news_container.toggle(
                    LanguageTranslator.translate(
                        code_name="news_stream_admin_hide_msg"
                    ),
                    key=hide_admin_msg_key,
                )
                if hide_admin_msg:
                    action_on_news = "hide_admin_msg"

            if action_on_news is not None:
                response = publ_news_api.do_news_option(
                    news_id=news_id,
                    action=action_on_news,
                    token_str=user_token,
                    token_info=token_info,
                    auth_api=auth_api,
                )
                ser_response_exp = news_container.expander(
                    LanguageTranslator.translate(
                        code_name="news_stream_admin_serv_resp_exp"
                    )
                )
                if "response" in response:
                    response = response["response"]
                ser_response_exp.write(response)
                continue
        else:
            # If user is not logged
            msg_to_news = prepare_admin_messages_to_article(
                article_txt=user_news_text,
                sim_to_original_article=sim_to_original_article,
                num_of_generated_news=num_of_generated_news,
                language=news["language"],
                min_article_len=MIN_ARTICLE_LEN,
            )
            if len(msg_to_news):
                continue

        if news_container is None:
            news_container = st.container(border=True)

        ico_to_write_p_3c = ICON_NOT_SET_NEWS_INFO
        if polarity_3c is not None:
            ico_to_write_p_3c = ICON_NEWS_POLARITY_3C_A
            if polarity_3c == "negative":
                ico_to_write_p_3c = ICON_NEWS_POLARITY_3C_N
            elif polarity_3c == "positive":
                ico_to_write_p_3c = ICON_NEWS_POLARITY_3C_P

        pli_from_value, pli_to_value = None, 1.0
        ico_to_write_pli = ICON_NOT_SET_NEWS_INFO
        if pli_value is not None:
            pli_from_value, pli_to_value, ico_to_write_pli = (
                convert_pli_value_to_icon(pli_value)
            )

        news_container.write(
            f"Info: `3c:`{ico_to_write_p_3c} `pli:`{ico_to_write_pli}"
        )

        news_container.write(user_news_text)

        news_expander = news_container.expander(
            LanguageTranslator.translate(code_name="news_stream_news_info_exp")
        )

        if admin_news_id is not None:
            news_expander.write(
                LanguageTranslator.translate(
                    code_name="news_stream_news_info_id"
                ).replace("{admin_news_id}", str(admin_news_id))
            )
            news_expander.write(
                LanguageTranslator.translate(
                    code_name="news_stream_news_sim_to_orig"
                ).replace("{sim_to_original_article}", str(sim_to_original_article))
            )
            news_expander.write(
                LanguageTranslator.translate(
                    code_name="news_stream_news_gen_count"
                ).replace("{num_of_generated_news}", str(num_of_generated_news))
            )
        news_expander.write(
            LanguageTranslator.translate(
                code_name="news_stream_news_lang_generated"
            ).replace("{news_language_ico}", news_language_ico)
        )
        news_expander.write(
            LanguageTranslator.translate(
                code_name="news_stream_news_lang_orig"
            ).replace("{main_page_language_ico}", main_page_language_ico)
        )
        news_expander.write(
            LanguageTranslator.translate(code_name="news_stream_news_orig_link")
            + " "
            + news_url
        )
        news_expander.write(
            LanguageTranslator.translate(code_name="news_stream_news_gen_at_date")
            + " "
            + when_generated
        )
        news_expander.write(
            LanguageTranslator.translate(code_name="news_stream_news_used_gen_model")
            + " "
            + model_name
        )
        news_expander.write(
            LanguageTranslator.translate(code_name="news_stream_news_gen_time")
            + " "
            + generation_time
        )

        l_clr_f_n = len(news_text.strip().replace("\n", ""))
        l_clr_g_n = len(user_news_text.strip().replace("\n", ""))
        if l_clr_f_n > l_clr_g_n:
            full_news_text = news_container.expander(
                LanguageTranslator.translate(
                    code_name="news_stream_news_full_article"
                )
            )
            if news_text[-1] not in [".", "?", "!", ";"]:
                news_text += "..."
            full_news_text.write(news_text)


def prepare_news_stream_public_news_tab(
    categories,
    news_in_categories,
    sort_date_by: str,
    number_of_news: int,
    user_token: str | None = None,
    token_info: dict | None = None,
    publ_news_api: PublicNewsStreamAPI | None = None,
    auth_api: PlaygroundAuthenticationAPI | None = None,
    admin_opts: dict | None = None,
    filter_pages: dict | None = None,
):
    """

    :param categories:
    :param news_in_categories:
    :param sort_date_by:
    :param number_of_news:
    :param user_token:
    :param token_info:
    :param publ_news_api:
    :param auth_api:
    :param admin_opts:
    :param filter_pages:
    :return:
    """
    # phr_search_inp_tab, btn_search_tab = st.columns([7, 1])
    # if (
    #     user_token is not None
    #     and len(user_token.strip())
    #     and publ_news_api is not None
    # ):
    #     phrase_to_search = phr_search_inp_tab.text_input(
    #         label="Szukaj",
    #         placeholder=f"Podaj frazę do wyszukania w wybranych stronach (ostatnie 24h)",
    #         max_chars=128,
    #         label_visibility="collapsed",
    #         on_change=None,
    #     )
    #     search_btn = btn_search_tab.button(":mag_right:")
    #     if search_btn:
    #         if len(phrase_to_search.strip()) < 5:
    #             st.error(f"Musisz wpisać frazę do wyszukania (min 5 znaków)!")
    #             # return
    #         elif publ_news_api is not None:
    #             search_n_in_cat = publ_news_api.search_news_in_categories(
    #                 text_to_search=phrase_to_search,
    #                 filter_pages=filter_pages,
    #                 num_of_results=number_of_news,
    #             )
    #             news_in_categories = search_n_in_cat

    c_names = [c for c in categories.keys()]
    c_names_display = [
        categories[c]["category_info"]["display_name"] for c in categories.keys()
    ]
    news_tabs = st.tabs(c_names_display)
    for idx, c_name in enumerate(c_names):
        with news_tabs[idx]:
            st.subheader(categories[c_name]["category_info"]["description"])
            if c_name not in news_in_categories:
                continue
            news_in_cat = news_in_categories[c_name]

            # when_generated
            # Newest are first
            news_in_cat = sorted(
                news_in_cat,
                key=lambda d: d["when_generated"],
                reverse=True,
            )
            if len(news_in_cat) > number_of_news:
                news_in_cat = news_in_cat[:number_of_news]

            if "najstarsze" in sort_date_by.lower():
                news_in_cat = sorted(
                    news_in_cat,
                    key=lambda d: d["when_generated"],
                    reverse=False,
                )

            add_news_to_public_news_stream(
                news_in_cat,
                user_token=user_token,
                token_info=token_info,
                publ_news_api=publ_news_api,
                auth_api=auth_api,
                admin_opts=admin_opts,
            )


def set_session_hash_chat_to_load():
    st.session_state["temp_state_chat_hash_to_load"] = True


def prepare_public_chat(
    generative_model: str,
    generation_options: Dict[str, str],
    conversation_options: Dict[str, str],
    public_conv_with_model: PublicConversationWithModelAPI,
    public_state_options: Dict[str, str],
    rag_search_options: Dict[str, str],
    force_use_rag_supervisor: bool,
):
    chat_window, message_state_window = st.columns([2, 1])

    chat_window_height = 600
    messages = chat_window.container(height=chat_window_height)
    messages_state_opts = message_state_window.container(height=chat_window_height)

    messages_state_container = messages_state_opts.container(
        height=int(chat_window_height * 0.85), border=False
    )

    new_chat_btn = st.sidebar.button(
        LanguageTranslator.translate(code_name="public_chat_button_new_chat")
    )
    if new_chat_btn:
        set_on_change_state()

    SessionConfig.set_session_free_chat_hash(chat_hash=None)
    with st.sidebar.popover(
        LanguageTranslator.translate(code_name="public_chat_load_chat")
    ):
        chat_hash = st.text_input(
            LanguageTranslator.translate(code_name="public_chat_load_chat_hash"),
            on_change=set_session_hash_chat_to_load,
        )
        if (
            "temp_state_chat_hash_to_load" in st.session_state
            and st.session_state["temp_state_chat_hash_to_load"]
        ):
            SessionConfig.set_session_free_chat_hash(chat_hash)
            st.session_state["temp_state_chat_hash_to_load"] = False

    chat_hash_session = SessionConfig.get_session_free_chat_hash()
    if chat_hash_session:
        loaded_chat_id, loaded_chat_history, is_chat_read_only = (
            public_conv_with_model.get_chat_by_hash(
                chat_hash=chat_hash_session,
                model_name=generative_model,
                convert_history_to_session=True,
            )
        )

        if loaded_chat_id is not None and len(loaded_chat_history):
            SessionConfig.set_session_free_chat_chat_id(
                chat_id=loaded_chat_id,
                chat=loaded_chat_history,
                is_chat_read_only=is_chat_read_only,
            )
            messages_state_container.write({"session_chat_id": loaded_chat_id})
        SessionConfig.set_session_free_chat_hash(chat_hash=None)

    chat_history = SessionConfig.get_session_free_chat()
    if chat_history is None:
        chat_history = []

    for chat_msg in chat_history:
        if "user" in chat_msg:
            messages.chat_message("user").write(chat_msg["user"])
        if "assistant" in chat_msg:
            messages.chat_message("assistant").write(chat_msg["assistant"])

    is_chat_read_only = SessionConfig.get_session_free_chat_is_read_only()
    if is_chat_read_only:
        return

    session_chat_id = SessionConfig.get_session_free_chat_id()
    if last_user_msg := chat_window.chat_input(
        LanguageTranslator.translate(code_name="public_chat_ask_bot")
    ):
        messages.chat_message("user").write(last_user_msg)

        if session_chat_id is None:
            resp = public_conv_with_model.new_chat(
                model_name=generative_model,
                generation_options=generation_options,
                public_state_options=public_state_options,
            )
            if "chat" in resp:
                session_chat_id = resp["chat"]["id"]
            else:
                messages_state_container.write(resp)
                return

        messages_state_container.write({"session_chat_id": session_chat_id})

        with messages.status(
            LanguageTranslator.translate(code_name="public_chat_bot_writing")
        ):
            last_user_msg_to_model = last_user_msg
            if force_use_rag_supervisor:
                last_user_msg_to_model = (
                    LanguageTranslator.translate(
                        code_name="public_chat_bot_prompt_question"
                    )
                    + " "
                    + last_user_msg_to_model
                )

            det_conv = ""
            if conversation_options["detailed_explanation"]:
                # detailed
                det_conv = LanguageTranslator.translate(
                    code_name="public_chat_model_detailed_explanation"
                )
            list_command = ""
            if conversation_options["explanation_in_list"]:
                list_command = LanguageTranslator.translate(
                    code_name="public_chat_model_answer_as_list"
                )
            last_user_msg_to_model = (
                f"{last_user_msg_to_model}\n{det_conv} {list_command}".strip()
            )

            assistant_response = public_conv_with_model.add_chat_message(
                chat_id=session_chat_id,
                last_user_msg=last_user_msg_to_model,
                generation_options=generation_options,
                public_state_options=public_state_options,
                model_name=generative_model,
                rag_search_options=rag_search_options,
            )

            if assistant_response is None or not len(assistant_response):
                st.write(public_conv_with_model.last_response)
            elif "status" in assistant_response:
                messages_state_container.error(assistant_response)
            else:
                generation_time = assistant_response["generation_time"]
                messages_state_container.write(
                    LanguageTranslator.translate(
                        code_name="public_chat_model_gen_time"
                    ).replace("{generation_time}", str(generation_time))
                )

                if "last_state" in assistant_response:
                    if assistant_response["last_state"] is not None:
                        messages_state_container.write(
                            assistant_response["last_state"]
                        )

                assistant_response = assistant_response[
                    "generated_assistant_message"
                ]
                messages.chat_message("assistant").write(assistant_response)
                chat_history.append(
                    {"user": last_user_msg, "assistant": assistant_response}
                )
            SessionConfig.set_session_free_chat_chat_id(
                chat=chat_history, chat_id=session_chat_id
            )

    if len(chat_history) and session_chat_id is not None:
        with st.sidebar.popover(
            LanguageTranslator.translate(code_name="public_chat_save_chat")
        ):
            save_as_read_only = st.toggle(
                LanguageTranslator.translate(code_name="public_chat_save_chat_ro"),
                value=True,
            )
            save_chat_btn = st.button(
                LanguageTranslator.translate(
                    code_name="public_chat_btn_save_get_hash"
                )
            )
            if save_chat_btn:
                chat_hash = public_conv_with_model.save_chat(
                    chat_id=session_chat_id,
                    model_name=generative_model,
                    save_as_read_only=save_as_read_only,
                )

                if "chat_hash" in chat_hash:
                    chat_hash = chat_hash["chat_hash"]
                    messages_state_container.info(
                        LanguageTranslator.translate(
                            code_name="public_chat_saved_chat_info"
                        ).replace("{save_as_read_only}", str(save_as_read_only))
                    )
                    messages_state_container.code(chat_hash)
                else:
                    messages_state_container.error(
                        LanguageTranslator.translate(
                            code_name="act_creator_model_error_try_again"
                        )
                    )

    if public_state_options.get("use_rag_supervisor", False):
        show_public_info_about_rag_supervisor_in_news_conversation()


def show_error_status(result):
    st.error(f"Error occurred while processing")
    for err in result["errors"]:
        if "required_params" in err and len(err["required_params"]):
            st.write(err)


def add_single_system_status_info(
    header,
    single_status,
    elem,
    admin_api,
    settings_id,
    token_str,
    token_info,
    auth_api,
    datetime_format="%Y-%m-%dT%H:%M:%S.%fZ",
):
    is_status_doing = single_status["doing"]
    time_offset = datetime.timedelta(hours=1) if True is True else None
    actual_datetime = datetime.datetime.now()
    if time_offset is not None:
        begin_date = (
            datetime.datetime.strptime(single_status["begin_date"], datetime_format)
            + time_offset
            if single_status["begin_date"] is not None
            else None
        )
        end_date = (
            datetime.datetime.strptime(single_status["end_date"], datetime_format)
            + time_offset
            if single_status["end_date"] is not None
            else None
        )
    else:
        begin_date = (
            datetime.datetime.strptime(single_status["begin_date"], datetime_format)
            if single_status["begin_date"] is not None
            else None
        )
        end_date = (
            datetime.datetime.strptime(single_status["end_date"], datetime_format)
            if single_status["end_date"] is not None
            else None
        )

    show_header = header
    status_container = elem.container(border=True)
    status_container.markdown(f"**{show_header}**")
    if is_status_doing:
        max_time_doing_h = 1.1
        status_container.warning(
            LanguageTranslator.translate(code_name="admin_panel_header").replace(
                "{show_header}", show_header
            )
        )
        time_delta = actual_datetime - begin_date
        if time_delta.seconds / 3600 > max_time_doing_h:
            status_container.error(
                LanguageTranslator.translate(
                    code_name="admin_panel_is_away"
                ).replace("{show_header}", show_header)
            )
    else:
        status_container.success(
            LanguageTranslator.translate(
                code_name="admin_panel_waiting_to_job"
            ).replace("{show_header}", show_header)
        )

    # Begin datetime
    if begin_date is not None:
        day_container, time_container = status_container.columns(2)
        day_container.date_input(
            LanguageTranslator.translate(code_name="admin_panel_job_last_run_d"),
            begin_date,
            key=f"d_b_{header}",
            disabled=True,
        )
        time_container.time_input(
            LanguageTranslator.translate(code_name="admin_panel_job_last_run_h"),
            begin_date,
            key=f"t_b_{header}",
            disabled=True,
        )
    else:
        status_container.info(
            LanguageTranslator.translate(
                code_name="admin_panel_job_newer_run"
            ).replace("{show_header}", show_header)
        )

    # End datetime
    if end_date is not None:
        day_container, time_container = status_container.columns(2)
        day_container.date_input(
            LanguageTranslator.translate(code_name="admin_panel_job_last_end_d"),
            end_date,
            key=f"d_e_{header}",
            disabled=True,
        )
        time_container.time_input(
            LanguageTranslator.translate(code_name="admin_panel_job_last_end_h"),
            end_date,
            key=f"t_e_{header}",
            disabled=True,
        )
    else:
        status_container.info(
            LanguageTranslator.translate(
                code_name="admin_panel_job_newer_done"
            ).replace("{show_header}", show_header)
        )

    # Restart button
    if status_container.button(
        LanguageTranslator.translate(code_name="admin_panel_job_reset"),
        key=f"btn_restart_{header}",
    ):
        response = admin_api.do_admin_action_on_module(
            settings_id=settings_id,
            module=header,
            action="restart",
            token_str=token_str,
            token_info=token_info,
            auth_api=auth_api,
        )
        if "status" in response and response["status"]:
            status_container.info(
                LanguageTranslator.translate(
                    code_name="admin_panel_job_restarted"
                ).replace("{show_header}", show_header)
            )
        else:
            status_container.error(response)


def add_stat_to_elem(elem_to_add_stat, news_statistics, admin_stats: bool = False):
    stats_datetime = news_statistics["stats_datetime"]
    elem_to_add_stat.markdown(
        LanguageTranslator.translate(code_name="statistics_date_of_stats")
        + " "
        + str(stats_datetime)
    )

    stats_categories = news_statistics["news_stats"]
    polarity_stats = news_statistics["polarity_stats"]

    categories = [c for c in stats_categories.keys()]
    cat_stat_tabs = elem_to_add_stat.tabs(categories)
    for idx in range(len(categories)):
        cat_name = categories[idx]
        add_single_category_stats(
            category=cat_name,
            pages_stats=stats_categories[cat_name],
            polarity_stats=polarity_stats[cat_name],
            elem_to_add_stats=cat_stat_tabs[idx],
            are_admin_stats=admin_stats,
        )


def add_single_category_stats(
    category, pages_stats, polarity_stats, elem_to_add_stats, are_admin_stats
):
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    table_stats_elem, pie_p_d_elem = elem_to_add_stats.columns([1, 1])
    # Dataframe table
    stats_df = pd.DataFrame(pages_stats)
    if not are_admin_stats:
        stats_df = stats_df.drop(
            labels=[
                "subpages_count",
                "number_of_hidden_news",
                "news_count",
                "perc_of_hidden_news",
                "perc_of_visible_news",
            ]
        )
    stats_df = stats_df.transpose()

    if not are_admin_stats:
        stats_df = stats_df.loc[
            :,
            [
                "news_per_day",
                "number_of_visible_news",
                "last_crawling_date",
                "first_crawling_date",
            ],
        ]

        stats_df.rename(
            columns={
                "number_of_visible_news": LanguageTranslator.translate(
                    code_name="statistics_tab_num_vis_news"
                ),
                "news_per_day": LanguageTranslator.translate(
                    code_name="statistics_tab_news_per_day"
                ),
                "last_crawling_date": LanguageTranslator.translate(
                    code_name="statistics_tab_last_crawling_date"
                ),
                "first_crawling_date": LanguageTranslator.translate(
                    code_name="statistics_tab_first_crawling_date"
                ),
            },
            inplace=True,
        )

    table_stats_elem.dataframe(stats_df)

    # Number of news per day
    news_per_day_dataset = convert_admin_pages_stats_news_p_day(
        pages_stats=pages_stats
    )
    per_day_news_fig = px.pie(
        news_per_day_dataset,
        values="news_per_day",
        names="url",
        title=LanguageTranslator.translate(
            code_name="statistics_news_per_24h_percentage"
        ),
    )
    pie_p_d_elem.plotly_chart(per_day_news_fig, theme="streamlit")

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # Polarity chart
    p_3c_dataset, p_3c_dataset_perc = convert_admin_pages_stats_to_polarity_3c(
        polarity_stats=polarity_stats
    )

    p_3c_fig = px.bar(
        p_3c_dataset,
        x="url",
        y="count",
        color="polarity_3c",
        color_discrete_map={
            "positive": "green",
            "negative": "red",
            "ambivalent": "gray",
        },
        title=LanguageTranslator.translate(
            code_name="statistics_news_polarity_3c_hist_count"
        ).replace("{category}", category),
    )
    elem_to_add_stats.plotly_chart(p_3c_fig, theme="streamlit")

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    p_3c_fig_perc = px.bar(
        p_3c_dataset_perc,
        x="url",
        y="percentage",
        color="polarity_3c",
        color_discrete_map={
            "positive": "green",
            "negative": "red",
            "ambivalent": "gray",
        },
        title=LanguageTranslator.translate(
            code_name="statistics_news_polarity_3c_hist_perc"
        ).replace("{category}", category),
    )
    elem_to_add_stats.plotly_chart(p_3c_fig_perc, theme="streamlit")


def show_admin_window(
    token_info: dict,
    token_str: str,
    system_status: Dict,
    admin_api: PlaygroundAdministrationAPI,
    auth_api: PlaygroundAuthenticationAPI,
    max_statuses_in_row,
):
    if "settings" not in system_status:
        return

    # System status / system info
    settings_id = system_status["settings"]
    exp_system_status = st.expander(
        LanguageTranslator.translate(code_name="admin_window_status_exp").replace(
            "{settings_id}", str(settings_id)
        ),
        expanded=True,
    )
    if "status" in system_status:
        for single_status in system_status["status"]:
            num_of_statuses = len(single_status)

            num_of_rows = num_of_statuses // max_statuses_in_row + (
                1 if (num_of_statuses % max_statuses_in_row) else 0
            )
            containers = [
                exp_system_status.container(border=False) for _ in range(num_of_rows)
            ]
            all_stats_columns = []
            for c in containers:
                all_stats_columns.extend(c.columns(max_statuses_in_row))

            idx = 0
            for status_name, stats in single_status.items():
                add_single_system_status_info(
                    header=status_name,
                    single_status=stats,
                    elem=all_stats_columns[idx],
                    admin_api=admin_api,
                    settings_id=settings_id,
                    token_str=token_str,
                    token_info=token_info,
                    auth_api=auth_api,
                )
                idx += 1
    else:
        exp_system_status.error(
            LanguageTranslator.translate(
                code_name="admin_window_error_retrieve_status"
            )
        )

    # News/categories statistics
    exp_news_stats = st.expander(
        LanguageTranslator.translate(code_name="admin_window_stats_cat_news")
    )

    if exp_news_stats.button(
        LanguageTranslator.translate(code_name="admin_window_btn_gen_stats")
    ):
        with st.spinner(
            LanguageTranslator.translate(code_name="admin_window_gen_in_progress")
        ):
            news_statistics = admin_api.get_news_statistics(
                token_str=token_str,
                auth_api=auth_api,
                token_info=token_info,
                settings_id=settings_id,
            )
            if "news_stats" in news_statistics:
                add_stat_to_elem(
                    elem_to_add_stat=exp_news_stats,
                    news_statistics=news_statistics,
                    admin_stats=True,
                )
            else:
                exp_news_stats.error(
                    LanguageTranslator.translate(
                        code_name="admin_window_error_gen_stats_retrieve"
                    )
                )

    # Show token
    exp_token = st.expander("Token")
    if token_info is not None and len(token_info):
        exp_token.write(token_info)
    else:
        exp_token.write(token_str)


def show_stats_window(publ_api: PublicNewsStreamAPI, settings_id):
    news_statistics = publ_api.get_news_statistics(
        settings_id=settings_id, get_last_stats=True
    )

    exp_news_stats = st.expander(
        LanguageTranslator.translate(code_name="statistics_connected_with_news"),
        expanded=True,
    )
    if "news_stats" in news_statistics:
        add_stat_to_elem(
            elem_to_add_stat=exp_news_stats,
            news_statistics=news_statistics,
            admin_stats=False,
        )


def insert_site_logo():
    st.logo(
        "resources/images/radlab-logo-new-scaled-circle.png",
        icon_image="resources/images/radlab-logo-new-scaled-circle.png",
        link="https://radlab.dev",
    )


def insert_language_choose():
    current_lang = SessionConfig.get_session_ui_language() or DEFAULT_LANGUAGE
    lang_codes = list(_LanguageDefinitions.LANGUAGES.keys())
    if current_lang not in lang_codes:
        raise ValueError(f"Unknown language code {current_lang}")

    selected_lang = st.sidebar.selectbox(
        label=LanguageTranslator.translate(code_name="language_set_interface_lang"),
        options=lang_codes,
        index=lang_codes.index(current_lang),
        format_func=lambda k: _LanguageDefinitions.LANGUAGES[k],
    )
    st.sidebar.divider()

    if selected_lang != current_lang:
        SessionConfig.set_session_ui_language(selected_lang)
        st.rerun()


def initialize_page():
    SessionConfig.init_session_state_if_needed()
    if SessionConfig.get_session_ui_language() is None:
        SessionConfig.set_session_ui_language(language=DEFAULT_LANGUAGE)

    insert_site_logo()
    insert_language_choose()
