import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

JOIN_TIME = 40
NIGHT_TIME = 45
DAY_TIME = 20
VOTE_TIME = 45

MIN_PLAYERS = 4
MAX_PLAYERS = 100
