import streamlit as st

from src.language import LanguageTranslator
from src.session_config import SessionConfig
from src.constants import (
    DEFAULT_UI_CONFIG_PATH,
    DEFAULT_ADMIN_UI_STATUSES_IN_ROW,
)
from src.api_public import (
    PlaygroundAuthenticationAPI,
    PlaygroundAdministrationAPI,
)
from src.token_utils import TokenValidator
from src.ui_utils_public import show_admin_window, initialize_page

AUTH_QUERY_PARAMS = ["state", "session_state", "iss", "code"]


def main():
    st.set_page_config(
        page_title=LanguageTranslator.translate(code_name="admin_page_title"),
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_page()

    SessionConfig.init_session_state_if_needed(reset_state=False)

    auth_api = PlaygroundAuthenticationAPI(
        config_path=DEFAULT_UI_CONFIG_PATH,
    )

    token_str = SessionConfig.get_session_auth_token()
    token = SessionConfig.get_session_auth_token_full_info()
    if token_str is None or token is None:
        login_query_params = dict(st.query_params)
        if not len(login_query_params):
            login_query_params = SessionConfig.get_session_auth_state_params()

        login_url = SessionConfig.get_session_auth_url()
        if login_query_params is None or not len(login_query_params):
            if login_url is None or not len(login_url):
                login_url = auth_api.get_proper_login_url()
                if login_url is None or "login_url" not in login_url:
                    return
                login_url = login_url["login_url"]
                SessionConfig.set_session_auth_url(login_url)

            st.sidebar.link_button(
                LanguageTranslator.translate(code_name="admin_login"), login_url
            )
        else:
            for q_p in AUTH_QUERY_PARAMS:
                if q_p not in login_query_params:

                    st.error(
                        LanguageTranslator.translate(
                            code_name="admin_no_q_p"
                        ).replace("{q_p}", q_p)
                    )

                    return
            SessionConfig.set_session_auth_state_params(
                auth_state=login_query_params
            )
        session_state = SessionConfig.get_session_auth_state_params()
        token = auth_api.login(session_state=session_state)
        token_str = None if token is None else token["token"]
        SessionConfig.set_session_auth_token(auth_token=token_str)
        SessionConfig.set_session_auth_token_full_response(full_info=token)

    if token_str is not None and len(token_str):
        _tv = TokenValidator()
        if not _tv.validate_token_string(token_str=token_str):
            st.error("Token is not valid")
            return

        admin_api = PlaygroundAdministrationAPI(config_path=DEFAULT_UI_CONFIG_PATH)
        system_status = admin_api.get_system_status(
            token_str=token_str,
            token_info=token,
            auth_api=auth_api,
        )

        show_admin_window(
            token_info=token,
            token_str=token_str,
            system_status=system_status,
            admin_api=admin_api,
            auth_api=auth_api,
            max_statuses_in_row=DEFAULT_ADMIN_UI_STATUSES_IN_ROW,
        )


if __name__ == "__main__":
    main()
