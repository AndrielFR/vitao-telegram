# coding: utf-8
from modules.Module import Module

import time
import traceback
import sys

# Compiler files
sys.dont_write_bytecode = True

# Modules
from modules.TTS import TTS
from modules.TRT import TRT
from modules.upload import upload
from modules.search_YouTube import search_YouTube
from modules._owner import _owner

# Configuration
from modules.Config import Configuration

class _Message_Handler(Module):
    def __init__(self, update, context):
        self.update = update
        self.bot = context.bot
        self.config = Configuration()

        self._message = update.message
        if self._message.text.startswith(('/', '!')):
            self.isCommand = True
            self.command = self._message.text.replace('/', '').replace('!', '').split(' ')[0].lower()
            self.message = self._message.text.replace('/{0} '.format(self.command), '').replace('!{0} '.format(self.command), '').replace('/{0}'.format(self.command), '').replace('!{0}'.format(self.command), '')
        else:
            self.isCommand = False
            self.command = ''
            self.message = self._message.text

        self.chat_id = update.message.chat.id

    def _handler(self):
        self.module = Module(self.update, self.bot)
        if self.isCommand:
            # Verificar ID do chat
            if self.command in ['cid', 'chatid']:
                self._send_message('O ***ID*** do chat atual é: ```{0}```'.format(self.chat_id), self._message.message_id)

             # Conversation Module
            if self._message.chat.username in self.config.owner_name:
                self.module = _owner(self.update, self.bot, self.command, self.message)

            # TTS Module
            if self.command in ['tts', 'ttss']:
                self.module = TTS(self.update, self.bot, self.command, self.message)

            # Translate Module
            if self.command in ['trt', 'translate']:
                self.module = TRT(self.update, self.bot, self.command, self.message)

            # Upload Module
            if self.command in ['up', 'upload']:
                self.module = upload(self.update, self.bot, self.command, self.message)

            # YouTube Module
            if self.command in ['yt', 'youtube']:
                self.module = search_YouTube(self.update, self.bot, self.command, self.message)

            # EXEC Module
            if self.command in ['exex']:
                if self._message.from_user.username in self.config.owner_name:
                    exec(compile(str(self.message), "<string>", "exec"))
                    self._send_message('Script executado com sucesso!', self._message.message_id)

        else:
            # Conversation Module
            if self._message.chat.username in self.config.owner_name:
                self.module = _owner(self.update, self.bot, 'sendmessage', self.message)

            if self._message.chat.id == self.config.chat_connected:
                if self.config.conversation:
                    self._send_message(text='***U:*** @{0}    \n***M: 👇🏾***\n{1}    \n\n***Responda:*** ``` {2} ```👆🏾'.format(self._message.from_user.username, self.message, '!rm '+str(self._message.message_id)), chat_id=self.config.owner_chat_id)
                    return

                for owner in self.config.owner_name:
                    owner_user = '@'+owner
                    if owner_user.lower() in self.message.lower():
                        self._send_message('No momento {0}, {1} está ocupado, deixe seu recado no grupo ou no privado, assim que ele tiver tempo ele vai lhe responder, obrigado pela atenção.'.format(self._message.from_user.first_name, owner), self._message.message_id)
                        return

        try:
            self.module._handler()
        except Exception as ERROR:
            l = open('./error.log', 'a')
            l.write('\n'+('='*25)+'\n- Tempo: {0}\n Erro: \n'.format(time.strftime("%d/%m/%Y - %H:%M:%S")))
            traceback.print_exc(file=l)
            l.close()
