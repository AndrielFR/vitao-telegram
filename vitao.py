from telegram.ext import *
from telegram import *

class Bot():
    def __init__(self):
        self.OWNER = 1155717290
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
            message = message.replace('/{0} '.format(command), '').replace('!{0} '.format(command), '')

            if update.message.chat.id == self.OWNER:
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
            
                # /start or /help
                if command in ['h', 'start', 'help']:
                    commandsMessage = "***Comandos:***    \n\n/connectchat ou cc id - me conecte ao chat indicado    \n/getchatmemberscount or gcmc id - verifique quantas pessoas há no chat indicado (se eu estiver nele)    \n/leavechat or lc id - me remova do chat indicado    \n/sendmessage or sm message - faça-me enviar uma mensagem ao chat em que estou conectado"
                    update.message.reply_markdown(commandsMessage)
                
                # /getmemberscount or /gmc
                if command in ['gcmc', 'getchatmemberscount']:
                    try:
                        membersCount = bot.get_chat_members_count(message)
                        update.message.reply_markdown('O chat ```{0}``` contém ***{1}*** usuários.'.format(message, membersCount))
                    except:
                        update.message.reply_markdown("Não estou no chat: ```{0}```".format(message))
                    
                # /leavechat or lc
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

                # /sendmessage or sm
                if command in ['sm', 'sendmessage']:
                    try:
                        if self.CHAT_CONNECTED != 0:
                            bot.send_message(self.CHAT_CONNECTED, message)
                        else:
                            update.message.reply_markdown('Use ***/connectchat id*** para me conectar ao chat indicado')
                    except:
                        update.message.reply_markdown("Não estou no chat: ```{0}``` ou estou sem permissão".format(self.CHAT_CONNECTED))
                
                # /connectchat or cc
                if command in ['cc', 'connectchat']:
                    self.CHAT_CONNECTED = message
                    update.message.reply_markdown('Me conectei ao chat: {0}'.format(message))

                # /replymessage ou rm
                if command in ['rm', 'replymessage']:
                    message_id = message.split(' ')[0]
                    message = message.replace(message_id, '')
                    bot.send_message(chat_id=self.CHAT_CONNECTED, parse_mode='MARKDOWN', text=message, reply_to_message_id=message_id)

            else:
                if update.message.chat.type == 'private':
                    update.message.reply_markdown('Você não é meu dono, sai daqui!')
                else:
                    # /gay
                    if command in ['gay']:
                      bot.send_message(chat_id=self.CHAT_CONNECTED, parse_mode='MARKDOWN', reply_to_message_id=update.message.message_id, text=' ┈┈┈╭━━━━━╮┈┈┈┈┈ \n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈ \n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈ \n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈ \n┈┈╭┻┊┊╰━┻━╮┈┈┈┈ \n┈┈╰┳┊╭━━━┳╯┈┈┈┈ \n┈┈┈┃┊┃╰━━┫┈BAPAQ U GAY \n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈')
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
                
if __name__ == '__main__':
    b = Bot()
    updater = Updater(token= '1072219495:AAG3PxpnRIl-Ioj9GWGG0lnOyTJjUst71iY')

    updater.dispatcher.add_handler(MessageHandler(Filters.all, b._handler))

    b.run(updater)
