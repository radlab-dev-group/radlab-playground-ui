from src.env_utils import bool_env_value


DEFAULT_LANGUAGE = "pl"
UI_LANG_DEFAULT_DEFINITION_FILE = "resources/language/ui_lang_def.xlsx"


SSL_CONNECTION = bool_env_value("STREAMLIT_SSL_CONNECTION")
RUN_SERVER_LOCALHOST = bool_env_value("STREAMLIT_RUN_SERVER_LOCALHOST")


DEFAULT_UI_CONFIG_PATH = "resources/configs/ui-configuration.json"
DEFAULT_ADMIN_UI_STATUSES_IN_ROW = 4

# Default UI value icon
ICON_DEFAULT_VALUE_UI = "🪐"

# Icons connected with news
ICON_NOT_SET_NEWS_INFO = "▪️"

ICON_NEWS_POLARITY_3C_P = "🤩"
ICON_NEWS_POLARITY_3C_N = "🤬"
ICON_NEWS_POLARITY_3C_A = "🤨"

ICON_FLAG_PL_LANG = "🇵🇱"
ICON_FLAG_EN_LANG = "🇺🇸"
ICON_FLAG_FR_LANG = "🇫🇷"
ICON_FLAG_RU_LANG = "🇷🇺"
ICON_FLAG_UA_LANG = "🇺🇦"
ICON_FLAG_DE_LANG = "🇩🇪"

ICON_NEWS_PLI_BAD = ":red_circle:"
ICON_NEWS_PLI_NORM = ":large_yellow_circle:"
ICON_NEWS_PLI_GOOD = ":large_green_circle:"

MIN_ARTICLE_LEN = 130

# Definitions used while translation, the single text occurrence
# will be changed to its proper definition e.g. proper icon
REPLACE_FOR_TRANSLATIONS = {
    "{ICON_DEFAULT_VALUE_UI}": ICON_DEFAULT_VALUE_UI,
    "{ICON_NOT_SET_NEWS_INFO}": ICON_NOT_SET_NEWS_INFO,
    "{ICON_NEWS_POLARITY_3C_P}": ICON_NEWS_POLARITY_3C_P,
    "{ICON_NEWS_POLARITY_3C_N}": ICON_NEWS_POLARITY_3C_N,
    "{ICON_NEWS_POLARITY_3C_A}": ICON_NEWS_POLARITY_3C_A,
    "{ICON_FLAG_PL_LANG}": ICON_FLAG_PL_LANG,
    "{ICON_FLAG_FR_LANG}": ICON_FLAG_FR_LANG,
    "{ICON_FLAG_RU_LANG}": ICON_FLAG_RU_LANG,
    "{ICON_FLAG_UA_LANG}": ICON_FLAG_UA_LANG,
    "{ICON_FLAG_DE_LANG}": ICON_FLAG_DE_LANG,
    "{ICON_FLAG_EN_LANG}": ICON_FLAG_EN_LANG,
    "{ICON_NEWS_PLI_BAD}": ICON_NEWS_PLI_BAD,
    "{ICON_NEWS_PLI_NORM}": ICON_NEWS_PLI_NORM,
    "{ICON_NEWS_PLI_GOOD}": ICON_NEWS_PLI_GOOD,
}

MIN_STREAM_QUERY_LEN = 12


class ApplicationIcons:
    # App icons
    HOME_ICO = "🏠"
    STREAM_ICO = "📰"
    CREATOR_ICO = "✍️"
    BROWSER_ICO = "🔎"
    EXPLORER_ICO = "🧭"
    PUBLIC_CHAT_ICO = "💬"
    STATISTICS_ICO = "📈"
    ADMINISTRATION_ICO = "🛡️"
