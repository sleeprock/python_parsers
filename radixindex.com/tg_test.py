import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

def send_msg(msg):
    api_id = '16161285'
    api_hash = 'b17ff295a7a8d09078ecbeb3d55456cf'
    token = '5445633818:AAG62XdnHCyppAbzweK-L6URKlwjxh91cOk'
    message = msg

    phone = "+79787452726"

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
        receiver = InputPeerUser(195021413, 0)
    
        # sending message using telegram client
        client.send_message(receiver, message, parse_mode='html')
    except Exception as e:
        
        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e)
    
    # disconnecting the telegram session
    client.disconnect()