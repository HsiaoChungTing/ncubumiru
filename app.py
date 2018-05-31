from flask import Flask, request, abort
import urllib.request, csv,io
import csv
import os
import pandas as pd
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,LocationSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('ji5ViJGJJbrK98TNdP7iZWapHB/aa641sii8w+3+Z+YSYk53vd+DZkuinEFyDrKGmporIGRv0WMehlx/AhE6S/oaqIh6Q1VUjmCSqvL9rXRczxFdaA/3bEiz9mR/M1hJkngqaPn0YdQ7zCk3YhN/bgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d9ad094e60d5296a04c2ef4f13396896')

@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    say='沒找到指定地點'
    find=False
    user_input=event.message.text
    url = 'https://raw.githubusercontent.com/TimShiao/nac-bumilu/master/location.txt'
    response = urllib.request.urlopen(url)
    loc_list= pd.read_csv(response, sep=',', names=['title', 'latitude', 'longtitude', 'location','keyword'])
    for i in range(len(loc_list)):
        if user＿input==loc_list.iloc[i][4]:
            say=loc_list.iloc[i][0]
            say_loc=loc_list.iloc[i][3]
            lati=loc_list.iloc[i][1]
            longti=loc_list.iloc[i][2]
            find=True
            break
    if find==True:
        location_message = LocationSendMessage(
        title='請點擊查看地圖',
        address=say,
        latitude=lati,
        longitude=longti
        )
        text_message_loc = TextSendMessage(text="位於"+say_loc)
        text_message_title = TextSendMessage(text=say)
        list_message=[text_message_title,location_message,text_message_loc]
        line_bot_api.reply_message(
            event.reply_token,list_message)
    else :
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=say))
if __name__ == "__main__":
	app.run()
