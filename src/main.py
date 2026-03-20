"""
RAG 问答系统主程序入口

支持两种模式：
  - once : 单次问答后退出
  - chat : 进入多轮对话模式，支持 /clear /new 等指令

用法：
    python ./src/main.py "你的问题" [--mode once|chat]

依赖：
    - rag.py 中的 RagService
    - config.py 中的配置
"""
import config
from chat_history_store import get_history
from rag import get_rag_service
import argparse


def main():

    rag = get_rag_service()

    parser = argparse.ArgumentParser(
        description=" ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # 显示默认值
    )

    parser.add_argument(
        "user_input",
        help="Ask anything"
    )

    parser.add_argument(
        "--mode",
        choices=["once", "chat"],
        default="once",
        help="默认为once，即回答一次问题后exit退出程序，可选为chat模式，即多轮附带历史信息的聊天模式"
    )

    args = parser.parse_args()

    if args.mode == "once":

        rag.run(args.user_input)

        return 0
    elif args.mode == "chat":

        rag.run(args.user_input)

        user_input = input("\nyou:")

        while user_input.lower() not in ["/exit","/e"]:
            user_input = user_input.strip()

            if user_input.lower() in ["/clear", "/c"]:
                history = get_history(config.session_config["configurable"]["session_id"])
                history.clear()
                print("chat history cleared")
                user_input = input("\nyou：")
                continue

            if user_input.lower() in ["/new", "/n"]:
                import uuid
                new_id = str(uuid.uuid4())[:8]
                config.session_config["configurable"]["session_id"] = new_id
                print(f"New conversation started：{new_id}")
                user_input = input("\nyou:")
                continue

            rag.run(user_input)

            user_input = input("\n你：")
        return 0
    else :
        return 0

if __name__ == '__main__':
    main()