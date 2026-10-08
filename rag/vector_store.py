import os

from langchain_core.documents.base import Document
from pymilvus import MilvusClient
from utils.config_handler_util import milvus_conf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool_util import get_abs_path
from utils.file_handler_util import pdf_loader, txt_loader, listdir_with_allowed_types, get_file_md5_hex
from utils.logger_handler_util import logger
from model.factory import embedding_model

class VectorStoreService:

    def __init__(self):

        self.vector_store = MilvusClient(
            uri=milvus_conf["milvus_url"],
            db_name=milvus_conf["db_name"],
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=milvus_conf["chunk_size"],
            chunk_overlap=milvus_conf["chunk_overlap"],
            separators=milvus_conf["separators"],
            length_function=len,
        )


    def load_document(self):
        """
        从数据文件内读取数据 将其转化为向量存入向量数据库
        存入前需要计算md5值去重
        :return:
        """
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(milvus_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(milvus_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False
            with open(get_abs_path(milvus_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if md5_for_check == line:
                        return True # 处理过

            return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(milvus_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_document(file_path: str):

            if file_path.endswith("txt"):
                return txt_loader(file_path)
            elif file_path.endswith("pdf"):
                return pdf_loader(file_path)
            else:
                return []

        allowed_file_path = listdir_with_allowed_types(
            get_abs_path(milvus_conf["data_path"]),
            tuple(milvus_conf["allow_knowledge_file_type"])
        )

        for filepath in allowed_file_path:
            md5_hex = get_file_md5_hex(filepath)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{filepath}已存在于知识库内, 跳过")
                continue

            try:
                documents: list[Document]= get_file_document(filepath)
                if not documents:
                    logger.warning(f"[加载知识库]{filepath}内没有有效内容")
                    continue

                # 获取切分结果
                chunks = self.splitter.split_documents(documents)
                texts = [
                    chunk.page_content for chunk in chunks
                ]
                vectors = embedding_model.embed_documents(texts)
                # 将切分结果写入向量数据库
                data = [
                    {
                        "id": i,
                        "vector": vectors[i],
                        "text": chunks[i].page_content,
                    }

                    for i in range(len(chunks))
                ]
                self.vector_store.upsert(
                    collection_name=milvus_conf["collection_name"],
                    data=data,
                )
                # 记录处理过的文件的md5值
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{filepath}加载成功")

            except Exception as e:
                logger.error(f"[加载知识库]{filepath}加载失败: {str(e)}", exc_info=True)


if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()