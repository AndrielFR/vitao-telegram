from modules.Module import Module

# Configuration
from modules.Config import Configuration

class _owner(Module):
    def __init__(self, update, bot, command, message):
        self.bot = bot
        self.config = Configuration()

        self._message = update.message

        self.command = command
        self.message = message

        self.chat_id = update.message.chat.id

    def _handler(self):
        # Sair do chat
        if self.command in ['lc', 'leavechat']:
            self._send_message(text='Até um outro dia pessoal, gostei de conhecer vocês.', chat_id=self.config.chat_connected)
            chat_id = self.message if self.message else self.config.chat_connected
            chat = self._get_chat(chat_id)
            if chat:
                if self._leave_chat(chat.id):
                    self._send_message('Sai com sucesso do chat: ```{0}```'. format(chat.title))
            else:
                self._send_message('Não foi possível sair do chat: ```{0}```'. format(chat_id))

        # Enviar mensagem
        if self.command in ['sm', 'sendmessage']:
            if not self._send_message(text=self.message, chat_id=self.config.chat_connected):
                self._send_message('Não foi possível enviar a mensagem.')

        # Responder mensagem
        if self.command in ['rm', 'replymessage']:
            message_id = self.message.split(' ')[0]
            message = self.message.replace(message_id, '')
            if not self._send_message(text=message, reply_to=message_id, chat_id=self.config.chat_connected):
                self._send_message('Não foi possível responder a mensagem. (Provável que tenha sido excluída ou era de um bot)')

        # Coletar números de membros no chat
        if self.command in ['gmc', 'getmemberscount']:
            chat_id = self.message if self.message else self.config.chat_connected
            chat = self._get_chat(chat_id)
            if chat:
                membersCount = self._get_members_count(chat_id)
                if membersCount:
                    self._send_message('O chat ```{0}``` contém ***{1}*** usuários.'.format(chat.title, membersCount))
                else:
                    self._send_message('Não foi possível coletar a quantidade de usuários.')
            else:
                self._send_message('Não foi possível coletar a quantidade de usuários.')
