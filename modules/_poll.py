from modules.Module import Module

class _poll(Module):
    def __init__(self, update, bot, command, message):
        self.bot = bot
        
        self._message = update.message
        
        self.command = command
        self.message = message
        
        self.chat_id = update.message.chat.id
        
    def _handler(self):
        # Abrir enquete
        if self.command in ['npll', 'newpoll']:
            message = self.message.split('\n')
            anonymous = True if message[0] in ['1', 'True'] else False
            question = message[0] if not message[0] in ['1', 'True', '0', 'False'] else message[1]
            awsners = self.message if not message[0] in ['1', 'True', '0', 'False'] else self.message[2:]
            awsners = awsners.replace(question+'\n', '')
            awsners = awsners.split('\n')
            reply = 0
            if len(awsners) > 10:
                error = 'Limite de respostas atingido (***10***)'
                self._send_message(error, self._message.message_id)
                return [False, error]
                
            self._send_action('typing')
            if not self._delete_message(self._message.message_id):
                reply = self._message.message_id
                
            if not self._new_poll(question, awsners, reply, anonymous):
                error = '***Uso incorreto do comando!***\nTente:\n ``` !npll 1\nTudo bem?\nSim\nNão ```'
                self._send_message(error, reply)
                return [False, error]
            return [True]
            
        # Fechar enquete
        if self.command in ['cpll', 'closepoll']:
            tx = self._message.reply_to_message
            message_id = 0
            reply = 0
            if tx:
                message_id = tx.message_id
            else:
                error = 'Responda a uma enquete ***minha***!'
                self._send_message(error, self._message.message_id)
                return [False, error]
                
            if tx.poll:
                if not tx.from_user.is_bot:
                    error = 'Essa enquete não é minha!'
                    self._send_message(error, self._message.message_id)
                    return [False, error]
                else:
                    if self._stop_poll(message_id):
                        self._delete_message(self._message.message_id)
                    else:
                        error = 'Não foi possível finalizar a enquete.'
                        self._send_message(error, self._message.message_id)
                        return [False, error]
            else:
                error = 'Isso não é uma enquete!'
                self._send_message(error, self._message.message_id)
                return [False, error]
             
            return [True]