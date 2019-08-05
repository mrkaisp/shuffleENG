# インポートするライブラリ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import urllib.request
import os
import sys
import json
from argparse import ArgumentParser
import making_question

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sentences = event.message.text

    if sentences == 'how to use':
        result = '1行に1文ずつ英語を入力してください。並び替え問題の語群を返します。\n\n'\
        '【注意】\n'\
        '❶先頭文字が固有名詞の場合は、先頭に"_"(アンダーバー)を入力してください。\n'\
        '　e.g. _Kai is a good teacher.\n\n'\
        '❷セットで語群に入れたい単語同士は、"_"(アンダーバー)で繋いでください。\n'\
        '　e.g. Do you like Mr._Kai?\n\n'\
        '❸適語補充型の問題にしたい場合は、補充語を()で囲ってください。\n'\
        '　e.g. I\'ve been (to) America.\n\n'\
        '❹不要語を追加したい場合は、文の後に追加して入力してください。\n'\
        '　e.g. I\'ve been to America. visited'
    else:
        result = making_question.do(sentences)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
     )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
