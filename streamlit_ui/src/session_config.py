import json

import streamlit as st

from typing import Optional


class SessionConfig:
    FREE_CHAT = "free_chat"
    FREE_CHAT_ID = "free_chat_id"
    FREE_CHAT_IS_RO = "free_chat_is_read_only"
    FREE_CHAT_CHAT_HASH = "free_chat_hash"

    AUTHENTICATED_USER = "authenticated_user"
    AUTHENTICATED_USER_INFO = "authenticated_user_info"
    AUTHENTICATION_URL = "authentication_url"
    AUTHENTICATION_STATE = "authentication_state"
    AUTHENTICATION_TOKEN = "authentication_token"
    AUTHENTICATION_TOKEN_FULL_INFO = "authentication_token_full_info"

    SELECTED_UI_LANGUAGE = "selected_ui_language"

    ALL_SESSION_VALUES = [
        FREE_CHAT,
        FREE_CHAT_ID,
        FREE_CHAT_CHAT_HASH,
        FREE_CHAT_IS_RO,
        AUTHENTICATED_USER,
        AUTHENTICATED_USER_INFO,
        AUTHENTICATION_URL,
        AUTHENTICATION_STATE,
        AUTHENTICATION_TOKEN,
        AUTHENTICATION_TOKEN_FULL_INFO,
        SELECTED_UI_LANGUAGE,
    ]

    @staticmethod
    def __return__value__(ret_value):
        if ret_value is None:
            return None
        if type(ret_value) in [str]:
            return None if not len(ret_value.strip()) else ret_value
        return ret_value

    @staticmethod
    def init_session_state_if_needed(reset_state: bool = False):
        for session_variable in SessionConfig.ALL_SESSION_VALUES:
            if reset_state:
                st.session_state[session_variable] = None
            else:
                if session_variable in st.session_state:
                    continue
                st.session_state[session_variable] = None

    @staticmethod
    def set_session_ui_language(language: Optional[str]):
        st.session_state[SessionConfig.SELECTED_UI_LANGUAGE] = language

    @staticmethod
    def get_session_ui_language():
        if SessionConfig.SELECTED_UI_LANGUAGE not in st.session_state:
            return None

        return SessionConfig.__return__value__(
            ret_value=st.session_state[SessionConfig.SELECTED_UI_LANGUAGE]
        )

    @staticmethod
    def set_session_free_chat_chat_id(
        chat: list | None, chat_id: str | None, is_chat_read_only: bool = False
    ):
        st.session_state[SessionConfig.FREE_CHAT] = chat
        st.session_state[SessionConfig.FREE_CHAT_ID] = chat_id
        st.session_state[SessionConfig.FREE_CHAT_IS_RO] = is_chat_read_only

    @staticmethod
    def set_session_authenticated_user(username: str | None):
        st.session_state[SessionConfig.AUTHENTICATED_USER] = username

    @staticmethod
    def get_session_authenticated_user():
        username = st.session_state[SessionConfig.AUTHENTICATED_USER]
        return SessionConfig.__return__value__(username)

    @staticmethod
    def set_session_auth_url(auth_url: str | None):
        st.session_state[SessionConfig.AUTHENTICATION_URL] = auth_url

    @staticmethod
    def set_session_auth_token(auth_token: str | None):
        st.session_state[SessionConfig.AUTHENTICATION_TOKEN] = auth_token

    @staticmethod
    def get_session_auth_token():
        a_token = st.session_state[SessionConfig.AUTHENTICATION_TOKEN]
        return SessionConfig.__return__value__(a_token)

    @staticmethod
    def set_session_auth_token_full_response(full_info: dict | None):
        if full_info is not None:
            full_info = json.dumps(full_info)
        st.session_state[SessionConfig.AUTHENTICATION_TOKEN_FULL_INFO] = full_info

    @staticmethod
    def get_session_auth_token_full_info():
        full_info = st.session_state[SessionConfig.AUTHENTICATION_TOKEN_FULL_INFO]
        if full_info is not None and len(full_info):
            full_info = json.loads(full_info)
        return full_info

    @staticmethod
    def get_session_auth_url():
        a_url = st.session_state[SessionConfig.AUTHENTICATION_URL]
        return SessionConfig.__return__value__(a_url)

    # AUTHENTICATION_STATE
    @staticmethod
    def set_session_auth_state_params(auth_state: dict | None):
        auth_state = json.dumps(auth_state)
        st.session_state[SessionConfig.AUTHENTICATION_STATE] = auth_state

    @staticmethod
    def get_session_auth_state_params():
        a_state = st.session_state[SessionConfig.AUTHENTICATION_STATE]
        if a_state is not None and len(a_state):
            a_state = json.loads(a_state)
        return SessionConfig.__return__value__(a_state)

    @staticmethod
    def set_session_free_chat_hash(chat_hash: str | None):
        st.session_state[SessionConfig.FREE_CHAT_CHAT_HASH] = chat_hash

    @staticmethod
    def get_session_free_chat_hash():
        chat = st.session_state[SessionConfig.FREE_CHAT_CHAT_HASH]
        return SessionConfig.__return__value__(chat)

    @staticmethod
    def get_session_free_chat_is_read_only():
        chat = st.session_state[SessionConfig.FREE_CHAT_IS_RO]
        return SessionConfig.__return__value__(chat)

    @staticmethod
    def get_session_free_chat():
        chat = st.session_state[SessionConfig.FREE_CHAT]
        return SessionConfig.__return__value__(chat)

    @staticmethod
    def get_session_free_chat_id():
        chat_id = st.session_state[SessionConfig.FREE_CHAT_ID]
        return SessionConfig.__return__value__(chat_id)
