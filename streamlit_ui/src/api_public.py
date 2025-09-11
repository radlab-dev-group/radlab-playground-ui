import abc
import json
import datetime
import requests

from typing import List, Dict

from src.session_config import SessionConfig
from src.api_config import ApiJsonConfiguration


class BasePublicApiInterface(abc.ABC):
    API_CALL_JSON_LIST_CHAT_MODELS = None

    def __init__(self):
        self._last_response = None

    @staticmethod
    def auth_header(token_str: str):
        return {"Authorization": f"token {token_str}"}

    @property
    def last_response(self):
        return self._last_response

    @staticmethod
    def general_call_get(
        host_url: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
        token_info: dict | None = None,
        auth_api=None,
    ):
        user_api_call_url = "{}/{}".format(host_url.strip("/"), endpoint.strip("/"))
        response = requests.get(
            user_api_call_url, params=params, data=data, headers=headers
        )

        if (
            response.status_code == 401
            and headers is not None
            and auth_api is not None
        ):
            if token_info is None or "refresh_token" not in token_info:
                return response
            new_token_info = auth_api.refresh_token(
                refresh_token=token_info["refresh_token"]
            )
            if new_token_info is None:
                return response
            new_token_str = new_token_info["token"]
            SessionConfig.set_session_auth_token(auth_token=new_token_str)
            SessionConfig.set_session_auth_token_full_response(
                full_info=new_token_info
            )
            new_headers = BasePublicApiInterface.auth_header(new_token_str)
            return BasePublicApiInterface.general_call_get(
                host_url=host_url,
                endpoint=endpoint,
                params=params,
                data=data,
                headers=new_headers,
                token_info=new_token_info,
                auth_api=None,
            )

        if response.status_code != 200:
            return response
        return response.json()

    @staticmethod
    def general_call_post(
        host_url: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        files=None,
        json_data: dict | None = None,
        headers: dict | None = None,
        token_info: dict | None = None,
        auth_api=None,
    ):
        if not len(host_url):
            user_api_call_url = endpoint
        else:
            user_api_call_url = "{}/{}".format(host_url, endpoint)

        response = requests.post(
            user_api_call_url,
            params=params,
            files=files,
            data=data,
            json=json_data,
            headers=headers,
        )

        if (
            response.status_code == 401
            and headers is not None
            and auth_api is not None
        ):
            if token_info is None or "refresh_token" not in token_info:
                return response
            new_token_info = auth_api.refresh_token(
                refresh_token=token_info["refresh_token"]
            )
            if new_token_info is None:
                return response
            new_token_str = new_token_info["token"]
            SessionConfig.set_session_auth_token(auth_token=new_token_str)
            SessionConfig.set_session_auth_token_full_response(
                full_info=new_token_info
            )
            new_headers = BasePublicApiInterface.auth_header(new_token_str)
            return BasePublicApiInterface.general_call_post(
                host_url=host_url,
                endpoint=endpoint,
                params=params,
                data=data,
                files=files,
                json_data=json_data,
                headers=new_headers,
                token_info=new_token_info,
                auth_api=None,
            )

        if response.status_code != 200:
            return response
        return response.json()

    @staticmethod
    def return_response(response):
        response_str = ""
        if type(response) not in [dict] or "status" not in response:
            if type(response.text) in [list, tuple]:
                if len(response):
                    response_str = str(response)
            else:
                response_str = response.text
            return {"status": False, "response": response_str}

        if response["status"]:
            return response["body"]
        return response


class PublicConversationWithModelAPI(BasePublicApiInterface):
    API_CALL_JSON_NEW_CHAT = "new_chat"
    API_CALL_JSON_SAVE_CHAT = "save_chat"
    API_CALL_JSON_ADD_CHAT_MSG = "add_chat_message"
    API_CALL_JSON_GET_CHAT_BY_HASH = "get_chat_by_hash"
    API_CALL_JSON_LIST_CHAT_MODELS = "conversation_models"

    def __init__(self, config_path: str):
        super(PublicConversationWithModelAPI, self).__init__()
        self.api_config = ApiJsonConfiguration(config_path=config_path)

    def list_available_models(self, api_call_url: str | None = None):
        if api_call_url is None:
            api_call_url = self.api_config.free_chat_conversation_endpoints[
                self.API_CALL_JSON_LIST_CHAT_MODELS
            ]

        response = self.general_call_get(
            host_url=self.api_config.free_chat_conversation_host,
            endpoint=api_call_url,
        )
        self._last_response = response
        return self.return_response(response=response)

    def new_chat(
        self,
        model_name: str,
        generation_options: Dict,
        public_state_options: Dict,
        api_call_url: str | None = None,
    ):
        if api_call_url is None:
            api_call_url = self.api_config.free_chat_conversation_endpoints[
                self.API_CALL_JSON_NEW_CHAT
            ]

        options = generation_options
        for k, v in public_state_options.items():
            options[k] = v
        options["model_name"] = model_name
        data = {"model_name": model_name, "options": json.dumps(options)}
        response = self.general_call_post(
            host_url=self.api_config.free_chat_conversation_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response
        return self.return_response(response=response)

    def save_chat(
        self,
        chat_id,
        model_name: str,
        save_as_read_only: bool = True,
        api_call_url: str | None = None,
    ):
        if api_call_url is None:
            api_call_url = self.api_config.free_chat_conversation_endpoints[
                self.API_CALL_JSON_SAVE_CHAT
            ]

        data = {
            "chat_id": chat_id,
            "model_name": model_name,
            "read_only": save_as_read_only,
        }
        response = self.general_call_post(
            host_url=self.api_config.free_chat_conversation_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response
        return self.return_response(response=response)

    def get_chat_by_hash(
        self,
        chat_hash,
        model_name: str,
        convert_history_to_session: bool = True,
        api_call_url: str | None = None,
    ):
        if api_call_url is None:
            api_call_url = self.api_config.free_chat_conversation_endpoints[
                self.API_CALL_JSON_GET_CHAT_BY_HASH
            ]

        data = {"chat_hash": chat_hash, "model_name": model_name}
        response = self.general_call_get(
            host_url=self.api_config.free_chat_conversation_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response

        chat_id, chat_history, is_read_only = None, [], True
        if "body" in response:
            chat_id = response["body"].get("chat_id", None)
            is_read_only = response["body"].get("is_read_only", True)
            chat_history = response["body"].get("chat_history", [])
            conv_chat_history = []
            if convert_history_to_session:
                last_turn = None
                for msg in chat_history:
                    if last_turn is None:
                        last_turn = {msg["role"]: msg["text"]}
                    else:
                        last_turn[msg["role"]] = msg["text"]
                        conv_chat_history.append(last_turn)
                        last_turn = None
                chat_history = conv_chat_history
        return chat_id, chat_history, is_read_only

    def add_chat_message(
        self,
        chat_id,
        last_user_msg: str,
        generation_options: Dict,
        public_state_options: Dict,
        model_name: str,
        rag_search_options: Dict | None,
        api_call_url: str | None = None,
    ):
        generation_options["use_content_supervisor"] = public_state_options.get(
            "use_content_supervisor", False
        )
        generation_options["use_rag_supervisor"] = public_state_options.get(
            "use_rag_supervisor", False
        )
        generation_options["use_doc_names_in_response"] = False

        if rag_search_options is not None:
            generation_options["percentage_rank_mass"] = rag_search_options.get(
                "percentage_rank_mass", 80
            )

        if api_call_url is None:
            api_call_url = self.api_config.free_chat_conversation_endpoints[
                self.API_CALL_JSON_ADD_CHAT_MSG
            ]

        data = {
            "last_user_message": last_user_msg,
            "generation_options": json.dumps(generation_options),
            "model_name": model_name,
            "chat_id": chat_id,
        }
        if rag_search_options is not None and len(rag_search_options):
            data["search_options"] = json.dumps(rag_search_options)

        response = self.general_call_post(
            host_url=self.api_config.free_chat_conversation_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response
        return self.return_response(response=response)


class PlaygroundAuthenticationAPI(BasePublicApiInterface):
    API_CALL_JSON_GET_LOGIN_URL = "get_login_url"
    API_CALL_JSON_GET_LOGIN = "login"
    API_CALL_JSON_GET_LOGOUT = "logout"
    API_CALL_JSON_REFRESH_TOKEN = "refresh_token"

    def __init__(self, config_path: str):
        self.api_config = ApiJsonConfiguration(config_path=config_path)
        super(PlaygroundAuthenticationAPI, self).__init__()

    def get_proper_login_url(self):
        api_call_url = self.api_config.auth_endpoints[
            self.API_CALL_JSON_GET_LOGIN_URL
        ]
        response = self.general_call_post(
            host_url=self.api_config.auth_host,
            endpoint=api_call_url,
        )
        self._last_response = response
        return self.return_response(response=response)

    def login(self, session_state: dict) -> dict | None:
        login_url = self.api_config.auth_endpoints[self.API_CALL_JSON_GET_LOGIN]
        response = self.general_call_post(
            host_url=self.api_config.auth_host,
            endpoint=login_url,
            data=session_state,
        )
        response = self.return_response(response=response)
        if response is not None and "token" in response:
            return response
        return None

    def refresh_token(self, refresh_token: str) -> dict | None:
        login_url = self.api_config.auth_endpoints[self.API_CALL_JSON_REFRESH_TOKEN]
        response = self.general_call_post(
            host_url=self.api_config.auth_host,
            endpoint=login_url,
            data={"refresh_token": refresh_token},
        )
        response = self.return_response(response=response)
        if response is not None and "token" in response:
            return response
        return None


class PlaygroundAdministrationAPI(BasePublicApiInterface):
    API_CALL_JSON_GET_SYSTEM_STATUS = "system_status"
    API_CALL_JSON_GET_NEWS_STATISTICS = "news_statistics"
    API_CALL_JSON_DO_ADM_ACT_ON_MODULE = "do_admin_action_on_module"
    API_CALL_JSON_LAST_NEWS_TO_CHECK_CORRECT = "last_news_to_check"

    def __init__(self, config_path: str):
        self.api_config = ApiJsonConfiguration(config_path=config_path)
        super(PlaygroundAdministrationAPI, self).__init__()

    def get_system_status(self, token_str: str, token_info, auth_api):
        api_call_url = self.api_config.admin_endpoints[
            self.API_CALL_JSON_GET_SYSTEM_STATUS
        ]
        headers = self.auth_header(token_str=token_str)
        response = self.general_call_get(
            host_url=self.api_config.admin_host,
            endpoint=api_call_url,
            headers=headers,
            token_info=token_info,
            auth_api=auth_api,
        )
        self._last_response = response
        return self.return_response(response=response)

    def get_news_statistics(
        self, token_str: str | None, token_info, auth_api, settings_id
    ):
        if token_str is not None and len(token_str):
            api_call_url = self.api_config.admin_endpoints[
                self.API_CALL_JSON_GET_NEWS_STATISTICS
            ]
        else:
            raise Exception("Problem during getting news statistics")
        headers = (
            self.auth_header(token_str=token_str)
            if token_str is not None and len(token_str)
            else None
        )
        response = self.general_call_get(
            host_url=self.api_config.admin_host,
            endpoint=api_call_url,
            headers=headers,
            data={"settings_id": settings_id},
            token_info=token_info,
            auth_api=auth_api,
        )
        self._last_response = response
        return self.return_response(response=response)

    def do_admin_action_on_module(
        self, settings_id, module, action, token_str, token_info, auth_api
    ):
        api_call_url = self.api_config.admin_endpoints[
            self.API_CALL_JSON_DO_ADM_ACT_ON_MODULE
        ]
        headers = self.auth_header(token_str=token_str)
        data = {
            "settings_id": settings_id,
            "module": module,
            "action": action,
        }
        response = self.general_call_post(
            host_url=self.api_config.admin_host,
            endpoint=api_call_url,
            data=data,
            headers=headers,
            token_info=token_info,
            auth_api=auth_api,
        )
        self._last_response = response
        return self.return_response(response=response)

    def show_news_to_check_correctness(
        self,
        number_of_news: int,
        filter_pages: dict or None,
        token_str: str,
        token_info,
        auth_api,
    ):
        api_call_url = self.api_config.admin_endpoints[
            self.API_CALL_JSON_LAST_NEWS_TO_CHECK_CORRECT
        ]
        data = {"number_of_news": number_of_news}

        headers = self.auth_header(token_str=token_str)
        if filter_pages is not None and len(filter_pages):
            data["filter_pages"] = json.dumps(filter_pages)

        response = self.general_call_get(
            host_url=self.api_config.admin_host,
            endpoint=api_call_url,
            data=data,
            headers=headers,
            token_info=token_info,
            auth_api=auth_api,
        )
        self._last_response = response
        return self.return_response(response=response)


class PublicNewsStreamAPI(BasePublicApiInterface):
    API_CALL_JSON_LIST_CATEGORIES = "get_categories"
    API_CALL_JSON_LIST_CATEGORIES_WITH_PAGES = "get_categories_with_pages"
    API_CALL_JSON_LIST_LAST_CATEGORIES = "get_last_news"
    API_CALL_JSON_LAST_DAYS_SUMMARIZER = "generate_article_from_search"
    API_CALL_JSON_DO_NEWS_ACTION = "do_news_action"
    API_CALL_JSON_GET_NEWS_STATISTICS_PUBLIC = "news_statistics_public"
    API_CALL_JSON_SEARCH_PHRASE_IN_NEWS = "search_news_in_categories"

    def __init__(self, config_path: str):
        self.api_config = ApiJsonConfiguration(config_path=config_path)
        super(PublicNewsStreamAPI, self).__init__()

    def list_available_categories(self, api_call_url: str | None = None):
        if api_call_url is None:
            api_call_url = self.api_config.free_news_stream_endpoints[
                self.API_CALL_JSON_LIST_CATEGORIES
            ]

        response = self.general_call_get(
            host_url=self.api_config.free_news_stream_host,
            endpoint=api_call_url,
        )
        self._last_response = response
        return self.return_response(response=response)

    def list_available_categories_with_pages(self, api_call_url: str | None = None):
        if api_call_url is None:
            api_call_url = self.api_config.free_news_stream_endpoints[
                self.API_CALL_JSON_LIST_CATEGORIES_WITH_PAGES
            ]

        response = self.general_call_get(
            host_url=self.api_config.free_news_stream_host,
            endpoint=api_call_url,
        )
        self._last_response = response
        return self.return_response(response=response)

    def all_news_from_all_categories(
        self,
        news_in_category: int,
        filter_pages: dict,
        polarity_3c: str | None,
        pli_from: int | None,
        pli_to: int | None,
        api_call_url: str | None = None,
    ):
        if api_call_url is None:
            api_call_url = self.api_config.free_news_stream_endpoints[
                self.API_CALL_JSON_LIST_LAST_CATEGORIES
            ]

        data = {
            "news_in_category": news_in_category,
            "filter_pages": json.dumps(filter_pages),
            "polarity_3c": polarity_3c,
            "pli_from": pli_from,
            "pli_to": pli_to,
        }

        response = self.general_call_get(
            host_url=self.api_config.free_news_stream_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response
        return self.return_response(response=response)

    def do_news_option(
        self, news_id, action: str, token_str: str, token_info: dict, auth_api
    ):
        api_call_url = self.api_config.free_news_stream_endpoints[
            self.API_CALL_JSON_DO_NEWS_ACTION
        ]
        headers = self.auth_header(token_str=token_str)

        data = {"news_id": news_id, "action": action}
        response = self.general_call_post(
            host_url=self.api_config.free_news_stream_host,
            endpoint=api_call_url,
            json_data=data,
            data=None,
            headers=headers,
            token_info=token_info,
            auth_api=auth_api,
        )

        self._last_response = response
        return self.return_response(response=response)

    def get_news_statistics(self, settings_id, get_last_stats: bool):
        api_call_url = self.api_config.free_news_stream_endpoints[
            self.API_CALL_JSON_GET_NEWS_STATISTICS_PUBLIC
        ]

        data = {"settings_id": settings_id, "get_last_stats": get_last_stats}
        response = self.general_call_get(
            host_url=self.api_config.admin_host,
            endpoint=api_call_url,
            headers=None,
            data=data,
            token_info=None,
            auth_api=None,
        )
        self._last_response = response
        return self.return_response(response=response)

    def search_news_in_categories(
        self,
        text_to_search: str,
        filter_pages: dict,
        num_of_results: int,
        last_days: int,
        api_call_url: str | None = None,
    ):
        if api_call_url is None:
            api_call_url = self.api_config.free_news_stream_endpoints[
                self.API_CALL_JSON_SEARCH_PHRASE_IN_NEWS
            ]

        sites_urls = []
        for category, cat_urls in filter_pages.items():
            for cat_urls_items in cat_urls:
                for url, url_status in cat_urls_items.items():
                    if url_status:
                        sites_urls.append(url)

        data = {
            "text_to_search": text_to_search,
            "num_of_results": num_of_results,
            "number_of_last_days": last_days,
            "sites": json.dumps(sites_urls),
        }

        response = self.general_call_post(
            host_url=self.api_config.free_news_stream_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response
        return self.return_response(response=response)


class PublicNewsCreatorAPI(BasePublicApiInterface):
    API_CALL_JSON_GEN_NEWS_FROM_SEARCH = "generate_article_from_search"

    def __init__(self, config_path: str):
        self.api_config = ApiJsonConfiguration(config_path=config_path)
        super(PublicNewsCreatorAPI, self).__init__()

    def generate_article_from_search_result(
        self,
        news_ids: List[int],
        user_query_str: str,
        type_of_new_article: str,
        query_response_id: int,
        api_call_url: str | None = None,
    ) -> dict:
        if api_call_url is None:
            api_call_url = self.api_config.free_news_creator_endpoints[
                self.API_CALL_JSON_GEN_NEWS_FROM_SEARCH
            ]

        data = {
            "user_query": user_query_str,
            "news_ids": json.dumps(news_ids),
            "article_type": type_of_new_article,
            "sse_query_response_id": query_response_id,
        }

        response = self.general_call_post(
            host_url=self.api_config.free_news_stream_host,
            endpoint=api_call_url,
            data=data,
        )
        self._last_response = response
        return self.return_response(response=response)


class PublicNewsBrowserAPI(BasePublicApiInterface):
    API_CALL_JSON_ARTICLE_SUMMARY_OF_DAY = "articles_summary_of_day"

    def __init__(self, config_path: str):
        self.api_config = ApiJsonConfiguration(config_path=config_path)
        super(PublicNewsBrowserAPI, self).__init__()

    def get_summary_of_day(self, date: datetime.date):
        api_call_url = self.api_config.free_news_browser_endpoints[
            self.API_CALL_JSON_ARTICLE_SUMMARY_OF_DAY
        ]

        response = self.general_call_get(
            host_url=self.api_config.free_news_browser_host,
            endpoint=api_call_url,
            data={"date": date},
        )
        self._last_response = response
        return self.return_response(response=response)
