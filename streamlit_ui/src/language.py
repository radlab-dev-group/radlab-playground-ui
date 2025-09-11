import pandas as pd

from typing import Optional

from src.session_config import SessionConfig
from src.constants import (
    DEFAULT_LANGUAGE,
    UI_LANG_DEFAULT_DEFINITION_FILE,
    REPLACE_FOR_TRANSLATIONS,
)


class _LanguageDefinitions:
    """
    Load translation definitions from an XLSX file.
    The first column must contain the *code* (unique identifier) for each
    translation entry. The next columns are named after language codes
    (e.g. ``pl``, ``en``) and contain the translated text.

    Example XLSX layout (first sheet):

    +------+----+----+
    | code | pl | en |
    +------+----+----+
    | hello| Cześć | Hello |
    +------+----+----+

    The class loads translation definitions from an XLSX
    file into an in‑memory dictionary:
    {
        "code1": {"pl": "tekst PL", "en": "text EN", ...},
        "code2": {"pl": "...", "en": "..."},
        ...
    }
    """

    CODE_NAME_COLUMN = "code_name"
    LANGUAGES = {
        "pl": "Polski 🇵🇱",
        "en": "English 🇬🇧",
    }

    LEAVE_COLUMNS = list(LANGUAGES.keys()) + [CODE_NAME_COLUMN]

    def __init__(
        self,
        xlsx_path: str,
        actual_lang: Optional[str] = None,
        init_session_if_not_exists: bool = True,
    ):
        """
        Initialize the definition loader.

        Parameters
        ----------
        xlsx_path: str
            Path to the XLSX file containing translation tables.
        """
        self._translations = None
        self._load_xlsx_file(xlsx_path=xlsx_path)

        self.xlsx_path = xlsx_path
        if init_session_if_not_exists:
            self._init_session_if_not_exists(actual_lang=actual_lang)

    def get_text_for_language_code(
        self, code_name: str, language: str = "pl"
    ) -> Optional[str]:
        """
        Retrieve the translated text for a given ``code_name`` and language.

        Parameters
        ----------
        code_name: str
            The translation key (value from the first column of the XLSX).
        language: str, optional
            Language column identifier (e.g. ``pl``, ``en``). Defaults to ``pl``.

        Returns
        -------
        str
            The translated text.

        Raises
        ------
        KeyError
            If ``code_name`` does not exist or the ``language`` column is absent.
        """
        if code_name not in self._translations:
            raise KeyError(
                f"Code '{code_name}' not found in translation definitions."
            )

        lang_map = self._translations[code_name]
        if language not in lang_map:
            raise KeyError(
                f"Language '{language}' not defined for code '{code_name}'."
            )

        return f"{lang_map[language]}"

    def _load_xlsx_file(self, xlsx_path: str):
        if self._translations is None:
            self._translations = {}

        df = pd.read_excel(xlsx_path, dtype=str)
        for row in df.iterrows():
            _cn = row[1][self.CODE_NAME_COLUMN]
            if _cn is None:
                # print(f"~ cannot find {self.CODE_NAME_COLUMN} in {row[1]}")
                continue

            self._translations[_cn] = {}
            for _l in self.LANGUAGES.keys():
                if _l not in row[1]:
                    raise Exception(f"Cannot find {_l} translation in {row[0]}")
                self._translations[_cn][_l] = row[1][_l]
        return self._translations

    @staticmethod
    def _init_session_if_not_exists(actual_lang: Optional[str] = None):
        SessionConfig.init_session_state_if_needed()
        if SessionConfig.get_session_ui_language() is None:
            SessionConfig.set_session_ui_language(
                language=(
                    DEFAULT_LANGUAGE
                    if actual_lang is None or not len(actual_lang)
                    else actual_lang
                )
            )


class LanguageTranslator:
    SessionConfig.init_session_state_if_needed()
    lang_def = _LanguageDefinitions(
        xlsx_path=UI_LANG_DEFAULT_DEFINITION_FILE,
        actual_lang=SessionConfig.get_session_ui_language(),
        init_session_if_not_exists=True,
    )

    @staticmethod
    def translate(code_name: str):
        language = SessionConfig.get_session_ui_language() or DEFAULT_LANGUAGE
        _str = LanguageTranslator.lang_def.get_text_for_language_code(
            code_name=code_name, language=language
        )
        if _str is None or not len(_str):
            return _str
        for _f, _t in REPLACE_FOR_TRANSLATIONS.items():
            _str = _str.replace(_f, _t)
        return _str
