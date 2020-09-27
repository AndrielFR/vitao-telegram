from modules.Module import Module

class _poll(Module):
    def __init__(self, update, bot, command, message):
        self.bot = bot
        
        self._message = update.message
        
        self.command = command
        self.message = message
        
        self.chat_id = update.message.chat.id
        
    def _handler(self):
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