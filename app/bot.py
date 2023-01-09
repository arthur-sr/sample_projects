import json
from datetime import datetime
import os
import traceback
from pathlib import Path

from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from .utils import aexec, write_log, write_error
from .subs_handler import SubsHandler


class BotService:
    def __init__(self, subs_handler: SubsHandler):
        self.read_config()
        write_log('START')
        self.subs_handler = subs_handler

        # initializing bot and command/echo handlers
        self.updater = Updater(token=os.environ.get('bot_token'), use_context=True)
        
        start_handler = CommandHandler(
            'start', self.start, 
            #Filters.user(user_id=int(os.environ.get('bot_admin_id')))
        )

        echo_handler = MessageHandler(
            Filters.text & 
            (~Filters.command), #& 
            #(Filters.user(username=os.environ.get('bot_admin_username'))), 
            self.echo,
            run_async=True
        )

        self.updater.dispatcher.add_handler(start_handler)
        self.updater.dispatcher.add_handler(echo_handler)

    
    def send_message(self, chat_id, lookup_key):
        try:
            if 'photo' in self.config[lookup_key]:
                #self.updater.bot.create_chat_invite_link()
                self.updater.bot.send_photo(
                    chat_id=chat_id,
                    photo=open(self.config[lookup_key]['photo'], 'rb'), 
                    caption=open(self.config[lookup_key]["text"], encoding='utf-8').read()
                )
            elif 'document' in self.config[lookup_key]:
                self.updater.bot.send_document(
                    chat_id=chat_id,
                    document=open(self.config[lookup_key]['document'], 'rb'),
                    caption=open(self.config[lookup_key]["text"], encoding='utf-8').read()
                )
            else:
                self.updater.bot.send_message(
                    chat_id=chat_id,
                    text=open(self.config[lookup_key]["text"], encoding='utf-8').read()
                )
        except Exception as err:
            msg = f'{"*"*10}\n' + repr(err) + '\n' + traceback.format_exc() + '\n'
            print(msg)

    
    def start(self, update: Update, context):
        print(update.effective_chat)
        
        self.send_message(update.effective_chat.id, lookup_key='greeting')
        
        user_id = update.effective_user.id
        username = update.effective_user.name

        write_log(f'/start ({user_id},{username})')
        
        self.subs_handler.add_sub({ 'user_id': user_id, 'username': username })
    
    def read_config(self):
        with open('messaging.json') as f:
            self.config = json.load(f)
        write_log('Messaging file was read')
    
    @aexec
    async def echo(self, update: Update, context):
        write_log(f'{update.message.text} ({update.effective_user.id},{update.effective_user.name})')
     
        # non-admin users are only logged
        if update.effective_user.name != os.environ.get('bot_admin_username'):
            return
        
        match update.message.text.split():
            case ['read']:
                self.read_config()
                self.updater.bot.send_message(chat_id=update.effective_chat.id, text='Messaging file was read')
        
            case ['test_send_to_subs']:
                self.read_config()
                self.test_send_message_to_subs()
            
            case ['send_to_subs']:
                self.read_config()
                self.send_message_to_subs()
            
            case ['who_subbed']:
                subs_file = 'Logs/subs.txt'
                subs = [f'{datetime.strftime(x.added, "%Y-%m-%d %H:%M:%S")} :: {x.username}' 
                    for x in self.subs_handler.get_subs()]
                
                Path(subs_file).write_text('\n'.join(subs), encoding='utf-8')
                
                self.updater.bot.send_document(
                    chat_id=update._effective_chat.id,
                    document=open(subs_file),
                    caption='Subbed to bot'
                )
            
            case other:
                self.updater.bot.send_message(chat_id=update.effective_chat.id, text='Unknown command')

    
    def test_send_message_to_subs(self):
        admin = self.subs_handler.get_sub_by_username(os.environ.get('bot_admin_username'))
        self.send_message(chat_id=admin.user_id, lookup_key='admins_message')
        print(f'sent test message to {admin.user_id}')
        write_log('Test message was sent to admin')


    def send_message_to_subs(self):
        for sub in self.subs_handler.get_subs():
            try:
                self.send_message(chat_id=sub.user_id, lookup_key='admins_message')
                print(f'sent message to {sub.username}')
            except Exception as err:
                msg = f'Failed to send message to user_id={sub.user_id}. Error:\n {err}'
                print(msg)
                write_error(msg)
        write_log('Messages were sent to subs and admin')

    
    def run(self):
        print('starting polling')
        self.updater.start_polling()


