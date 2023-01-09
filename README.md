************ CONFIGURATION ***************
Following is assumed to run from bot directory (parent directory of app/ folder)

INSTALLATION (paste into command line):
    1) python -m pip install -r requirements.txt
    2) open '.env' file with your text editor and paste your bot_token and username into correstponding fields (inside '')

RUNNING APP (paste into command line):
    python run_bot.py

Requirements:
    1) Secret file: .env 
        File contains two fields:
        bot_token -- string token taken from @BotFather
        bot_admin_username -- username of bot administrator

    2) File with message configurations: messaging.json
        Fields of this file are straightforward

Bot writes logging location into ./Logs directory

Bot stores subsciptions info subscibers.db file.
Do not delete this file -- if deleted, subscribers info will be missed.


************ USAGE ***************
Following commands are available:

admin (user with telegram username as in .env file) supports three commands/messages:
    1) read -- reads messaging.json file and update messaging info
    2) send_to_subs -- send message ("admins_message" from messaging.json) to all subscribers
    3) test_send_to_subs -- same as send_to_subs but bot print only to admin. For testing of how output rendered
    4) /start -- return message that will be send to users when they start bot (i.e. text+photo)

    all other commands/messages are responded with "Unknown command" message

subscribers (all non-admin users) support one command/message:
    1) /start -- return greeting message, as defined in messaging.json (i.e. text+photo)

    bot will not respond to any other command/message from subscriber

***
Messages are set up in messaging.json file.
This file has following structure:
    "greetings" - set up of greeting message (i.e. message responding to /start command)
    "admins_message" - set up of message, which will be sent to all subscribers of the bot (send_to_subs command).

Each of these fields has subfields:
    "text" - path to text file to be sent
    "photo" - path to photo file to be sent
    "document" - path to document to be sent

Telegram does not allow to send both photo and document. 
So, if both "photo" and "document" are presented - only photo will be sent.

************ LOGGING ***************
Bot loggs (into 'Logs/logfile.log') incoming commands/messages from any user/admin. 
No spam limits set, so take care.
Also bot logs admin's actions:
    -- reading messaging file events
    -- sending messages events from admin (test and real ones)

Bot logs some captured errors into 'Logs/errors.log' 
