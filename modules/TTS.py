from modules.Module import Module

from gtts import gTTS

import os

class TTS(Module):
    def __init__(self, bot, update, command, message, chat_id):
        self.bot = bot
        self._message = update.message
        self.command = command
        self.message = message
        self.chat_id = chat_id
        
    def _handler(self):
        slow = None
        if self.command.startswith('ttss'):
            slow = True
        else:
            slow = False
            
        tx = self._message.reply_to_message
        message = self.message
        if message:
            pass
        elif tx:
            message = tx.text
        else:
            error = 'O texto está vazio.'
            self._send_message(error, self._message.message_id)
            return [False, error]
                    
        try:
            gTTS(message, lang='pt-br')
        except:
            error = 'Erro enquanto carregava o dicionário de idiomas.'
            self._send_message(error, self._message.message_id)
            return [False, error]
            
        self._send_action('record_audio')
        
        tts = gTTS(message, lang='pt-br', slow=slow)
        tts.save('v.mp3')
        with open('v.mp3', 'rb') as a:
            try:
                self._delete_message(self._message.message_id)
                if tx:
                    self._send_voice(a, tx.message_id)
                else:
                    self._send_voice(a)
            except:
                if tx:
                    self._send_voice(a, tx.message_id)
                else:
                    self._send_voice(a, self._message.message_id)
                    
        os.remove('v.mp3')
        return [True]
            