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
