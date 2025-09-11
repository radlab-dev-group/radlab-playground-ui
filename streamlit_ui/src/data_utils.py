import json

import pandas as pd


def convert_admin_pages_stats_to_polarity_3c(polarity_stats: dict) -> (list, list):
    pages_polarity = []
    pages_polarity_perc = []
    for page_www_url, page_data in polarity_stats.items():
        examples_count = sum(page_data["3c"].values())
        page_stats = page_data["3c"]
        for polarity, polarity_count in page_stats.items():
            pages_polarity.append(
                {
                    "url": page_www_url,
                    "polarity_3c": polarity,
                    "count": polarity_count,
                }
            )
            pages_polarity_perc.append(
                {
                    "url": page_www_url,
                    "polarity_3c": polarity,
                    "percentage": polarity_count / examples_count,
                }
            )

    pages_polarity = pd.DataFrame(pages_polarity)
    return pages_polarity, pages_polarity_perc


def convert_admin_pages_stats_news_p_day(pages_stats):
    p_d_stats = []
    for url, stats in pages_stats.items():
        p_d_stats.append(
            {
                "url": url,
                "news_per_day": stats["news_per_day"],
            }
        )
    p_d_stats_df = pd.DataFrame(p_d_stats)
    return p_d_stats_df


def prepare_news_to_user(news_text: str, news_length_chars: int = 200) -> str:
    user_news = ""
    for spl_news in news_text.split("\n"):
        if len(spl_news.strip()):
            user_news += spl_news
        if len(user_news) >= news_length_chars:
            break
        user_news += "\n\n"
    return user_news.strip()
