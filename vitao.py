# coding: utf-8
# API
from telegram.ext import *
from telegram import *

import os
import json
import random
import sys

# Compiler files
sys.dont_write_bytecode = True

# Modules
from modules.Module import Module
from modules.TTS import TTS
from modules.TRT import TRT
from modules.search_YouTube import search_YouTube
from modules.upload import upload

class Bot():
    def __init__(self):
        self.OWNER = 'AndrielFR'
        self.DOWNLOAD_DIR = 'dl/'
        
        self.OWNER_CHAT_ID = 0
        self.CHAT_CONNECTED = 0
        
        self.ACTIVE = False
        
        self.module = Module()
    
    def run(self, updater):
        updater.start_polling()
    
    def _handler(self, bot, update):
        if not update.message:
            return
        if not update.message.text:
            return
        message = update.message.text
        if message.startswith('/') or message.startswith('!'):
            command = message.replace('/', '').replace('!', '').split(' ')[0].lower()
            message = message.replace('/{0} '.format(command), '').replace('!{0} '.format(command), '').replace('/{0}'.format(command), '').replace('!{0}'.format(command), '')

            if update.message.chat.username == self.OWNER:
                # /fowardon e fowardoff
                if command in ['fon', 'fowardon']:
                    bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                    if not self.ACTIVE:
                        self.ACTIVE = True
                        update.message.reply_markdown('***Acordei!***')
                    else:
                        update.message.reply_markdown('***Já estou acordado faz é tempo!***')
                elif command in ['foff', 'fowardoff']:
                    if self.ACTIVE:
                        self.ACTIVE = False
                        update.message.reply_markdown('***OK, indo dormir em: 3, 2, 1...***')
                    else:
                        update.message.reply_markdown('***Já estou dormindo...***')
            
                # /start ou /help
                if command in ['h', 'start', 'help']:
                    commandsMessage = "***Comandos:***    \n\n/connectchat ou cc id - me conecte ao chat indicado    \n/getchatmemberscount or gcmc id - verifique quantas pessoas há no chat indicado (se eu estiver nele)    \n/leavechat or lc id - me remova do chat indicado    \n/sendmessage or sm message - faça-me enviar uma mensagem ao chat em que estou conectado"
                    update.message.reply_markdown(commandsMessage)
                
                # /getmemberscount ou /gmc
                if command in ['gcmc', 'getchatmemberscount']:
                    bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                    try:
                        _chat = bot.get_chat(message)
                        membersCount = bot.get_chat_members_count(_chat.id)
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='O chat ```{0}``` contém ***{1}*** usuários.'.format(_chat.title, membersCount))
                    except:
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Me adicione ao chat antes')
                    
                # /leavechat ou lc
                if command in ['lc', 'leavechat']:
                    bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                    try:
                        bot.send_message(chat_id=self.CHAT_CONNECTED, parse_mode='MARKDOWN', text='Até um outro dia pessoal, eu amo vocês!')
                    except:
                        pass
                    try:
                        _chat = bot.get_chat(message)
                        bot.leave_chat(_chat.id)
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Sai com sucesso do chat: ```{0}```'.format(_chat.title))
                    except:
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text="Não foi possível sair do chat: ```{0}```".format(message))

                # /sendmessage ou sm
                if command in ['sm', 'sendmessage']:
                    bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                    try:
                        if self.CHAT_CONNECTED != 0:
                            bot.send_message(self.CHAT_CONNECTED, message)
                        else:
                            bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Use ***/connectchat id*** para me conectar ao chat indicado')
                    except:
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Me adicione ao chat antes')
                
                # /connectchat ou cc
                if command in ['cc', 'connectchat']:
                    bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                    try:
                        _chat = bot.get_chat(message)
                        self.CHAT_CONNECTED = _chat.id
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Me conectei ao chat: `{0}`'.format(_chat.title))
                    except:
                        bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Me adicione a esse chat antes')

                # /replymessage ou rm
                if command in ['rm', 'replymessage']:
                    bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                    message_id = message.split(' ')[0]
                    message = message.replace(message_id, '')
                    bot.send_message(chat_id=self.CHAT_CONNECTED, parse_mode='MARKDOWN', text=message, reply_to_message_id=message_id)

            # /gay
            if command in ['gay']:
                bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text=' ┈┈┈╭━━━━━╮┈┈┈┈┈ \n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈ \n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈ \n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈ \n┈┈╭┻┊┊╰━┻━╮┈┈┈┈ \n┈┈╰┳┊╭━━━┳╯┈┈┈┈ \n┈┈┈┃┊┃╰━━┫┈BAPAQ U GAY \n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈')
                
            # /chatid ou /cid
            if command in ['cid', 'chatid']:
               bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='O ***id*** do chat atual é: `{0}`'.format(update.message.chat.id))
                      
            # /tts
            if command.startswith('tts'):
                self.module = TTS(bot, update, command, message, update.message.chat.id)
                    
            # /trt ou translate
            if command in ['trt', 'translate']:
                self.module = TRT(bot, update, command, message, update.message.chat.id)
                
            # /yt ou youtube
            if command in ['yt', 'youtube']:
                self.module = search_YouTube(bot, update, command, message, update.message.chat.id)
                
            # /upload ou /up
            if command in ['up', 'upload']:
                self.module = upload(bot, update, command, message, update.message.chat.id)
                
            reh = self.module._handler()
            if not reh[0]:
                print(reh[1])
          
            return

        if update.message.chat.id == self.CHAT_CONNECTED:
            message = update.message.text
            message = str(message).lower()
            if self.ACTIVE:
                bot.send_message(chat_id=self.OWNER_CHAT_ID, parse_mode='MARKDOWN', text='***U:*** @{0}    \n***M: 👇🏾***\n{1}    \n\n***Responda:*** ``` {2} ```👆🏾'.format(update.message.from_user.username, update.message.text, '!rm '+str(update.message.message_id)))
            
            if 'babaluu' in message:
                update.message.reply_markdown('Me chamou?')
            elif 'bom dia' in message:
                update.message.reply_markdown('Você é gay!')
            elif 'gay' in message or 'baitola' in message or 'viado' in message:
                update.message.reply_markdown('Achei ofensivo, vou dizer que foi estupro.')
                
if __name__ == '__main__':
    b = Bot()
    updater = Updater(token= '' )
    
    updater.dispatcher.add_handler(MessageHandler(Filters.all, b._handler))

    b.run(updater)