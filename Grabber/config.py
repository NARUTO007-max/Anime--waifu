import os
from urllib.parse import quote_plus

OWNER_ID = 7576729648
GROUP_ID = "-1002535643821"
TOKEN = "7929416862:AAHZrKaPqiIEmGf6oemjQT1truMPeQCn2-g"
api_id = 21218274
api_hash = "3474a18b61897c672d315fb330edb213"
PHOTO_URL = ["https://files.catbox.moe/oai7m9.mp4"]
SUPPORT_CHAT = "Animeheaven_community"
UPDATE_CHAT = "Animeheaven_community"
BOT_USERNAME = "Hinatawaifu_bot"
CHARA_CHANNEL_ID = -1002659827150

# MongoDB credentials — ENCODE them properly
mongo_user = quote_plus("waifu")
mongo_pass = quote_plus("yash2005@")

MONGO_URL = f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.ampo8t7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "waifu"
LOG_CHAT_ID = -1002535643821