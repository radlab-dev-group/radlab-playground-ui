import streamlit as st

from src.language import LanguageTranslator
from src.ui_utils_public import initialize_page

NEW_APP_URL = "https://radar.apps.radlab.dev"


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="news_browser_page_title"),
        page_icon="📡",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    initialize_page()

    st.markdown(
        """
        <style>
        .migration-card {
            background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
            border-radius: 1rem;
            padding: 3rem 2rem;
            text-align: center;
            border: 1px solid #cbd5e1;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        }
        .migration-card h2 {
            font-size: 1.8rem;
            color: #1e293b;
            margin-bottom: 0.5rem;
        }
        .migration-card p {
            font-size: 1.1rem;
            color: #475569;
            max-width: 600px;
            margin: 0 auto 1.5rem;
        }
        .migration-card a {
            display: inline-block;
            padding: 0.75rem 2rem;
            background: #3b82f6;
            color: white;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: background 0.2s;
        }
        .migration-card a:hover {
            background: #2563eb;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="migration-card">
            <h2>📡 Przeglądarka Informacji została przeniesiona</h2>
            <p>
                Funkcjonalność przeglądarki informacji została przeniesiona do nowej aplikacji.
                Zapraszamy do korzystania z odświeżonego interfejsu pod adresem:
            </p>
            <a href="{NEW_APP_URL}" target="_blank" rel="noopener noreferrer">{NEW_APP_URL}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
