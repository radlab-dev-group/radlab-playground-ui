import datetime

import pandas as pd
import streamlit as st
import plotly.express as px

from src.language import LanguageTranslator


def add_menu(is_logged: bool = False):
    actual = datetime.date.today() - datetime.timedelta(days=1)
    min_value = datetime.date(year=2025, month=1, day=1)
    if is_logged:
        min_value = datetime.date(year=2024, month=1, day=1)

    menu_container = st.container(border=True)

    selected_day = menu_container.date_input(
        label=LanguageTranslator.translate(
            code_name="news_browser_select_day_label"
        ),
        value=actual,
        min_value=min_value,
        max_value=actual,
    )
    settings = {"selected_day": selected_day}
    return settings, menu_container


def add_info_to_selected_proposition(info: dict):
    general_info_cont = st.sidebar.expander(
        LanguageTranslator.translate(code_name="news_browser_what_is"),
        expanded=False,
    )

    i_cl = info["clustering"]
    general_info_cont.info(
        LanguageTranslator.translate(code_name="news_browser_description_cont")
        .replace("{info['day_to_summary']}", info["day_to_summary"])
        .replace("{info['when_generated']}", info["when_generated"])
        .replace("{i_cl['clustering_method']}", i_cl["clustering_method"])
        .replace("{i_cl['reducer_method']}", i_cl["reducer_method"])
        .replace("{i_cl['reducer_optimizer']}", i_cl["reducer_optimizer"])
        .replace("{i_cl['genai_labels_model']}", i_cl["genai_labels_model"])
    )


@st.dialog(
    LanguageTranslator.translate(code_name="news_browser_st_dialog_connected"),
    width="large",
)
def show_similar_day(day_str, similarities):
    st.title(
        LanguageTranslator.translate(code_name="news_browser_sim_day_title")
        .replace("{day_str}", day_str)
        .replace("{len(similarities)}", str(len(similarities)))
    )

    for sim_article in similarities:
        similarity_value = sim_article["similarity_value"]
        similarity_metric = sim_article["similarity_metric"]

        target = sim_article["target"]
        label_str = target["label_str"]
        article_text = target["article_text"]
        news_urls = target["news_urls"]

        sim_art_short_cont = st.container(border=True)
        sim_art_short_cont.write("## " + label_str)

        sim_art_short_cont.write(f"{article_text}")

        sim_art_short_exp = sim_art_short_cont.expander(
            LanguageTranslator.translate(
                code_name="news_browser_expand_for_more_info"
            )
        )
        sim_art_short_exp.write(
            LanguageTranslator.translate(code_name="news_browser_similarity")
            .replace("{similarity_metric}", similarity_metric)
            .replace("{similarity_value}", str(similarity_value))
        )

        sim_art_short_exp.data_editor(
            pd.DataFrame({"url": news_urls}),
            column_config={
                "url": st.column_config.LinkColumn(
                    LanguageTranslator.translate(
                        code_name="news_browser_summary_header"
                    ),
                    help=LanguageTranslator.translate(
                        code_name="news_browser_summary_header_help"
                    ),
                )
            },
            hide_index=True,
        )

        st.divider()


def handle_similar_prev_next(cluster, container):
    if not cluster.get("has_next_similarity", False) and not cluster.get(
        "has_prev_similarity", False
    ):
        return

    similarities = cluster.get("similarity", {})
    if not len(similarities):
        return

    days_exp = container.expander(
        LanguageTranslator.translate(code_name="news_browser_similar_information")
    )

    date2btn = {}
    for date_sim, sim_at_day in similarities.items():
        date2btn[date_sim] = days_exp.button(
            LanguageTranslator.translate(
                code_name="news_browser_similar_information_day"
            ).replace("{date_sim}", date_sim),
            key=f"k_{date_sim}",
        )

    for date_sim, btn in date2btn.items():
        if btn:
            show_similar_day(day_str=date_sim, similarities=similarities[date_sim])
            break


def add_single_cluster_stats(
    cluster: dict,
    stats_container,
    buttons_container,
    is_admin_logged: bool,
    num_of_all_texts: int,
    cluster_label_str: str,
    day: datetime.date,
):
    stats = cluster["stats"]
    news_urls = cluster["news_urls"]
    sample_news_urls = cluster["sample"]["news_urls"]

    if is_admin_logged:
        pass

    handle_similar_prev_next(cluster=cluster, container=buttons_container)

    stats_container.write(
        LanguageTranslator.translate(code_name="news_browser_stats_info")
    )

    stats_container.markdown(
        LanguageTranslator.translate(code_name="news_browser_stats_info_body")
        .replace("{cluster_label_str}", cluster_label_str)
        .replace("{day}", str(day))
        .replace("{num_of_all_texts}", str(num_of_all_texts))
        .replace("{stats['num_of_texts']}", str(stats["num_of_texts"]))
        .replace("{len(sample_news_urls)}", str(len(sample_news_urls)))
        .replace("{stats['pli_value']}", str(stats["pli_value"]))
    )

    web_authors_tab, pol_3c_tab, sites_tab = stats_container.tabs(
        [
            LanguageTranslator.translate(
                code_name="news_browser_stats_info_stat_provider"
            ),
            LanguageTranslator.translate(
                code_name="news_browser_stats_info_stat_polar_3c"
            ),
            LanguageTranslator.translate(
                code_name="news_browser_stats_info_stat_articles"
            ),
        ]
    )
    # Sources
    all_sources_freq = stats["source"]
    pie_all_sources_freq = [
        {"url": k, "news_count": v} for k, v in all_sources_freq.items()
    ]
    pie_all_sources_freq_fig = px.pie(
        pie_all_sources_freq,
        values="news_count",
        names="url",
        title=LanguageTranslator.translate(
            code_name="news_browser_stats_info_stat_web_in_info"
        ),
    )
    web_authors_tab.plotly_chart(pie_all_sources_freq_fig, theme="streamlit")

    # Polarity
    polarity_3c = stats["polarity_3c"]
    pie_polarity_3c = [
        {"polarity": k, "news_count": v} for k, v in polarity_3c.items()
    ]
    pie_polarity_3c_fig = px.pie(
        pie_polarity_3c,
        values="news_count",
        names="polarity",
        title=LanguageTranslator.translate(
            code_name="news_browser_stats_info_stat_web_3c"
        ),
        color="polarity",
        color_discrete_map={
            "negative": "red",
            "positive": "green",
            "ambivalent": "gray",
        },
    )
    pol_3c_tab.plotly_chart(pie_polarity_3c_fig, theme="streamlit")

    # Info about connected urls
    sites_sample_tab, sites_all_tab = sites_tab.tabs(
        [
            LanguageTranslator.translate(
                code_name="news_browser_link_to_summary_articles"
            ),
            LanguageTranslator.translate(
                code_name="news_browser_link_to_connected_articles"
            ),
        ]
    )
    news_summary_header = LanguageTranslator.translate(
        code_name="news_browser_link_to_source_info"
    )
    #   - all connected sites
    news_df = pd.DataFrame({"url": news_urls})
    sites_all_tab.data_editor(
        news_df,
        column_config={
            "url": st.column_config.LinkColumn(
                news_summary_header,
                help=LanguageTranslator.translate(
                    code_name="news_browser_link_to_original_article"
                ),
            )
        },
        hide_index=True,
    )
    #   - sample connected sites
    # sample_news_urls = list(set(sample_news_urls))
    sample_news_df = pd.DataFrame({"url": sample_news_urls})
    sites_sample_tab.data_editor(
        sample_news_df,
        column_config={
            "url": st.column_config.LinkColumn(
                news_summary_header,
                help=LanguageTranslator.translate(
                    code_name="news_browser_link_to_original_article"
                ),
            )
        },
        hide_index=True,
    )


def add_clusters_to_selected_proposition(
    clusters: list, day: datetime.date, is_admin_logged: bool, menu_container
):
    num_of_texts = 0
    for c in clusters:
        num_of_texts += c["stats"]["num_of_texts"]

    cluster_labels = [c["label_str"].strip() for c in clusters]
    cluster_labels_idx = [
        {"id": idx, "label_str": label} for idx, label in (enumerate(cluster_labels))
    ]
    options = [(c["label_str"].strip(), i) for i, c in enumerate(cluster_labels_idx)]
    selected_option = menu_container.selectbox(
        LanguageTranslator.translate(
            code_name="news_browser_stats_select_information"
        ),
        options,
        format_func=lambda x: x[0],
        index=0,
    )

    cluster_idx = selected_option[1]
    cluster = clusters[cluster_idx]

    clusters_cont = st.container(border=False)
    art_col, stats_col = clusters_cont.columns([3, 2])
    # Article text
    art_col.write(cluster["article_text"])
    # Article stats
    buttons_container = stats_col.container(border=False)
    stats_container = stats_col.container(border=True)

    add_single_cluster_stats(
        cluster=cluster,
        stats_container=stats_container,
        buttons_container=buttons_container,
        is_admin_logged=is_admin_logged,
        num_of_all_texts=num_of_texts,
        cluster_label_str=cluster_labels[cluster_idx],
        day=day,
    )


def show_summaries_for_day(
    day: datetime.date,
    summaries: list or None,
    summary_number: int,
    menu_container,
    is_admin_logged: bool,
):
    if summaries is None or not len(summaries):
        st.info(
            LanguageTranslator.translate(
                code_name="news_browser_no_summaries_for_day"
            )
        )
        return

    if summary_number > len(summaries):
        LanguageTranslator.translate(
            code_name="news_browser_no_summaries_for_day_and_prop"
        )
        return

    summary = summaries[summary_number]

    # Info
    add_info_to_selected_proposition(info=summary["info"])

    # Clusters
    add_clusters_to_selected_proposition(
        clusters=summary["clusters"],
        day=day,
        is_admin_logged=is_admin_logged,
        menu_container=menu_container,
    )


def select_which_summary(summaries: list, menu_container) -> int:
    summary_number = menu_container.selectbox(
        label=LanguageTranslator.translate(
            code_name="news_browser_many_propositions"
        ),
        index=0,
        options=[i for i in range(len(summaries))],
        placeholder=LanguageTranslator.translate(
            code_name="news_browser_many_propositions_placeholder"
        ),
    )
    return summary_number
