# Task2：基于 RAG 的技术文档搜索与解释系统

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![LangChain](https://img.shields.io/badge/LangChain-≥0.2-orange)
![Chroma](https://img.shields.io/badge/Chroma-向量数据库-9cf)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-blueviolet)

**课程作业**：基于 LangChain + Chroma + DeepSeek 的 RAG 问答系统

## 项目概述

本项目实现了一个检索增强生成（RAG）技术文档智能问答系统，主要特点包括：

- 自动加载 `./rag_docs` 目录下的 PDF 文档
- 通过 MD5 校验实现文档幂等处理，避免重复向量化
- 使用 `RecursiveCharacterTextSplitter` 进行合理文本分块
- 嵌入模型：阿里云 DashScope `text-embedding-v4`
- 向量数据库：Chroma
- 生成模型：DeepSeek `deepseek-chat`
- 支持单次问答与多轮对话
- 回答严格基于检索到的文档内容，显著减少幻觉

## 项目结构
```text
Task2/
├── src/                    # 核心源代码
│   ├── main.py             # 命令行入口（单次 / 交互模式）
│   ├── rag.py              # RAG 核心服务逻辑（RagService 类）
│   ├── config.py           # 配置管理（模型、路径、API Key 等）
│   ├── knowledge_base.py   # 知识库管理（文档加载、分块、嵌入、检索）
│   ├── chat_history_store.py # 会话历史存储（内存实现，可扩展）
│   └── util.py             # 通用工具函数（MD5 计算等）
├── rag_docs/               # 原始文档目录（目前主要为 PDF）
│   └── 西安美食情况的研究.pdf
├── data/                   # 元数据、校验文件、缓存
│   └── md5.txt             # 已处理文档的 MD5 记录（防重复向量化）
├── chroma_db/              # Chroma 向量数据库持久化目录（已 gitignore）
├── .gitignore
├── requirements.txt
└── README.md
```


## 环境要求

- Python ≥ 3.9
- 推荐使用虚拟环境（venv / conda）

## 快速开始

```bash
### 1. 安装依赖

# 创建并激活虚拟环境
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

### 2. 配置 API Key（推荐用环境变量）

# Linux / macOS
export DASHSCOPE_API_KEY="sk-你的DashScope密钥"
export DEEPSEEK_API_KEY="sk-你的DeepSeek密钥"

# Windows (cmd)
set DASHSCOPE_API_KEY=sk-你的DashScope密钥
set DEEPSEEK_API_KEY=sk-你的DeepSeek密钥

### 3. 运行

# 单次问答
python src/main.py "西安有哪些著名小吃？"

# 交互式多轮对话
python src/main.py --mode chat

聊天模式支持指令：
/clear 或 /c    → 清空当前会话历史
/new   或 /n    → 开始全新会话
/exit  或 /e    → 退出程序

```

