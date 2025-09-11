import plotly.express as px

from typing import List, Dict

from src.language import LanguageTranslator
from src.api_public import PublicNewsStreamAPI


def call_search_api_and_show_result(
    user_query_str: str,
    query_rag_column,
    publ_news_api: PublicNewsStreamAPI,
    news_options: dict,
    categories_sorted: List[str],
    num_of_results: int,
    last_days: int,
) -> (Dict, int):
    search_result_container = query_rag_column.container(border=False)

    if num_of_results is None or num_of_results == 0:
        if last_days == 1:
            num_of_results = 7
        elif last_days < 7:
            num_of_results = 9
        else:
            num_of_results = 12

    sse_search_response = publ_news_api.search_news_in_categories(
        text_to_search=user_query_str,
        filter_pages=news_options["filter_pages"],
        num_of_results=num_of_results,
        last_days=last_days,
    )

    if "search_result" not in sse_search_response:
        return {}, None

    search_n_in_cat = sse_search_response["search_result"]
    query_response_id = sse_search_response["query_response_id"]

    add_search_results_to_container(
        search_in_category=search_n_in_cat,
        search_result_container=search_result_container,
        categories_sorted=categories_sorted,
    )

    return search_n_in_cat, query_response_id


def add_search_results_to_container(
    search_in_category,
    search_result_container,
    categories_sorted: List[str],
):
    category_to_res = {}
    polarity_3c = {}
    for c_name, c_results in search_in_category.items():
        category_to_res[c_name] = []
        for result in c_results:
            category_to_res[c_name].append(result)
            p3c_class = result["polarity_3c"]
            if p3c_class is not None:
                if p3c_class not in polarity_3c:
                    polarity_3c[p3c_class] = 0
                polarity_3c[p3c_class] += 1
    if len(polarity_3c):
        show_polarity_chart(
            search_result_container=search_result_container, polarity_3c=polarity_3c
        )

    if len(category_to_res):
        show_result_urls(
            search_result_container=search_result_container,
            category_to_res=category_to_res,
            categories_sorted=categories_sorted,
        )


def show_result_urls(
    search_result_container,
    category_to_res: dict,
    categories_sorted: List[str],
):
    search_expander = search_result_container.expander(
        LanguageTranslator.translate(code_name="list_of_found_news")
    )

    tab_names = []
    for c_name in categories_sorted:
        if c_name in category_to_res:
            tab_names.append(c_name)

    tabs_category = search_expander.tabs(tab_names)
    for tab_name, tab in zip(tab_names, tabs_category):
        for idx, news_info in enumerate(category_to_res[tab_name]):
            r_container = tab.container(border=True)

            url = news_info["news_sub_page"]["news_url"]
            date_gen = news_info["news_sub_page"]["when_crawled"].split(".")[0]
            date_gen = date_gen.replace("T", " ")

            sample_text = news_info["generated_text"].replace("\n", " ")[:200]
            r_container.write(f"**{date_gen}**: {url}")
            r_container.write(f"> {sample_text} (...)")


def show_polarity_chart(search_result_container, polarity_3c: dict):
    all_c_sum = sum(polarity_3c.values())
    if all_c_sum < 1:
        return

    p_3c_dataset_perc = []
    for c, v in polarity_3c.items():
        p_3c_dataset_perc.append({"polarity_3c": c, "percentage": v / all_c_sum})

    p_3c_fig_perc = px.bar(
        p_3c_dataset_perc,
        x="polarity_3c",
        y="percentage",
        color="polarity_3c",
        color_discrete_map={
            "positive": "green",
            "negative": "red",
            "ambivalent": "gray",
        },
        title=LanguageTranslator.translate(
            code_name="list_of_found_news_pol_3c_perc"
        ),
    )

    search_expander = search_result_container.expander(
        LanguageTranslator.translate(code_name="list_of_found_news_pol_3c"),
        expanded=True,
    )
    search_expander.plotly_chart(p_3c_fig_perc, theme="streamlit")
