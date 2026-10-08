import os
import hashlib

from langchain_core.documents import Document

from utils.logger_handler_util import logger
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(file_path):   # 获取文件的md5十六进制字符串

    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在")
        return None

    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]{file_path}不是文件")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096 # 分片读取的大小4KB

    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)

            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5计算]计算{file_path}失败,{str(e)}")
        return None


def listdir_with_allowed_types(path: str, allowed_types: tuple[str]):
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_types]{path}不是文件夹")
        return None

    for file in os.listdir(path):
        if file.endswith(allowed_types):
            files.append(os.path.join(path, file))

    return tuple(files)


def pdf_loader(filepath: str, passwd = None) -> list[Document]:

    return PyPDFLoader(
        file_path=filepath,
        password=passwd,
    ).load()


def txt_loader(filepath: str, passwd = None) -> list[Document]:

    return TextLoader(
        file_path=filepath,
        encoding="utf-8",
    ).load()