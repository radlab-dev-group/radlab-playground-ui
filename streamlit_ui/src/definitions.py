from src.constants import ICON_DEFAULT_VALUE_UI
from src.language import LanguageTranslator, _LanguageDefinitions

ICON_NEWS_PLI_BAD = ":red_circle:"
ICON_NEWS_PLI_NORM = ":large_yellow_circle:"
ICON_NEWS_PLI_GOOD = ":large_green_circle:"


def prepare_pli_icons():
    pli_icons = [
        {
            "below_value": 0.0,
            "icon": ICON_DEFAULT_VALUE_UI,
            "text": f"{ICON_DEFAULT_VALUE_UI} {LanguageTranslator.translate(code_name='pli_value_all')}",
        },
        {
            "below_value": 0.301,
            "icon": ICON_NEWS_PLI_BAD,
            "text": f"{ICON_NEWS_PLI_BAD} {LanguageTranslator.translate(code_name='pli_value_bad')}",
        },
        {
            "below_value": 0.701,
            "icon": ICON_NEWS_PLI_NORM,
            "text": f"{ICON_NEWS_PLI_NORM} {LanguageTranslator.translate(code_name='pli_value_norm')}",
        },
        {
            "below_value": 1.01,
            "icon": ICON_NEWS_PLI_GOOD,
            "text": f"{ICON_NEWS_PLI_GOOD} {LanguageTranslator.translate(code_name='pli_value_good')}",
        },
    ]
    ico2value = {p["text"]: p["below_value"] for p in pli_icons}
    value2ico = {p["below_value"]: p["icon"] for p in pli_icons}

    return pli_icons, ico2value, value2ico
