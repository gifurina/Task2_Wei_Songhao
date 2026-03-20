"""
RAG (Retrieval-Augmented Generation)核心服务模块

提供 RagService 类，整合：
- 文档加载与向量化
- 向量检索
- 提示词模板
- DeepSeek大模型调用
- 带历史记忆的对话链

单例模式获取实例：get_rag_service()
"""
import config
from pathlib import Path
from knowledge_base import KnowledgeBase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, \
    RunnableLambda, RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from chat_history_store import get_history

_rag_service_instance = None


def get_rag_service():
    """Get the unique RagService instance"""
    global _rag_service_instance
    if _rag_service_instance is None:
        print("initialize RagService ...")

        embedding = DashScopeEmbeddings(model=config.embedding_model_name)
        _rag_service_instance = RagService(embedding=embedding)
    return _rag_service_instance

class RagService:
    def __init__(self,embedding):
        try:
            self.embedding = embedding

            self.knowledge_base = KnowledgeBase(embedding)
            print("Vector database connected successfully")

            self._loaded_files = set()
            self.load_all_documents()

        except Exception as e:
            print("failed to initialize RAG system")
            print(f"[ERROR]：{type(e).__name__}: {str(e)}")
            raise



        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业、严谨的技术文档问答助手。
            请严格依据以下[参考资料]来回答用户问题。
            - 如果资料中能找到答案，请尽量引用原文
            - 如果资料中没有相关信息，请直接说“当前资料暂无相关内容”，不要编造
            - 回答要准确、简洁、结构清晰"""),

            ("system", "参考资料如下：\n{context}\n"),

            MessagesPlaceholder("chat_history"),

            ("human", "{input}")
        ])

        self.chat_model = ChatDeepSeek(
            model=config.chat_model_name,
            temperature=config.chat_temperature,
        )

        self.chain = self.__get_chain()

    def __get_chain(self):

        def format_docs(docs: list[Document]) -> str:

            if not docs:
                return "no reference"

            parts = []
            for idx, doc in enumerate(docs, 1):
                source = doc.metadata.get("source", "unknown").split("/")[-1]
                page = doc.metadata.get("page")
                page_str = f"page:{page + 1}" if page is not None else "unknown"

                content = doc.page_content.strip()
                if len(content) > 800:
                    content = content[:780] + "..."

                block = (
                    f"[reference] {idx}\n"
                    f"source：{source}  {page_str}\n"
                    f"content：\n{content}\n"
                    f"{'─' * 60}\n"
                )
                parts.append(block)

            return "\n".join(parts)

        def format_for_retriever(value):
            return value["input"]

        def format_for_prompt(value):
            new_value = {
                "input": value["input"]["input"],
                "context": value["context"],
                "chat_history": value["input"]["chat_history"],
            }
            return new_value
        parallel = RunnableParallel(
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | self.knowledge_base.get_retriever() | RunnableLambda(format_docs),
            }
        )

        chain = parallel | RunnableLambda(format_for_prompt) |self.prompt_template | self.chat_model | StrOutputParser()

        chat_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        return chat_chain

    def load_all_documents(self, directory: str = "./rag_docs"):
        folder = Path(directory)
        if not folder.is_dir():
            print(f"directory not found:{directory}")
            return

        pdf_files = list(folder.glob("*.pdf"))
        if not pdf_files:
            print("no pdf files found in directory")
            return

        print(f"{len(pdf_files)}pdf files found")
        print("loading documents...")
        for pdf in pdf_files:
            self.load_file(str(pdf))

    def load_file(self, file_path: str):
        if file_path in self._loaded_files:
            print(f"this file uploaded,skip：{file_path}")
            return "already loaded"
        result = self.knowledge_base.upload_by_pdf(file_path)
        if "successfully" in result:
            self._loaded_files.add(file_path)
        return result

    def run(self, user_input: str):
        try:
            ai_res = self.chain.stream(
                input={"input": user_input},
                config=config.session_config
            )

            print("\nAI answer:", end="", flush=True)
            for chunk in ai_res:
                print(chunk, end="", flush=True)
            print()

        except Exception as e:
            print(f"failed to generate AI answer")
            print(f"[ERROR]：{type(e).__name__}: {str(e)}")

