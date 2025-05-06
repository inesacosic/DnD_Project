# Section 1--**Base System Functionality**
## Specific Scenerios DM is capable of handling

1. Integrating previous established lore into current storytelling
2. Complex NPC interactions
3. In depth character creation for new players 

The numbers in the following sections correspond to what scenerio they help implement

# Section 2--**Prompt Engineering and Model Parameter Choice**

1. By using RAG, I retrieved context from the most recent game for the given players. If context did exist, I stored it as a parameter for the model as {'context': ...}. Then, in my **dm_chat.json** (general DM template), I added a system prompt which stated that if there was context, it should be used as a starting point for the current game. I used the function insert_params() from llm_utils.py to insert the context into the prompt. The *temperature* of this template is set to 0.5 because I want the model to provide a creative gameplay but not be too random/wild. The *max_tokens* option is set to 100, as I believe it to be a "happy medium" for response length.

2. In this project I created a seperate agent to act as a trader (NPC). When the user inputs something that suggests they may want to make a trade, the user's input will be fed to an agent with the prompt given in **selection_chat.json.** This prompts checks whether the general dm agent or trader agent should be used based on the user's input. It has a *temprature* set to 0 because it's job is to decide between DM or trader, without creativity. The *max_tokens* option is set to 50 since, in general, this agent should only generate a one line response. 
    1. If the selection agent returns a response for trader, then the self.chat variable in base.py will switch to the trader agent to complete the trade, which uses **trader_chat.json** template. When the trade is finished, the agent is instructed to output a response containing the end_regex of 'TRADE(.*)DONE' which will switch the self.chat variable back to the general DM agent. The *temperature* for this template is set to 0.4, since it should be creative but not so creative that it takes too long to generate the end regex. The *max_tokens* are set to 100, similar to the general DM template. 

3. To use the tool 'create_character' to help the DnD create character's for new players, I had to edit the **dm_chat.json** template to add a 'tools' section. I also edited the system prompt to let the agent know that it can use the 'create_character' tool when it needs to create a character for a player.  

# Section 3--**Tools Usage**

3. I used a tool called 'create_character' which calls an API that provides information on classes from on DnD fifth addition. 
    1. The first step was to create the function, which calls the API and gets the response back. It uses a seperate summarize llm to summarize the information that the API responded with.
    2. I then created the process_response() function in base.py--which was based on the one provided in Lab 5--and I set the process_response in kwargs to this function when I create the self.generalDM object. I created the process_function_call() function, also based on Lab 5, in order for the agent to be able to use/be in scope of the create_character() function. I used the tool_tracker decorator on process_function_call(), from llm_utils, which tracks and logs calls to the function it decorates. 
    3. When the agent returns a response that uses the 'create_character' tool, the response will be processed using proccess_response() which calls process_function_call(), which calls create_character(), and then adds the response into the {{class_information}} parameter of the system prompt, and generates another response.

# Section 4--**Planning and Reasoning**

2. I used few shot learning in some templates, including **trader_chat.json** and **selection_chat.json**. In trader chat I gave the system prompt examples of what it should be outputting when it makes a trade. In the selection template I provided several messages with different roles, including assistant and user, to exemplify what the assistant should be generating based on what the user inputs.

3. One issue I ran into while trying to integrate the 'create_character' tool call was that I noticed the agent would call the tool uneccessarily and too often. In order to prevent this, I had to edit the system prompt to use chain-of-thought thinking when going through character creation. Specifically, I stated that the following steps should be used to create a character: (1) ask for a character's class (2) use the 'create_character' tool (3) add characters abilities. I told the model that they should follow this process step-by-step (chain-of-thought)


# Section 5--**Rag Implementation**

1. In the DungeonMasterServer class, I set up a function called set_up_chromadb() which creates a persistant chromadb client and creates a collection called 'dnd_knowledge'. If there is no collection named 'dnd_knowledge', it will create one, otherwise it will retrieve it. Throughout the game, I save user and DM responses into two lists, character_info_log and game_events_log, in attempt to help the DM recognize a players character info for future games. When **all** players leave the game, the function save_data() is called which stores all the game information from these lists along with the date and joined players into the chromadb collection. 
    1. When a new game starts, before the chat begins (in base.py) self.get_latest_game() which calculates the date two weeks ago based on the current date. It then finds all the documents in the servers chromadb collection from the past two weeks. The documents are filtered to get only the games which have all *currently* players joined. It sorts those documents by date descending and returns the latest document.
    2. If a document is found (returned) it inserts the document into the dm_chat.json template's system prompt that contains the {{context}} parameter.


# Section 6--**Additional Tools/Innovation**

For this project, I tried to implement text-to-audio using a model from HuggingFace, which is what the code in audio_generator.py was for. However, unfortunatelty I was not able to successfully implement this section of the project. My hope was that I could use the audio generator to produce an audio when the model gave a specific description of a setting. For example if the model were to describe the character being in a forest, an audio of a spooky forest with rustling leaves would be created.

