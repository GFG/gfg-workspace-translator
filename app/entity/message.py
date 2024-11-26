class Message:
    def __init__(self, message: dict) -> None:
        self.message = message
    
    def text(self):
        return self.message.get('formattedText') \
            or self.message.get('argumentText') \
            or self.message.get('text') \
            or ""
    
    def sender_id(self):
        sender_name = self.get(self.message, 'sender', 'name')
        if sender_name is None:
            return None
        return sender_name.split('/')[-1]

    def space_id(self):
        space_name = self.get(self.message, 'space', 'name')
        if space_name is None:
            return None
        return space_name.split('/')[-1]
    
    def thread_id(self):
        thread_name = self.get(self.message, 'thread', 'name')
        if thread_name is None:
            return None
        return thread_name.split('/')[-1]
    
    def is_threaded(self):
        return self.message.get('threadReply')
    
    def is_human(self):
        return self.get(self.message, 'sender', 'type') == 'HUMAN'

    @staticmethod
    def get(root: dict, *path):
        node = root
        for key in path:
            if node is None:
                return None
            node = node.get(key)
        return node