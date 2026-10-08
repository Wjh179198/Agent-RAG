from utils.config_handler_util import prompt_conf
from utils.path_tool_util import get_abs_path
from utils.logger_handler_util import logger

def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompt_conf["main_prompt_path"])
        print(system_prompt_path)
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yml配置中没有main_prompt_path配置项")
        return None

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词失败, {str(e)}")
        return None


def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompt_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yml配置中没有rag_summarize_prompt_path配置项")
        return None

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析系统提示词失败, {str(e)}")
        return None


def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompt_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yml配置中没有report_prompt_path配置项")
        return None

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析系统提示词失败, {str(e)}")
        return None

if __name__ == "__main__":
    print(load_system_prompts())
