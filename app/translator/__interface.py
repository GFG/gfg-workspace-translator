from .language_detector import LanguageDetector

from app.config import SUPPORTED_LANGUAGES, DEFAULT
from app.entity.message import Message

class Translator:
    def translate(self, message: Message, conversation: list[Message] = None, src: str=DEFAULT['source'], dst: str=DEFAULT['target']) -> str:
        raise NotImplementedError
    
    def support_context(self) -> bool:
        raise NotImplementedError
    
    @staticmethod
    def need_translation(text: str, src: str, dst: str) -> bool:
        if src not in SUPPORTED_LANGUAGES or dst not in SUPPORTED_LANGUAGES:
            raise ValueError("Unsupported language")
        if src == dst:
            return False
        if text == "":
            return False
        if LanguageDetector().detect(text) == dst:
            return False
        return True
    
    
