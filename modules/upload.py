from modules.Module import Module

from requests import exceptions, get, post

import random

class upload(Module):
    def __init__(self, update, bot, command, message):
        self.bot = bot
        
        self._message = update.message
        
        self.command = command
        self.message = message
        
        self.chat_id = update.message.chat.id
        
    def _handler(self):
        tx = self._message.reply_to_message
        message = self.message
        final_url = ''
        
        self._send_action('typing')
        
        if message:
            pass
        elif tx:
            if tx.voice or tx.photo or tx.video:
                error = '***Formato de arquivo não suportado.***'
                self._send_message(error, self._message.message_id)
                return [False, error]
            if tx.document:
                if tx.document.file_name.endswith(('.zip', '.gif', '.mp4', '.tgz', '.tg')):
                    error = '***Formato de arquivo não suportado.***'
                    self._send_message(error, self._message.message_id)
                    return [False, error]
                    
                file_name = '{0}-{1}'.format(tx.document.file_name, random.randint(0, 9999))
                
                try:
                    file = self._get_file(tx.document.file_id)
                    file.download(custom_path='{0}{1}'.format(self.DOWNLOAD_DIR, file_name))
                except:
                    error = '***Arquivo muito pesado.***'
                    self._send_message(error, self._message.message_id)
                    return [False, error]
                    
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
                    self._delete_message(self._message.message_id)
                except:
                    pass
            self._send_message(r_te, tx.message_id)
            return[True]