from telegram.ext import *
from telegram import *

class Module():
    def __init__(self, update=None, bot=None, command='', message=''):
        pass
        
    def _handler(self):
        pass
        
    def _send_message(self, text, reply_to=0, chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        try:
            if reply_to == 0:
               self.bot.send_message(chat_id=chat_id, parse_mode='MARKDOWN', text=text)
            else:
                self.bot.send_message(chat_id=chat_id, parse_mode='MARKDOWN', reply_to_message_id=reply_to, text=text)
            return True
        except:
            return False
            
    def _send_voice(self, voice, reply_to=0, caption='', chat_id = 0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        try:
            if reply_to == 0:
                self.bot.send_voice(chat_id=chat_id, parse_mode='MARKDOWN', voice=voice, caption=caption)
            else:
                self.bot.send_voice(chat_id=chat_id, parse_mode='MARKDOWN', reply_to_message_id=reply_to, voice=voice, caption=caption)
            return True
        except:
            return False
            
    def _send_audio(self, audio, reply_to=0, caption='', chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        try:
            if reply_to == 0:
                self.bot.send_voice(chat_id=chat_id, parse_mode='MARKDOWN', audio=audio, caption=caption)
            else:
                self.bot.send_voice(chat_id=chat_id, parse_mode='MARKDOWN', reply_to_message_id=reply_to, audio=audio, caption=caption)
            return True
        except:
            return False
            
    def _send_action(self, action, chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        try:
            self.bot.send_chat_action(chat_id=chat_id, action=action)
            return True
        except:
            return False
        
    def _delete_message(self, message_id, chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        try:
            self.bot.delete_message(chat_id=chat_id, message_id=message_id)
            return True
        except:
            return False
        
    def _get_chat(self, chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        result = None
        try:
            result = self.bot.get_chat(chat_id)
        except:
            result = False
        return result
        
    def _leave_chat(self, chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        try:
            self.bot.leave_chat(chat_id)
            return True
        except:
            return False
            
    def _get_members_count(self, chat_id=0):
        chat_id = chat_id if not chat_id == 0 else self.chat_id
        result = None
        try:
            result = self.bot.get_chat_members_count(chat_id)
        except:
            result = False
        return result
        
    def _get_file(self, file_id):
        result = None
        try:
            result = self.bot.get_file(file_id)
        except:
            result = False
        return result