import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

def send_msg(msg):
    api_id = 'your_id'
    api_hash = 'your_hash'
    token = 'your_token'
    message = msg

    phone = "+77777777777"

    # creating a telegram session and assigning
    # it to a variable client
    client = TelegramClient('session', api_id, api_hash)
    
    # connecting and building the session
    client.connect()

    if not client.is_user_authorized():
    
        client.send_code_request(phone)
        
        # signing in the client
        client.sign_in(phone, input('Enter the code: '))
    
    
    try:
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        receiver = InputPeerUser('user_id', 0)
    
        # sending message using telegram client
        client.send_message(receiver, message, parse_mode='html')
    except Exception as e:
        
        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e)
    
    # disconnecting the telegram session
    client.disconnect()
