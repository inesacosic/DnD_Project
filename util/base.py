from dndnetwork import DungeonMasterServer, PlayerClient
from llm_utils import TemplateChat, insert_params, tool_tracker
import requests

import datetime
import json

@tool_tracker
def process_function_call(function_call):
    name = function_call.name
    args = function_call.arguments

    return globals()[name](**args)

def create_character(character_class):
        # Use API for character creation based on chosen class
        url = f"https://www.dnd5eapi.co/api/2014/classes/{character_class.lower()}"
        payload = {}
        headers = {
        'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        data = response.json() 
        # create model for summarizing the response from the API
        summarizer = TemplateChat.from_file('util/templates/summary_chat.json', sign = 'hello')
        # insert the response from API into the models template
        params_summarizer = {'character_info': "\n".join(data)}
        for item in summarizer.messages:
                    item['content'] = insert_params(item['content'], **params_summarizer)
        # do some summarizing..
        response = summarizer.completion()
        summary = response.message.content
        return summary

def process_response(self, response):
    if response.message.tool_calls:
            # calls the function to g
            tool_call = process_function_call(response.message.tool_calls[0].function)
            params = {'class_information': tool_call}
            for item in self.messages:
                    item['content'] = insert_params(item['content'], **params)
            response = self.completion()
    return response

class DungeonMaster:
    def __init__(self):
        self.game_log = ['START']
        self.server = DungeonMasterServer(self.game_log, self.dm_turn_hook)
        # general DM template
        self.generalDM = TemplateChat.from_file('util/templates/dm_chat.json', sign='hello', process_response = process_response)
        # trader NPC template
        self.trader = TemplateChat.from_file(
                sign='hello', 
                template_file = 'util/templates/trader_chat.json',
                end_regex = r'TRADE(.*)DONE'
        )
        self.chat = self.generalDM

        self.start = True
        self.embedding_model = "nomic-embed-text"
        # selection template
        self.selection = TemplateChat.from_file('util/templates/selection_chat.json', sign = 'hello')
        self.initialize = True

    def start_server(self):
        self.server.start_server()

    def dm_turn_hook(self):
        dm_message = ''
        try:
            if self.start:
                # check if there was a previous game and load it into parameters
                self.chat.parameters |= {'context': self.get_latest_game()} 
                # store latest game as context in messages
                for item in self.chat.messages:
                    item['content'] = insert_params(item['content'], **self.chat.parameters)

                dm_message = self.chat.start_chat()
                self.start = False
            else: 
                # if there is any suspicion of user wanting to trade
                # check user request usuing selection prompt and 
                # run trader agent if user does indeed want to trade
                if self.server.switch is True:
                    selected = self.switch_prompts()
                    if selected['as'] == 'trader':
                        # switch to trader chat
                        self.chat = self.trader
                        if self.initialize == True:
                            dm_message = self.chat.start_chat()
                            self.initialize = False
                            return dm_message
                    self.server.switch = False
                
                # insert the current players name into the name parameter so DM can address current player by name
                params = {'name': self.server.current_client}
                for item in self.chat.messages:
                    item['content'] = insert_params(item['content'], **params)

                dm_message = self.chat.send('\n'.join(self.game_log))

            # Return a message to send to the players for this turn
            return dm_message 
        except StopIteration as e:
                # when the agent returns a message with end_regex handle it 
                if isinstance(e.value, tuple):
                    dm_message = e.value[0]
                    self.chat = self.generalDM
                    return dm_message
    
    def get_latest_game(self):
        # get current date and date two weeks ago
        now = int(datetime.datetime.now().timestamp()) 
        two_weeks_ago = now - 14 * 24 * 60 * 60 
        # get the collections where the date is greater than two weeks ago
        results = self.server.collection.get(
            where={"date": {"$gt": two_weeks_ago}}
        )

        if not results['metadatas']:
            print('No recent games found')
            return None
        # filter results to get only the ones with all currently joined players
        filtered_results = [
            (doc, meta) for doc, meta in zip(results["documents"], results["metadatas"])
            if all(player in meta["Players"] for player in self.server.joined_players)
        ]

        if not filtered_results:
            print('No games found with all current players')
            return None

        # Sort by date descending
        sorted_data = sorted(
            filtered_results,
            key=lambda x: x[1].get("date", 0),
            reverse=True
        )

        # return document portion of latest game
        latest_document = sorted_data[0][0]

        return latest_document
    
    def switch_prompts(self):
        # get the last 5 turns from the game log and insert into parameters
        recent_turns = " ".join(self.game_log[-5:])
        params =  {'ask': recent_turns}
        for item in self.selection.messages:
                item['content'] = insert_params(item['content'], **params)
        response = self.selection.completion() 
        selected = json.loads(response.message.content)
        # return to selected prompt
        return selected


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
