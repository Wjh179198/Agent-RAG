import os
import random

from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
from rag.rag_service import RagSummarizeService
from utils.config_handler_util import agent_conf
from utils.gaode_util import get_user_city, get_city_addcode
from utils.logger_handler_util import logger
from utils.path_tool_util import get_abs_path

rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",]
external_data={}

# 读取配置信息
load_dotenv(override=True)

GAODE_API_KEY : str | None = os.getenv("GAODE_API_KEY")


@tool
def rag_summarize(query: str):
    """
    当用户提问时 搜索参考资料 将提问和参考资料交给模型 让模型总结回复

    Args:
        query: 用户的问题

    Returns:
          返回的参考资料
    """
    return rag.rag_summarize(query)

@tool
def get_user_location() -> str:
    """
    获取用户所在的城市

    Returns:
        返回城市的字符串
    """
    return get_user_city("113.54.202.57")

@tool
def get_weather(city: str) -> str:
    """
    获取城市的天气信息

    Args:
        city: 具体的城市

    Returns:
          返回天气详情
    """
    address_code = get_city_addcode("113.54.202.57")
    resp = requests.get(f"https://restapi.amap.com/v3/weather/weatherInfo?city={address_code}?key={GAODE_API_KEY}")
    resp.raise_for_status()
    weather = resp.json()
    if weather["status"] != 1 or not weather["lives"]:
        raise RuntimeError(f"城市{city}的天气获取失败")

    live = weather["lives"][0]
    condition = live.get("weather", "未知")
    temperature = live.get("temperature", "未知")
    humidity = live.get("humidity", "未知")
    wind_direction = live.get("winddirection", "未知")
    wind_power = live.get("windpower", "未知")
    report_time = live.get("reporttime", "未知")

    return (
        f"城市{city}天气为{condition}，气温{temperature}摄氏度，"
        f"空气湿度{humidity}%，{wind_direction}风{wind_power}级，"
        f"数据发布时间{report_time}。"
    )

@tool
def get_current_month() -> str:
    """
    获取当前月份
    """
    return random.choice(month_arr)

@tool
def get_user_id() -> str:
    """
    获取用户的ID，以纯字符串形式返回
    """
    return random.choice(user_ids)

def generate_external_data():
    """
    {
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        ...
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回， 如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"







