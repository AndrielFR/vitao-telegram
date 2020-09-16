from telegram.ext import *
from telegram import *

class Module():
    def __init__(self, bot=None, update=None, command='', message='', chat_id=0):
        self.bot = bot
        self.chat_id = chat_id
        
    def _handler(self):
        pass
        
    def _send_message(self, text, reply_to=0):
        if reply_to == 0:
            self.bot.send_message(chat_id=self.chat_id, parse_mode='MARKDOWN', text=text)
        else:
            self.bot.send_message(chat_id=self.chat_id, parse_mode='MARKDOWN', reply_to_message_id=reply_to, text=text)
            
    def _send_voice(self, voice, reply_to=0, caption=''):
        if reply_to == 0:
            self.bot.send_voice(chat_id=self.chat_id, parse_mode='MARKDOWN', voice=voice, caption=caption)
        else:
            self.bot.send_voice(chat_id=self.chat_id, parse_mode='MARKDOWN', reply_to_message_id=reply_to, voice=voice, caption=caption)
            
    def _send_audio(self, audio, reply_to=0, caption=''):
        if reply_to == 0:
            self.bot.send_voice(chat_id=self.chat_id, parse_mode='MARKDOWN', audio=audio, caption=caption)
        else:
            self.bot.send_voice(chat_id=self.chat_id, parse_mode='MARKDOWN', reply_to_message_id=reply_to, audio=audio, caption=caption)
            
    def _send_action(self, action):
        self.bot.send_chat_action(chat_id=self.chat_id, action=action)
        
    def _delete_message(self, message_id):
        self.bot.delete_message(chat_id=self.chat_id, message_id=message_id)