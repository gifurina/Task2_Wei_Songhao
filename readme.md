# 技术文档 RAG 智能问答系统

基于 **LangChain + Chroma + DeepSeek** 实现的轻量级 RAG（检索增强生成）问答工具，主要用于技术文档的语义搜索与精准回答。

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-≥0.2-orange)
![Chroma](https://img.shields.io/badge/Chroma-向量数据库-9cf)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-blueviolet)

## 项目目标

构建一个简单易用的命令行 RAG 系统，能够：

- 自动读取 `./rag_docs` 目录下的 PDF 文档
- 通过向量数据库进行语义检索
- 结合大语言模型生成**严格基于文档内容**的回答
- 支持多轮对话、历史记忆、会话切换
- 使用 MD5 实现文档幂等上传，避免重复向量化

## 核心功能

- PDF 文档自动加载与分块
- Chroma 持久化向量数据库
- MD5 防重机制
- 带上下文的多轮对话
- 严格依据检索内容回答

## 快速开始

### 1. 环境准备

```bash
# 建议使用 Python 3.10+
python -m venv venv
source venv/bin/activate      # Linux / macOS
# 或 Windows: venv\Scripts\activate

pip install -r requirements.txt