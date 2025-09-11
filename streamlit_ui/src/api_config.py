import json


class ApiJsonConfiguration:
    API_EP_FIELD = "ep"
    API_HOST_FIELD = "host"

    JSON_MODULES_FIELD = "modules"
    API_PUBLIC_CHAT_CONVERSATION = "public_chat_conversation"
    API_PUBLIC_NEWS_STREAM = "public_news_stream"
    API_PUBLIC_NEWS_CREATOR = "public_news_creator"
    API_PUBLIC_NEWS_BROWSER = "public_news_browser"
    API_AUTHORIZATION = "authorization"
    API_ADMINISTRATION = "administration"

    def __init__(self, config_path: str | None = None) -> None:
        self._api_config_dict = {}
        self.config_path = config_path

        self._auth_config = None
        self._admin_config = None
        self._free_c_c_config = None
        self._free_n_s_config = None
        self._free_n_c_config = None
        self._free_b_c_config = None

        if config_path is not None:
            self.load()

    @property
    def free_chat_conversation_host(self) -> str | None:
        if self._free_c_c_config is None:
            return None
        return self._free_c_c_config[self.API_HOST_FIELD]

    @property
    def free_chat_conversation_endpoints(self) -> dict | None:
        if self._free_c_c_config is None:
            return {}
        return self._free_c_c_config[self.API_EP_FIELD]

    @property
    def free_news_stream_host(self) -> str | None:
        if self._free_n_s_config is None:
            return None
        return self._free_n_s_config[self.API_HOST_FIELD]

    @property
    def free_news_stream_endpoints(self) -> dict | None:
        if self._free_n_s_config is None:
            return {}
        return self._free_n_s_config[self.API_EP_FIELD]

    @property
    def free_news_creator_host(self) -> str | None:
        if self._free_n_c_config is None:
            return None
        return self._free_n_c_config[self.API_HOST_FIELD]

    @property
    def free_news_creator_endpoints(self) -> dict | None:
        if self._free_n_c_config is None:
            return {}
        return self._free_n_c_config[self.API_EP_FIELD]

    @property
    def free_news_browser_host(self) -> str | None:
        if self._free_b_c_config is None:
            return None
        return self._free_b_c_config[self.API_HOST_FIELD]

    @property
    def free_news_browser_endpoints(self) -> dict | None:
        if self._free_b_c_config is None:
            return {}
        return self._free_b_c_config[self.API_EP_FIELD]

    @property
    def auth_host(self) -> str | None:
        if self._auth_config is None:
            return None
        return self._auth_config[self.API_HOST_FIELD]

    @property
    def auth_endpoints(self) -> dict | None:
        if self._auth_config is None:
            return {}
        return self._auth_config[self.API_EP_FIELD]

    @property
    def admin_host(self) -> str | None:
        if self._admin_config is None:
            return None
        return self._admin_config[self.API_HOST_FIELD]

    @property
    def admin_endpoints(self) -> dict | None:
        if self._admin_config is None:
            return {}
        return self._admin_config[self.API_EP_FIELD]

    def load(self, config_path: str | None = None) -> None:
        if config_path is not None:
            self.config_path = config_path
        with open(self.config_path, "rt") as json_in:
            self._api_config_dict = json.load(json_in)[self.JSON_MODULES_FIELD]
        self._process_config_file()

    def _process_config_file(self) -> None:
        self._free_c_c_config = self._api_config_dict[
            self.API_PUBLIC_CHAT_CONVERSATION
        ]
        self._free_n_s_config = self._api_config_dict[self.API_PUBLIC_NEWS_STREAM]
        self._free_n_c_config = self._api_config_dict[self.API_PUBLIC_NEWS_CREATOR]
        self._free_b_c_config = self._api_config_dict[self.API_PUBLIC_NEWS_BROWSER]
        self._auth_config = self._api_config_dict[self.API_AUTHORIZATION]
        self._admin_config = self._api_config_dict[self.API_ADMINISTRATION]

    @staticmethod
    def _prepare_proper_host(host: str) -> str:
        return host.strip("/")

    @staticmethod
    def _prepare_proper_ep(ep: str) -> str:
        return ep.strip("/")
