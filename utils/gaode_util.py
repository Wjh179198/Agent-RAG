import os
import requests
from dotenv import load_dotenv

# 读取配置信息
load_dotenv(override=True)

GAODE_API_KEY : str | None = os.getenv("GAODE_API_KEY")

def get_user_city(ip_address: str):

    resp = requests.get(f"https://restapi.amap.com/v3/ip?ip={ip_address}&key={GAODE_API_KEY}")
    resp.raise_for_status()
    if resp.json()["status"] != 1:
        raise RuntimeError(f"{ip_address}地址解析失败")

    return str(resp.json()["city"])

def get_city_addcode(ip_address: str):

    resp = requests.get(f"https://restapi.amap.com/v3/ip?ip={ip_address}&key={GAODE_API_KEY}")
    resp.raise_for_status()
    if resp.json()["status"] != 1:
        raise RuntimeError(f"{ip_address}地址解析失败")
    return str(resp.json()["adcode"])

