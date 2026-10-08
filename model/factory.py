"""
提供模型
"""
import os
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models.base import init_chat_model, _ConfigurableModel
from langchain.embeddings.base import init_embeddings

from utils.config_handler_util import rag_conf

# 读取配置信息
load_dotenv(override=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL")

class BaseModelFactory(ABC):
    @abstractmethod
    def generate(self) -> Optional[Embeddings | BaseChatModel | _ConfigurableModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generate(self) -> BaseChatModel | _ConfigurableModel:
        return init_chat_model(
            model=rag_conf["chat_model_name"],
            model_provider=rag_conf["chat_model_provider"],
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            extra_body={
                "thinking": {"type": "disabled"}
            }
        )


class EmbeddingsModelFactory(BaseModelFactory):
    def generate(self) -> Optional[Embeddings | BaseChatModel | _ConfigurableModel]:
        return init_embeddings(
            model=rag_conf["embedding_model_provider"] + ":" + rag_conf["embedding_model_name"],
            api_key=SILICONFLOW_API_KEY,
            base_url=SILICONFLOW_BASE_URL,
        )

chat_model = ChatModelFactory().generate()
embedding_model = EmbeddingsModelFactory().generate()