from pyrogram import Client
from config import *
from handlers.game import register_game
from handlers.callbacks import register_callbacks

app = Client(
    "shadow_v2",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_game(app)
register_callbacks(app)

app.run()
