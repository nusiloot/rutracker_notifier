# coding : utf-8
import requests
import json
from config import *
# Accessing telegram bot logs
url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
request = requests.get(url).text
# Converting data to json to extract chat_id
json_r = json.loads(request)
chat_id = json_r['result'][-1]['message']['from']['id']
# Writing chat_id to config file
f = open("config.py", 'a')
f.write("\n" + "chat_id = " + str(chat_id))
