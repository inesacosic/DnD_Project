
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import TemplateChat

class Trader:
    def __init__(self, **kwargs):
        self.template_file = 'util/templates/trader_chat.json'
        self.user_input = kwargs['user_input'] if 'user_input' in kwargs else None
        self.end_regex = r'TRADE(.*)DONE'
        # list to store trader conversation
        self.trader_log = []
    

    def run_console_chat(self, sign, **kwargs):
        chat = TemplateChat.from_file(
            sign='hello', 
            template_file = self.template_file,
            end_regex = self.end_regex
            )
        chat_generator = chat.start_chat()
        print(next(chat_generator))
        while True:
            try:
                message = chat_generator.send(self.user_input)
                print('Agent:', message)
                # add to the trader_log
                self.trader_log.append(message)
            except StopIteration as e:
                if isinstance(e.value, tuple):
                    print('Agent:', e.value[0])
                    ending_match = e.value[1]
                    print('Ending match:', ending_match)
                    self.trader_log = " ".join(self.trader_log)
                break

