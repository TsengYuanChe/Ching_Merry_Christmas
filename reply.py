import openai
import os
from dotenv import load_dotenv
from db import fetch_history, save_to_db, search_message_in_history  # 引入搜尋函數

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def get_reply(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as e:
        reply = f"發生錯誤: {str(e)}"
    return reply

def angry_gpt(user_message):
    # 搜尋訊息是否出現在歷史中
    occurrences = search_message_in_history(user_message)

    if occurrences:
        # 如果訊息已出現，生成歷史時間的文字
        occurrence_text = "\n你在：\n" + "\n".join(occurrences) + "罵過同一件事：）"
    else:
        occurrence_text = "這是你第一次這樣罵我：（"

    # 獲取最近的對話歷史
    history = fetch_history()

    # 將歷史對話添加到 ChatGPT 的 prompt
    history_context = "\n".join([f"用戶: {user}\n回覆: {reply}" for user, reply, _ in history])

    system_message = (
        "你現在是『青心』的男朋友，你很常犯錯，不管收到什麼樣的訊息都是在罵你，"
        "但你時常忘記被罵過什麼。先狡辯，再試著為了被罵的訊息道歉，"
        "用一些聽得懂的冷笑話或是諧音梗來安撫『青心』。\n"
        "這是最近的對話歷史:\n"
        f"{history_context}\n"
    )

    # 組裝 ChatGPT 消息格式
    msg = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    # 獲取回覆
    reply_message = get_reply(msg)

    # 將歷史出現的時間追加到回覆中
    reply_message += occurrence_text

    # 儲存當前對話到資料庫
    save_to_db(user_message, reply_message)

    return reply_message