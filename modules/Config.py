from modules.Module import Module

class Configuration(Module):
    def __init__(self):
        self.token = ''
        self.owner_name = ['AndrielFR', 'Allan_dk', 'jeangraff30']
        self.download_dir = 'dl/'
        
        self.owner_chat_id = 0
        self.chat_connected = 0
        
        self.conversation = False