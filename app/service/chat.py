from googleapiclient.discovery import build

from app.credential.credential import CredentialStore

from app.service.__interface import Service

class Chat(Service):
    def __init__(self):
        self.service = build(
            'chat',
            'v1',
            credentials=CredentialStore().get_service_account(),
        )
        self.client = build(
            'chat',
            'v1',
            credentials=CredentialStore().get_client_secrets(),
        )

    def list_joined_spaces(self):
        spaceTypes = ['GROUP_CHAT', 'SPACE']
        filter = ' OR '.join([f'spaceType = "{spaceType}"' for spaceType in spaceTypes])
        response = self.service.spaces().list(filter=filter).execute()
        spaces = response.get('spaces', [])
        if response.get('nextPageToken'):
            response = self.service.spaces().list(
                pageToken=response['nextPageToken'],
                filter=filter
            ).execute()
            spaces += response.get('spaces', [])
        return spaces
    
    def get_space(self, space_id):
        space_name = f'spaces/{space_id}'
        return self.service.spaces().get(name=space_name).execute()
    
    def send_message(self, text, space_name, thread_name):
        body = {
            'text': text,
            'thread': {
                'name': thread_name
            },
            'threadReply': True
        }

        # Send the translated text back to the chat
        return self.service.spaces().messages().create(
            parent=space_name,
            threadKey=thread_name,
            messageReplyOption='REPLY_MESSAGE_OR_FAIL',
            body=body
        ).execute()
    
    def list_messages(self, space_id, thread_id, k=None):
        if space_id is None or thread_id is None:
            return []
        parent = f'spaces/{space_id}'
        filter = f'thread.name = spaces/{space_id}/threads/{thread_id}'
        response = self.client.spaces().messages().list(
            parent=parent,
            filter=filter,
        ).execute()
        messages = response.get('messages', [])
        if response.get('nextPageToken'):
            response = self.client.spaces().messages().list(
                parent=parent,
                filter=filter,
                pageToken=response['nextPageToken']
            ).execute()
            messages += response.get('messages', [])
        print(messages)
        if k is not None and len(messages) > k:
            messages = messages[-k:]
        return messages
    
if __name__ == '__main__':
    messages = Chat().list_messages('AAAAw4bmK6k', 'gvZBtxk6udE', 5)
    print(messages)
    def formatConversation(messages):
        result = []
        messages = list(filter(lambda message: message['sender']['type'] == 'HUMAN', messages))
        for message in messages:
            text = message['formattedText']
            sender = message['sender']['name']
            result.append(f'<message sender="{sender}">\n{text}\n</message>')
        return '\n'.join(result)
    print(formatConversation(messages))