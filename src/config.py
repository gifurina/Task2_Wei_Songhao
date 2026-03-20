"""
项目配置文件
所有可配置的参数统一放在这里，便于维护和修改。

包含：
- MD5 防重文件路径
- Chroma 向量数据库配置
- splitter文本分割参数
- model模型名称与温度
- session会话配置

使用方式：
    import config
"""

#md5
md5_path = "./others/md5.txt"

#chroma
collection_name = "rag"
persist_directory = "./chroma_db"

#splitter
chunk_size = 600
chunk_overlap = 100
separators = [
    "\n\n",
    "\n",
    ".",
    ",",
    "?",
    "!",
    "。",
    "，",
    "？",
    "！",
    " ",
    ""
]

#model
chat_model_name="deepseek-chat"
chat_temperature=0.0
embedding_model_name = "text-embedding-v4"

#session
import uuid
new_session_id = str(uuid.uuid4())[:8]
session_config = {
    "configurable":{
        "session_id":new_session_id
    }
}