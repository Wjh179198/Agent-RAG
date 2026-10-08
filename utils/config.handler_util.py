"""
yaml
"""

import yaml
from utils.path_tool_util import get_abs_path

def load_rag_yaml(config_path: str = get_abs_path("config/rag.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_chroma_yaml(config_path: str = get_abs_path("config/chroma.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_prompt_yaml(config_path: str = get_abs_path("config/prompt.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_agent_yaml(config_path: str = get_abs_path("config/agent.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


rag_conf = load_rag_yaml()
chroma_conf = load_chroma_yaml()
prompt_conf = load_prompt_yaml()
agent_conf = load_agent_yaml()