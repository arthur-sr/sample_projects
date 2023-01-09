import os 
from dotenv import load_dotenv

from .bot import BotService
from .subs_handler import SubsHandler

load_dotenv()

if not os.path.isdir('./Logs'):
    os.makedirs('./Logs')


subs_db_handler = SubsHandler()
telegram_bot = BotService(subs_db_handler)

