from modules.Module import Module

from youtube_search  import YoutubeSearch

import json

class search_YouTube(Module):
    def __init__(self, bot, update, command, message, chat_id):
        self.bot = bot
        self._message = update.message
        self.command = command
        self.message = message
        self.chat_id = chat_id
        
    def _handler(self):
        if not self.message:
            error = 'O texto está vazio.'
            self._send_message(error, self._message.message_id)
            return [False, error]
        
        r = None
        try:
            r = json.loads(YoutubeSearch(self.message, max_results=1).to_json())
        except KeyError:
            error = 'Vídeo não encontrado'
            self._send_message(error, self._message.message_id)
            return [False, error]
            
        self._send_action('typing')
        
        o = ''
        for i in r["videos"]:
            try:
                o += '***Título:*** ```'+str(i["title"])+'```\n'
                o += '***Link:*** '+"https://youtube.com"+str(i["url_suffix"])+'\n'
                o += '***Canal:*** ```'+str(i["channel"])+'```\n'
                o += '***Duração:*** '+str(i["duration"])+'\n'
                o += '***'+str(i["views"])+'***\n'
            except IndexError:
                return [False, 'que']
                
        self._send_message(o, self._message.message_id)
        return [True]
        