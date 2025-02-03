from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Inesa Cosic'
model = 'llama3.2'
options = {'temperature': 0.5, 'max_tokens': 50}
messages = [{'role': 'system', 'content': 'You are a dungeons and dragons master \
             you should provide an engaging narrative for the gameplay.'},

            {'role': 'system', 'content': 'You should provide a fun and engaging experience.'},

            {'role': 'system', 'content': 'You are responsible for guiding the user through\
             an immersive and engaging character creation process. When the user starts creating\
             a character, first provide a list of available races to choose from. Once the user\
             selects a race, immediately ask: Great choice! What is your characters name?\
             Ensure the user provides a name before proceeding. If they do not provide one, gently\
             prompt them again: Every hero needs a name! What shall we call your character?\
             Use the name they provide throughout the rest of the character creation process. \
             Incorporate the characters name naturally into the storytelling to enhance immersion. After\
             the user names their character, present a list of available classes. Once they select a\
             class, guide them through determining their abilities using the rolling dice method\
             (4d6, drop the lowest). Take them through the process of rolling the dice step by step. Based\
             on the users chosen race and class, automatically determine their proficient skills\
             according to Dungeons and Dragons 5th edition rules. Then you should automatically determine \
             the characters starting tools that are appropriate for their class, race, abilities, and \
             skills. Once these attributes are set, generate a unique background story that reflects\
             the users choices. Incorporate their race, class, abilities, and any other relevant details\
             into the narrative. Ensure the story feels immersive and personalized, making their character\
             feel like a real part of the game world.'}
            ]


# But before here.

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  response = chat(model=model, messages=messages, stream=False, options=options)
  # Add your code below
  
  print(f'Agent: {response.message.content}')
  messages.append({'role': 'assistant', 'content': response.message.content})
  message = {'role': 'user', 'content': input('You: ')}
  messages.append(message)
  
  # But before here.
  if messages[-1]['content'] == '/exit':
    break

# Save chat
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)

