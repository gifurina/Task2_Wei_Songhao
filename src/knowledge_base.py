"""
知识库管理模块

负责：
1. Chroma 向量数据库的初始化与连接
2. PDF 文档的加载、切分、向量化、入库
3. 提供检索器(retriever)给 RAG 链使用

核心类：KnowledgeBase
"""
import os
import config
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from util import check_md5,save_md5,get_file_md5

class KnowledgeBase:

    def __init__(self,embedding_model):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=embedding_model,
            persist_directory=config.persist_directory,
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )

    def upload_by_pdf(self, file_path: str):
        try:
            if not os.path.exists(file_path):
                return f"[ERROR] file not found:{file_path}"

            md5_hex = get_file_md5(file_path)

            if check_md5(md5_hex):
                return "[SKIP] file already exists"

            loader = PyPDFLoader(file_path=file_path)
            docs = loader.load()

            if not docs:
                return "[WARNING] PDF file is empty"

            split_docs = self.splitter.split_documents(docs)

            if not split_docs:
                return "[WARNING] no content to split"

            self.chroma.add_documents(documents=split_docs)
            save_md5(md5_hex)

            return f"successfully upload {len(split_docs)} segments"

        except FileNotFoundError:
            return f"[ERROR] file not found:{file_path}"

        except Exception as e:
            return f"[upload failed] {type(e).__name__}: {str(e)}"

    def get_retriever(self):
        return self.chroma.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

