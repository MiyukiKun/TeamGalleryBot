import os
from telethon import TelegramClient
from pymongo import MongoClient


api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
main_group_id = int(os.environ.get("MAIN_GROUP_ID"))
main_bot_id = int(os.environ.get("BOT_ID"))
main_bot_token = os.environ.get('MAIN_BOT_TOKEN')
inline_bot_token = os.environ.get('INLINE_BOT_TOKEN')
db_url = os.environ.get('MONGO_DB_URL')

client = MongoClient(db_url, tls=True)

bot1 = TelegramClient('bot', api_id, api_hash).start(bot_token=main_bot_token)
bot = TelegramClient('bot1', api_id, api_hash).start(bot_token=inline_bot_token)
