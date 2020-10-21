from modules.Module import Module

from requests import exceptions, get, post

import random
import os

# Configuration
from modules.Config import Configuration

class upload(Module):
    def __init__(self, update, bot, command, message):
        self.bot = bot
        self.config = Configuration()
        
        self._message = update.message
        
        self.command = command
        self.message = message
        
        self.chat_id = update.message.chat.id
        
    def _handler(self):
        tx = self._message.reply_to_message
        message = self.message
        final_url = ''
        reply = 0
        
        self._send_action('typing')
        
        if message:
            pass
        elif tx:
            if tx.voice or tx.photo or tx.video or (tx.document and tx.document.file_name.endswith(('.zip', '.gif', '.mp3', '.mp4', '.tgz', '.tg'))):
                error = '***Formato de arquivo não suportado.***'
                self._send_message(error, self._message.message_id)
                return [False, error]
            if tx.document:
                file_name = '{1}-{0}'.format(tx.document.file_name, random.randint(0, 9999))
                 
                try:
                    file = self._get_file(tx.document.file_id)
                    file.download(custom_path='{0}{1}'.format(self.config.download_dir, file_name))
                except:
                    error = '***Arquivo muito pesado.***'
                    self._send_message(error, self._message.message_id)
                    return [False, error]
                    
                m_l = None
                with open(self.config.download_dir+file_name, 'rb') as fd:
                    m_l = fd.readlines()
                    
                message = ''
                for m in m_l:
                    message += m.decode('iso-8859-1')
                    
                os.remove(self.config.download_dir+file_name)
            else:
                message = tx.text
                
        if not self._delete_message(self._message.message_id):
            reply = self._message.message_id
        
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
                reply = tx.message_id
            self._send_message(r_te, reply)
            return[True]