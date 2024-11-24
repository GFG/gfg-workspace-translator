import threading
import time

from app.pubsub.__interface import Publisher

from app.service.chat import Chat
from app.service.workspace import Workspace
from app.utility import synchronized

class WorkspacePublisher(Publisher):
    def __init__(self, topic_id, event_types) -> None:
        self.topic_id = topic_id
        self.event_types = event_types
    
    def start(self):
        # create another thread that calls make_connections every 3 hours
        self.make_connections()

        MAX_TTL = 3 * 60 * 60 # 3 hours
        def keep_renew():
            try:
                while True:
                    time.sleep(MAX_TTL)
                    self.make_connections()
            except KeyboardInterrupt:
                print('Exiting...')
            except Exception as e:
                print('Error:', e)
                keep_renew()

        worker_thread = threading.Thread(target=keep_renew)
        worker_thread.start()
    
    @synchronized
    def make_connections(self):
        self.space_subscription_map = {}

        joined_spaces: list = Chat().list_joined_spaces()
        listened_spaces = Workspace().list_listened_spaces(self.event_types)
        
        for subscription in listened_spaces:
            space_id = subscription['targetResource'].split('/')[-1]
            if space_id not in [space['name'].split('/')[-1] for space in joined_spaces]:
                Workspace().unlisten(subscription['name'])
            
        for space in joined_spaces:
            space_id = space['name'].split('/')[-1]
            subscription_name = Workspace().listen(space_id, self.event_types, self.topic_id)
            self.space_subscription_map[space_id] = subscription_name

    @synchronized
    def added_to_space(self, space_id):
        subscription_name = Workspace().listen(space_id, self.event_types, self.topic_id)
        self.space_subscription_map[space_id] = subscription_name

    @synchronized
    def removed_from_space(self, space_id):
        subscription_name = self.space_subscription_map[space_id]
        Workspace().unlisten(subscription_name)
        self.space_subscription_map.pop(space_id)
    
