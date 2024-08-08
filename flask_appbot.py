import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort,render_template
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
    TextMessage #傳輸回Line 官方後台的資料格式
)
from linebot.v3.webhooks import (
    MessageEvent, #傳輸過來的方法
    TextMessageContent  #使用者傳過來的資料格式
)
import os,sys
app = Flask(__name__) 

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINEBOT_KEY', None)
channel_access_token = os.getenv('LINEBOT_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINEBOT_KEY as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINEBOT_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


handler=WebhookHandler(channel_secret)
configuration=Configuration(access_token=channel_access_token)

@app.route("/")  #裝飾器 :跟目錄要做什麼事
def say_hello_world(username=""):
    return render_template ("hello.html",name=username)


#設計一個callback的路由，提供給Line 官方後台去呼叫
#也就是所謂的呼叫Webhook Sever
#因為官方會把使用者傳輸的訊息轉傳給Webhook Sever
#所已會使Restful API 的 PORT 方法
@app.route("/callback", methods=['POST'])  
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

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


#根據不同的使用者事件(EVENT),用不同方式回應
#eg.MessageEvent 代表使用者單純傳訊息事件
#TextMessageContent 代表使用者傳輸的訊息內容是文字
#
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=event.message.text)
                ]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)