from app.translator.__interface import Translator
from app.pubsub.publisher import Publisher
from app.pubsub.subscriber_pull import Subscriber

from app.service.chat import Chat
from app.entity.message import Message

class EventHandler:
    def __init__(self, translator: Translator, publisher: Publisher, subscriber: Subscriber) -> None:
        self.translator = translator
        self.publisher = publisher
        self.subscriber = subscriber

    def handle_event(self, event):
        match event.get('type', 'SPACE_MESSAGE'):
            case 'MESSAGE':
                self.handle_message(event)
            case 'SPACE_MESSAGE':
                self.handle_message(event)
            case 'ADDED_TO_SPACE':
                self.handle_added_to_space(event)
            case 'REMOVED_FROM_SPACE':
                self.handle_removed_from_space(event)
            case _:
                print(f'Unknown event type: {event}')

    def handle_message(self, event):
        message = Message(event.get('message', {}))
        if not message.is_human():
            return
        text = message.text()
        if not text:
            return
        print(f'Received message: {event}')
        if self.translator.support_context() and message.is_threaded():
            space_id = message.space_id()
            thread_id = message.thread_id()
            conversation = Chat().list_messages(space_id, thread_id)
            conversation = [Message(msg) for msg in conversation if Message(msg).is_human()]
        else:
            conversation = None
        translated = self.translator.translate(message, conversation)
        if translated == text:
            print(f'No need to translate: {text}')
            return
        response = Chat().send_message(
            text=translated,
            space_name=event['message']['space']['name'],
            thread_name=event['message']['thread']['name']
        )
        print(f'Sent message: {response}')

    def handle_added_to_space(self, event):
        space_id = event['space']['name'].split('/')[-1]
        self.publisher.added_to_space(space_id)
        print(f'Added to space: {space_id}')

    def handle_removed_from_space(self, event):
        space_id = event['space']['name'].split('/')[-1]
        self.publisher.removed_from_space(space_id)
        print(f'Removed from space: {space_id}')

if __name__ == '__main__':
    from app.translator.model_closesource import CloseTranslator
    
    event_handler = EventHandler(CloseTranslator(), None, None)
    
    space_id = 'AAAA-Z5PVtc'
    thread_id = 'mm373X-7j64'
    messages = Chat().list_messages(space_id=space_id, thread_id=thread_id)

    event_handler.handle_message({
        'message': messages[2]
    })

