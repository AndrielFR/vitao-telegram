from telegram.ext import *
from telegram import *

# Modules
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
import os

class Bot():
    def __init__(self):
        self.OWNER = 'AndrielFR'
        #self.CHAT_CONNECTED =  -1001493681484
        self.CHAT_CONNECTED = -1001297842259
        #self.CHAT_CONNECTED = -1001387940789
        self.ACTIVE = False
    
    def run(self, updater):
        updater.start_polling()
    
    def _handler(self, bot, update):
        if update.message.text == None:
            return
        message = update.message.text
        if message.startswith('/') or message.startswith('!'):
            #print(update)
            #print(update.message)
            command = message.replace('/', '').replace('!', '').split(' ')[0]
            message = message.replace('/{0} '.format(command), '').replace('!{0} '.format(command), '').replace('/{0}'.format(command), '').replace('!{0}'.format(command), '')

            if update.message.chat.username == self.OWNER:
                # /fowardon e fowardoff
                if command in ['fon', 'fowardon']:
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
                    try:
                        membersCount = bot.get_chat_members_count(message)
                        update.message.reply_markdown('O chat ```{0}``` contém ***{1}*** usuários.'.format(message, membersCount))
                    except:
                        update.message.reply_markdown("Não estou no chat: ```{0}```".format(message))
                    
                # /leavechat ou lc
                if command in ['lc', 'leavechat']:
                    try:
                        bot.send_message(message, "Até um outro dia pessoal, eu amo vocês!")
                    except:
                        pass
                    try:
                        bot.leave_chat(message)
                        update.message.reply_markdown('Sai com sucesso do chat: ```{0}```'.format(message))
                    except:
                        update.message.reply_markdown("Não estou no chat: ```{0}```".format(message))

                # /sendmessage ou sm
                if command in ['sm', 'sendmessage']:
                    try:
                        if self.CHAT_CONNECTED != 0:
                            bot.send_message(self.CHAT_CONNECTED, message)
                        else:
                            update.message.reply_markdown('Use ***/connectchat id*** para me conectar ao chat indicado')
                    except:
                        update.message.reply_markdown("Não estou no chat: ```{0}``` ou estou sem permissão".format(self.CHAT_CONNECTED))
                
                # /connectchat ou cc
                if command in ['cc', 'connectchat']:
                    self.CHAT_CONNECTED = message
                    update.message.reply_markdown('Me conectei ao chat: {0}'.format(message))

                # /replymessage ou rm
                if command in ['rm', 'replymessage']:
                    message_id = message.split(' ')[0]
                    message = message.replace(message_id, '')
                    bot.send_message(chat_id=self.CHAT_CONNECTED, parse_mode='MARKDOWN', text=message, reply_to_message_id=message_id)

            # /gay
            if command in ['gay']:
              bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text=' ┈┈┈╭━━━━━╮┈┈┈┈┈ \n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈ \n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈ \n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈ \n┈┈╭┻┊┊╰━┻━╮┈┈┈┈ \n┈┈╰┳┊╭━━━┳╯┈┈┈┈ \n┈┈┈┃┊┃╰━━┫┈BAPAQ U GAY \n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈')
                      
            # /tts
            if command in ['tts']:
                tx = update.message.reply_to_message
                message = message
                if message:
                    pass
                elif tx:
                    message = tx.text
                else:
                    return
                            
                try:
                    gTTS(message, lang='pt')
                except AssertionError:
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='O texto está vazio.')
                except RuntimeError:
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Erro enquanto carregava o dicionário de idiomas.')
                bot.send_chat_action(chat_id=update.message.chat.id, action='record_audio')
                tts = gTTS(message, lang='pt-br')
                tts.save('v.mp3')
                with open('v.mp3', 'rb') as a:
                    ll = list(a)
                    lc = len(ll)
                if lc == 1:
                    tts = gTTS(message, lang='pt-br')
                    tts.save('v.mp3')
                with open('v.mp3', 'rb') as a:
                    try:
                        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        bot.send_voice(chat_id=update.message.chat.id, voice=a)
                    except:
                        bot.send_voice(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, voice=a)
                    os.remove('v.mp3')
            return
        
        #print(update.message)
        if not self.ACTIVE:
            return

        if update.message.chat.id == self.CHAT_CONNECTED:
            message = update.message.text
            message = str(message).lower()
            bot.forward_message(chat_id=self.OWNER, from_chat_id=update.message.chat.id, message_id=update.message.message_id)
            bot.send_message(chat_id=self.OWNER, parse_mode='MARKDOWN', text='***ID da mensagem:*** ```'+str(update.message.message_id)+'``` 👆')
            if 'babaluu' in message:
                update.message.reply_markdown('Me chamou?')
            elif 'bom dia' in message:
                update.message.reply_markdown('Você é gay!')
            elif 'gay' in message or 'baitola' in message or 'viado' in message:
                update.message.reply_markdown('Achei ofensivo, vou dizer que foi estupro.')
                
    def group_handler(self, bot, update):
        if update.message.chat.id == self.CHAT_CONNECTED:
            pass

if __name__ == '__main__':
    b = Bot()
    updater = Updater(token= '')

    updater.dispatcher.add_handler(MessageHandler(Filters.all, b._handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.group, b.group_handler))

    b.run(updater)
