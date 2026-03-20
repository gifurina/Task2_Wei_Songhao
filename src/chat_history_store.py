"""
会话历史存储模块

使用 LangChain 的 InMemoryChatMessageHistory 实现简单的内存会话存储。
每个 session_id 对应一个独立的聊天历史记录。

主要接口：
    get_history(session_id) -> InMemoryChatMessageHistory
"""

from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]