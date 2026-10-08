"""
当用户提问时 搜索参考资料 将提问和参考资料交给模型 让模型总结回复
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model, embedding_model
from rag.vector_store import VectorStoreService
from utils.prompt_loader_util import load_rag_prompts
from utils.config_handler_util import milvus_conf

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str):

        query_vector = embedding_model.embed_query(str(query))

        results = self.vector_store.vector_store.search(
            collection_name=milvus_conf["collection_name"],
            data=[query_vector],
            limit=10,
            output_fields=["text"],
        )

        return results[0]

    def rag_summarize(self, query: str):

        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for i, doc in enumerate(context_docs):
            text = doc["entity"]["text"]
            counter += 1
            context += f"[参考资料{counter}]: 参考资料: {text}\n]"

        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )

if __name__ == "__main__":
    rag = RagSummarizeService()
    print(rag.rag_summarize("小户型适合哪种扫地机器人"))