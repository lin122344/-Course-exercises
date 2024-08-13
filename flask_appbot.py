from flask import (
    Flask, 
    request, 
    abort, 
    render_template
)
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
     InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage  # 傳輸回Line官方後台的資料格式
)
from linebot.v3.webhooks import (
    MessageEvent, # 傳輸過來的方法
    TextMessageContent # 使用者傳過來的資料格式
)
import os
from handle_keys import get_secret_and_token
from openAI_APIKEY import chat_with_chatgpt
from CWA_OPENDAT import get_cities_weather


app = Flask(__name__) 
keys = get_secret_and_token() 
handler = WebhookHandler(keys['LINEBOT_KEY'])
configuration = Configuration(access_token=keys['LINEBOT_ACCESS_TOKEN'])

@app.route("/")
def say_hello_world(username=""):
    # 測試用，確定webhook server 有連通
    return render_template("hello.html", name=username)

@app.route("/callback", methods=['POST'])  
def callback():
#設計一個callback的路由，提供給Line 官方後台去呼叫
#也就是所謂的呼叫Webhook Sever
#因為官方會把使用者傳輸的訊息轉傳給Webhook Sever
#所已會使Restful API 的 PORT 方法
    # get X-Line-Signature header value
    signature = request.headers['x-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
#根據不同的使用者事件(EVENT),用不同方式回應
#eg.MessageEvent 代表使用者單純傳訊息事件
#TextMessageContent 代表使用者傳輸的訊息內容是文字
    user_id = event.source.user_id
    user_message= event.message.text #使用者傳過來的訊息
    api_key = keys["openAI_APIKEY"]

    if '今天天氣如何' in user_message:
        # 問天氣
        cwa_api_key = keys["METEOROLOGICAL-AI"]
        locations_name = ['臺中市']
        if locations_name:
             weather_data = get_cities_weather(cwa_api_key, locations_name)
         
        # 台中市:
        #     xxx: aaa 
        #     yyy: bbb
        #     zzz: ccc
             response = ""
             for location in weather_data: # 取得每一個縣市的名稱
                response += f"{location}:\n" # 加入縣市名稱訊息到response
                for weather_key in sorted(weather_data[location]): # 根據縣市名稱，取得縣市天氣資料
                    response += f"\t\t\t\t{weather_key}: {weather_data[location][weather_key]}\n"
             response = response.strip()
             response = chat_with_chatgpt(
                user_id,response, api_key,
                extra_prompt="請你幫我生出一段報導，根據前面的天氣資訊，建議使用者的穿搭等等，每個縣市分開，200字以內。"
            )
        else:
            response = "請給我你想知道的縣市，請輸入：特務P天氣如何 臺中市 桃園市 彰化市"
    else:
        # 閒聊
        response = chat_with_chatgpt(user_id, user_message, api_key)
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=response)
                ]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)