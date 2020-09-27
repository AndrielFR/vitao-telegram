# coding: utf-8
# API
from telegram.ext import *
from telegram import *

from modules.Module import Module
from modules._Message_Handler import _Message_Handler
from telegram.ext.dispatcher import run_async

# Configuration
from modules.Config import Configuration

import logger
import sys

# Compiler files
sys.dont_write_bytecode = True

class Bot():
    def __init__(self):
        self.config = Configuration()
        
    @run_async
    def textHandler(self, update, context):
        self.module = _Message_Handler(update, context)
        self.module._handler()
        
    def error_handler(self, update, context):
        print('error: "{0}"'.format(context.error))
                
if __name__ == '__main__':
    b = Bot()
    updater = Updater(token=b.config.token, use_context=True)
    
    updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.command | Filters.entity('MENTION'), b.textHandler))
    
    #updater.dispatcher.add_error_handler(b.error_handler)

    print('Starting bot...')
    updater.start_polling()
    print('Bot started!')