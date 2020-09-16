from telegram.ext import *
from telegram import *

# Modules
from bs4 import BeautifulSoup
from emoji import get_emoji_regexp
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from youtube_search  import YoutubeSearch
from requests import exceptions, get, post

import os
import json
import random

class Bot():
    def __init__(self):
        self.OWNER = 'AndrielFR'
        self.DOWNLOAD_DIR = 'dl/'
        
        self.OWNER_CHAT_ID = 0
        self.CHAT_CONNECTED =  0
        
        self.ACTIVE = False
    
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
                      
            # /tts
            if command.startswith('tts'):
                slow = None
                if command.startswith('ttss'):
                    slow = True
                else:
                    slow = False
                tx = update.message.reply_to_message
                message = message
                if message:
                    pass
                elif tx:
                    message = tx.text
                else:
                    return
                            
                try:
                    gTTS(message, lang='pt-br')
                except AssertionError:
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='O texto está vazio.')
                except RuntimeError:
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Erro enquanto carregava o dicionário de idiomas.')
                bot.send_chat_action(chat_id=update.message.chat.id, action='record_audio')
                tts = gTTS(message, lang='pt-br', slow=slow)
                tts.save('v.mp3')
                with open('v.mp3', 'rb') as a:
                    try:
                        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        if tx:
                            bot.send_voice(chat_id=update.message.chat.id, reply_to_message_id=tx.message_id, voice=a)
                        else:
                            bot.send_voice(chat_id=update.message.chat.id, voice=a)
                    except:
                        if tx:
                            bot.send_voice(chat_id=update.message.chat.id, reply_to_message_id=tx.message_id, voice=a)
                        else:
                            bot.send_voice(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, voice=a)
                    os.remove('v.mp3')
                    
            # /trt ou translate
            if command in ['trt', 'translate']:
                translator = Translator()
                tx = update.message.reply_to_message
                message = message
                if message:
                    pass
                elif tx:
                    message = tx.text
                else:
                    return
                            
                r_te = None
                try:
                    r_te = translator.translate(self.deEmojify(message), dest='pt')
                except:
                    return
                    
                bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                s_l = LANGUAGES[f"{r_te.src.lower()}"]
                t_l = LANGUAGES[f"{r_te.dest.lower()}"]
                r_te = f"De: ***{s_l.title()}***\nPara: ***{t_l.title()}***\n\n{r_te.text}"
                bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text=r_te)
                
            # /yt ou youtube
            if command in ['yt', 'youtube']:
                s = message
                if not s:
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='O texto está vazio.')
                    return
                
                r = None
                try:
                    r = json.loads(YoutubeSearch(s, max_results=1).to_json())
                except KeyError:
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='Vídeo não encontrado.')
                    
                bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                o = ''
                for i in r["videos"]:
                    try:
                        o += '***Título:*** ```'+str(i["title"])+'```\n'
                        o += '***Link:*** '+"https://youtube.com"+str(i["url_suffix"])+'\n'
                        o += '***Canal:*** ```'+str(i["channel"])+'```\n'
                        o += '***Duração:*** '+str(i["duration"])+'\n'
                        o += '***'+str(i["views"])+'***\n'
                    except IndexError:
                        break
                bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text=o)
            
            # /upload ou /up
            if command in ['up', 'upload']:
                tx = update.message.reply_to_message
                final_url = ''
                
                bot.send_chat_action(chat_id=update.message.chat.id, action='typing')
                
                if message:
                    pass
                elif tx:
                    if tx.document:
                        if tx.document.file_name.endswith(('.zip')):
                            bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=tx.message_id, text='***Formato de arquivo não suportado.***')
                            #return
                            
                        file_name = '{0}-{1}'.format(tx.document.file_name, random.randint(0, 9999))
                        
                        try:
                            file = bot.get_file(tx.document.file_id)
                            file.download(custom_path='{0}{1}'.format(self.DOWNLOAD_DIR, file_name))
                        except:
                            bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=tx.message_id, text='***Arquivo muito pesado.***')
                            return
                            
                        m_l = None
                        with open(self.DOWNLOAD_DIR+file_name, 'rb') as fd:
                            m_l = fd.readlines()
                        message = ''
                        for m in m_l:
                            message += m.decode('utf-8')
                        os.remove(self.DOWNLOAD_DIR+file_name)
                    else:
                        message = tx.text
                
                # del.dog
                dFail = False
                if not dFail:
                    url = 'https://del.dog/'
                    r = post(url + "documents", data=message.encode("utf-8"))
                    r_te = None
                    
                    if r.status_code == 200:
                        re = r.json()
                        key = re['key']
                        final_url = url+key
                        
                        r_te = (
                            "`Upload bem sucedido!`\n\n"
                            f"[Link Dogbin]({final_url})\n"
                            f"[Ver RAW]({url}raw/{key})"
                         )
                    else:
                        r_te = "`Falha ao se conectar com o del.dog`"
                        dFail = True
                     
                    if tx:
                        try:
                            bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        except:
                            pass
                    bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=tx.message_id, text=r_te)
                    
            # /chatid ou /cid
            if command in ['cid', 'chatid']:
               bot.send_message(chat_id=update.message.chat.id, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text='O id do chat atual é: `{0}`'.format(update.message.chat.id))
          
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
            
    def deEmojify(self, text):
            return get_emoji_regexp().sub("", text)
                
if __name__ == '__main__':
    b = Bot()
    updater = Updater(token= '') 

    updater.dispatcher.add_handler(MessageHandler(Filters.all, b._handler))

    b.run(updater)