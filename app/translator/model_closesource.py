from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.globals import set_verbose, set_debug
set_verbose(False)
set_debug(False)

import warnings
warnings.filterwarnings("ignore", module="langchain_core")

from app.translator.__interface import Translator

from app.entity.message import Message
from app.config import *

class CloseTranslator(Translator):
    def __init__(self) -> None:
        pass

    @staticmethod
    @lru_cache(maxsize=2)
    def get_model(src: str, dst: str):
        chosen_model = CLOSE_MODELS[USING_MODEL]
        model = init_chat_model(**chosen_model['config'])
        def translate(text: str, context: str = None) -> str:
            prompt = chosen_model['template'].format(
                src=SUPPORTED_LANGUAGES[src], 
                dst=SUPPORTED_LANGUAGES[dst], 
                context=context,
                text=text
            )
            response = model(prompt)
            return response.content
        return translate
    
    def support_context(self) -> bool:
        return True
    
    def translate(self, message: Message, conversation: list[Message] = None, src: str=DEFAULT['source'], dst: str=DEFAULT['target']) -> str:
        text = message.text()
        if not Translator.need_translation(text, src, dst):
            return text
        translator = self.get_model(src, dst)
        context = self.format_conversation(conversation) if conversation else None
        return translator(text, context)
    
    def format_conversation(self, conversation: list[Message]) -> str:
        return '\n'.join([f'<message sender-id="users/{msg.sender_id()}">\n{msg.text()}</message>' for msg in conversation])
        
if __name__ == "__main__":
    translator = CloseTranslator()
    
    message = Message({
        'text': "Xin chào, tôi là một con hải cẩu.",
        'sender': {
            'name': 'users/1234567890'
        },
        'space': {
            'name': 'spaces/0987654321'
        }
    })

    translated = translator.translate(message)
    print(translated)
