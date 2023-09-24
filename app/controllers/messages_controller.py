import json
import logging
import random
from twilio.rest import Client

logger = logging.getLogger(__name__)
list_of_messages = json.loads(open('app/store/messages.json').read())
read_messages = []

def getTwilioClient():
    account_sid = 'ACe961eff7539e2fef6d26045fa3f4d23b'
    auth_token = 'a4b4ade582a76429b805c20ce61a1fb6'
    return Client(account_sid, auth_token)

def send_message(message, from_number, to_number):
    return getTwilioClient().messages.create(
        from_=f'whatsapp:{from_number}',
        body=message,
        to=f'whatsapp:{to_number}'
        )

class MessagesController:
    def send_whatsapp_message(message_body, to_number='+27749354595', from_number='+14155238886'):
        # pick random message
        logging.info('called---------------')
        message = random.choice(list_of_messages)
        if message not in read_messages: 
            response = send_message(message, from_number, to_number)
            read_messages.append(message)
        else:
            # fix this to ensure there are no duplicates
            message = random.choice(list_of_messages)
            response = send_message(message, from_number, to_number)
            read_messages.append(message)
        logger.info(response.status)
        return 'whatsapp message sent', 201
    
    def send_sms_message(message_body, to_number='+27749354595', from_number='+14155238886'):
        # pick random message
        message = random.choice(list_of_messages)
        if message not in read_messages: 
            response = send_message(message, from_number, to_number)
            read_messages.append(message)
        else:
            # fix this to ensure there are no duplicates
            message = random.choice(list_of_messages)
            response = send_message(message, from_number, to_number)
            read_messages.append(message)
        logger.info(response.status)
        return 'sms message sent', 201
    
    def get_message_history(to: str, from_: str):
        return getTwilioClient().messages.list(to='+27749354595', from_='+14155238886')



