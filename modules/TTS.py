from modules.Module import Module

from gtts import gTTS

import os

class TTS(Module):
    def __init__(self, update, bot, command, message):
        self.bot = bot
        
        self._message = update.message
        
        self.command = command
        self.message = message
        
        self.chat_id = update.message.chat.id
        
    def _handler(self):
        slow = None
        if self.command == ('ttss'):
            slow = True
        else:
            slow = False
            
        tx = self._message.reply_to_message
        message = self.message
        reply = 0
        tts = None
        if message:
            pass
        elif tx:
            message = tx.text
        else:
            error = 'O texto está vazio.'
            self._send_message(error, self._message.message_id)
            return [False, error]
            
        if self._delete_message(self._message.message_id):
            if tx:
                reply= tx.message_id
        else:
            reply = self._message.message_id
                    
        try:
            self._send_action('record_audio')
            tts = gTTS(message, lang='pt-br', slow=slow)
            tts.save('v.mp3')
            with open('v.mp3', 'rb') as a:
                self._send_voice(a, reply)
            os.remove('v.mp3')
        except:
            error = 'Erro enquanto carregava o dicionário de idiomas.'
            self._send_message(error, self._message.message_id)
            return [False, error]
        return [True]
            