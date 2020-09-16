from modules.Module import Module

from googletrans import LANGUAGES, Translator
from emoji import get_emoji_regexp

class TRT(Module):
    def __init__(self, bot, update, command, message, chat_id):
        self.bot = bot
        self._message = update.message
        self.command = command
        self.message = message
        self.chat_id = chat_id
        
    def _handler(self):
        translator = Translator()
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
                    
        r_te = None
        try:
            r_te = translator.translate(self.deEmojify(message), dest='pt')
        except Exception as E:
            return [False, E]
            
        self._send_action('typing')
        s_l = LANGUAGES[f"{r_te.src.lower()}"]
        t_l = LANGUAGES[f"{r_te.dest.lower()}"]
        r_te = f"De: ***{s_l.title()}***\nPara: ***{t_l.title()}***\n\n{r_te.text}"
        self._send_message(r_te, self._message.message_id)
        
        return [True]
        
    def deEmojify(self, text):
        return get_emoji_regexp().sub("", text)