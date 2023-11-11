from openai import OpenAI

from typing import Optional
from abc import ABC, abstractmethod

from snippetize_me.settings import config


SECRET_KEY = config.get('open-ai-api').get('secret-key')


class BaseCommunicator(ABC):
    """
    The base class for generating a communicator between API and controllers
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._is_initialized = False
        return cls._instance

    def __init__(self, secret_key: Optional[str] = SECRET_KEY):
        if not self._is_initialized:
            self.api_client = self._initialize_api_client(secret_key)
            self._is_initialized = True

    @abstractmethod
    def _initialize_api_client(self, secret_key):
        """Method for api initialization with secret key"""
        raise NotImplementedError


class OpenAICommunicator(BaseCommunicator):
    def _initialize_api_client(self, secret_key: str) -> OpenAI:
        return OpenAI(api_key=secret_key)
