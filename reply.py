import openai, os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def get_reply(messages):
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        reply = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as e:
        reply = f"發生錯誤: {str(e)}"
    return reply

# def generate_content_msg(stock_id):
    try:
        stock_id = int(stock_id)  # 確保轉為數字類型
    except ValueError:
        return f"無效的股票代號：{stock_id}"

    if stock_id == "大盤":
        stock_name = "大盤"
    elif stock_id in data:
        stock_name = data[stock_id]["股票名稱"]
    else:
        return f"找不到股號 {stock_id} 的資訊。"
    
    price_data = stock_price(stock_id)
    news_data = stock_news(stock_name)[:3]
    
    content_msg = '你現在是一位專業的證券分析師, \
        你會依據以下資料來進行分析並給出一份完整的分析報告:\n'
        
    content_msg += f'近期價格資訊:\n {price_data}\n'
    
    if stock_id != "大盤":
        stock_value_data = stock_fundamental(stock_id)
        content_msg += f'每季營收資訊：\n {stock_value_data}\n'
        
    content_msg += f'近期新聞資訊: \n {news_data}\n'
    content_msg += f'請給我{stock_name}近期的趨勢報告,請以詳細、\
        嚴謹及專業的角度撰寫此報告,並提及重要的數字, reply in 繁體中文'

    return content_msg

def angry_gpt(text):
    content_msg = text
    
    msg = [{
        "role": "system",
        "content": "你現在是『青心』的男朋友, 你很常犯錯，不管收到什麼樣的訊息都是在罵你\
        但你時常忘記被罵過什麼。先狡辯，再試著為了被罵的訊息道歉，用一些冷笑話或是諧音梗來安撫『青心』。"
    }, {
        "role": "user",
        "content": content_msg
    }]
    
    reply_data = get_reply(msg)

    return reply_data

print(angry_gpt('家裡很亂！'))