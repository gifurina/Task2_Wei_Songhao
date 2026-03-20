
# Task2：基于 RAG 的技术文档搜索与解释系统

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-≥0.2-orange)
![Chroma](https://img.shields.io/badge/Chroma-向量数据库-9cf)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-blueviolet)

**课程作业**：基于 LangChain + Chroma + DeepSeek 的 RAG 问答系统

## 项目概述

本项目实现了一个**检索增强生成（RAG）**技术文档问答系统，主要功能包括：

- 自动加载 `./rag_docs` 目录下的 PDF 技术文档
- 使用 MD5 校验实现文档幂等上传，避免重复向量化
- RecursiveCharacterTextSplitter 进行智能文本分块
- DashScope `text-embedding-v4` 模型向量化
- Chroma 持久化向量数据库
- DeepSeek `deepseek-chat` 大模型生成回答
- 支持单次问答 & 多轮对话模式（带历史记忆）
- 严格基于检索到的文档内容回答，减少幻觉

## 项目结构
Task2/
├── src/
│   ├── rag.py                # RAG 核心服务（RagService 类）
│   ├── main.py               # 命令行入口（单次/多轮模式）
│   ├── config.py             # 统一配置文件
│   ├── knowledge_base.py     # Chroma 向量库管理
│   ├── chat_history_store.py # 会话历史内存存储
│   └── util.py               # MD5 工具函数
├── rag_docs/                 # 原始文档目录（PDF）
│   └── 西安美食情况的研究.pdf
├── others/                  
│   └── md5.txt               # 已上传文件 MD5 记录
├── chroma_db/                # Chroma 向量数据库持久化目录（.gitignore 忽略）
├── .gitignore
├── requirements.txt
└── README.md

## 环境要求

- Python ≥ 3.9
- 推荐使用虚拟环境

## 快速开始

### 1. 安装依赖

```bash

# 创建并激活虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# 或 Linux/macOS
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# os.environ["DASHSCOPE_API_KEY"] = "your DashScope api_key"
# os.environ["DEEPSEEK_API_KEY"] = "your DeepSeek api_key"

# 直接问一个问题
python src/main.py "西安有哪些著名小吃？"

# 进入聊天模式
python src/main.py --mode chat

# 支持的指令：
# /clear 或 /c   → 清空当前会话历史
# /new   或 /n   → 开始一个全新的会话（新 session_id）
# /exit  或 /e   → 退出程序

you: 西安有哪些著名小吃？
AI answer: ...

you: 再推荐几家店
AI answer: ...

you: /clear
chat history cleared

you: /new
New conversation started: abc12345