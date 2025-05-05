# Section 1
## Scenerios DM is capable of handling

1. Integrating previous established lore into current storytelling
2. Complex NPC interactions
3. Automated dice rolls for skills, combat, and saves
4. In depth character creation for new players 

# Section 2

1. By using RAG, I retrieved context from the most recent game for the given players. If context did exist, I stored it as a parameter for the model as {'context': ...}. Then, in my dm_chat.json (general DM template), I added a system prompt with told the llm that if there was context, it should be used as a starting point for the current game. I used the function insert_params() from llm_utils.py to insert the context into the prompt.

2. In this project I created a seperate agent to act as a trader (NPC). When the user inputs something that suggests they may want to make a trade, the user's input will be fed to an agent with the prompt given in selection_chat.json. This prompts checks whether the general dm agent or trader agent should be used based on the user's input. If the selection agent returns a response for trader, then the self.chat variable in base.py will switch to the trader agent to complete the trade. When the trade is finished, the agent will output a response containing the end_regex of 'TRADE(.*)DONE' which will switch the self.chat variable back to the general DM agent.

3.

4. To use the tool 'create_character' to help the DnD create character's for new players, I had to edit the dm_chat.json template to add a 'tools' section. I also edited the system prompt to let the agent know that it can use the 'create_character' tool when it needs to create a character for a player.  

# Section 3

3. 

4. I used a tool called 'create_character' which calls an API that provides information on classes from on DnD fifth addition. 
    1. The first step was to create the function, which calls the API and gets the response back. It uses a seperate summarize llm to summarize the information that the API responded with.
    2. I then created the process_response() function in base.py--which was based on the one provided in Lab 5--and I set the process_response in kwargs to this function when I create the self.generalDM object. I created the process_function_call() function, also based on Lab 5, in order for the agent to be able to use/be in scope of the create_character() function. I used the tool_tracker decorator on process_function_call(), from llm_utils, which tracks and logs calls to the function it decorates. 
    3. When the agent returns a response that uses the 'create_character' tool, the response will be processed using proccess_response() which calls process_function_call(), which calls create_character(), and then adds the response into the {{class_information}} parameter of the system prompt, and generates another response.

# Section 4

# Section 5

1. In the DungeonMasterServer class, I set up a function called set_up_chromadb() which creates a persistant chromadb client and creates a collection called 'dnd_knowledge'. If there is no collection named 'dnd_knowledge', it will create one, otherwise it will retrieve it. Throughout the game, I save user and DM responses into two lists, character_info_log and game_events_log, in attempt to help the DM recognize a players character info for future games. When all players leave the game, the function save_data() is called which stores all the game information from these lists along with the date and joined players into the chromadb collection. 
    1. When a new game starts, before the chat begins (in base.py) self.get_latest_game() which calculates the date two weeks ago based on the current date. It then finds all the documents in the servers chromadb collection from the past two weeks. The documents are filtered to get only the games which have all *currently* players joined. It sorts those documents by date descending and returns the latest document.
    2. If a document is found (returned) it inserts the document into the dm_chat.json template's system prompt that contains the {{context}} parameter.


# Section 6

# Section 7
