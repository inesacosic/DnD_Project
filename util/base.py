from dndnetwork import DungeonMasterServer, PlayerClient
from llm_utils import TemplateChat, insert_params
import requests

import datetime
import json


class DungeonMaster:
    def __init__(self):
        self.game_log = ['START']
        self.server = DungeonMasterServer(self.game_log, self.dm_turn_hook)
        self.chat = TemplateChat.from_file('util/templates/dm_chat.json', sign='hello')
        self.start = True
        self.embedding_model = "nomic-embed-text"

    def start_server(self):
        self.server.start_server()

    def dm_turn_hook(self):
        dm_message = ''
        # Do DM things here. You can use self.game_log to access the game log

        if self.start:

            # store the parameters 
            self.chat.parameters |= {'context': self.get_latest_game()} # latest game

            # store latest game as context in messages
            for item in self.chat.messages:
                item['content'] = insert_params(item['content'], **self.chat.parameters)

            dm_message = self.chat.start_chat()
            self.start = False
        else: 

            # insert the current players names into the name parameter so DM can address current player by name
            params = {'name': self.server.current_client}
            for item in self.chat.messages:
                item['content'] = insert_params(item['content'], **params)

            dm_message = self.chat.send('\n'.join(self.game_log))

        # Return a message to send to the players for this turn
        return dm_message 
    
    def get_latest_game(self):

        now = int(datetime.datetime.now().timestamp()) # current date
        two_weeks_ago = now - 14 * 24 * 60 * 60 # date two weeks ago

        results = self.server.collection.get(
            where = {"date": {"$gt": two_weeks_ago}} # get the collections where the date is greater than two weeks ago
        )

        if not results['metadatas']:
            print('No recent games found')
            return None
        
        # Sort by date descending
        sorted_data = sorted(
            zip(results["metadatas"], results["documents"]),
            key=lambda x: x[0]["date"],
            reverse=True
        )

        latest_document = sorted_data[0][1]
        return latest_document


    def create_character(character_class):
        # Use API for character creation based on chosen class
        url = f"https://www.dnd5eapi.co/api/2014/classes/{character_class}"


        payload = {}
        headers = {
        'Accept': 'application/json'
        }


        response = requests.request("GET", url, headers=headers, data=payload)

        data = json.loads(response.text)

        print(data)





class Player:
    def __init__(self, name):
        self.name = name
        self.client = PlayerClient(self.name)

    def connect(self):
        self.client.connect()

    def unjoin(self):
        self.client.unjoin()

    def take_turn(self, message):
        self.client.send_message(message)
