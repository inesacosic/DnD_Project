"""import template chat"""

from llm_utils import TemplateChat
from base import DungeonMaster
from base import Player
import time

def run_console_chat(**kwargs):
    template_file = 'util/templates/dm_chat.json'
    chat = TemplateChat.from_file(template_file, **kwargs)


run_console_chat()
DM = DungeonMaster()
## start the server
## starts a background thread that accepts clients 
DM.start_server()




