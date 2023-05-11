from flask import request
from bot_app import app
from openai.error import AuthenticationError
from bot_app.open_ai import openai_response
from bot_app.methods import send_message, send_chat_action, set_webhook
from bot_app.mongodb import hashing_attribute, users_collection
from re import match
import logging
import json
# import telegram 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Setting webhook
webhook_response = set_webhook("url")
logger.info(webhook_response.text)

if webhook_response:
    @app.route('/', methods=['POST', 'GET'])
    def process():
        """
        Function that handles logic of the bot. 
        Should be optimized later on.
        """
        if request.method == 'POST':
            # Obtain main parameters to handle request from the user
            chat_id = request.json["message"]["chat"]["id"]
            username = request.json["message"]["chat"]["username"]
            user_message = request.json["message"]["text"].encode('utf-8').decode()
            # print(request.json)
            user_token = str()
            # chat_id is a unique id for user's chat with telegram bot
            existing_user = users_collection.find_one({"chat_id": chat_id })
            # regex to check basic token syntax
            open_ai_token_regex = r"^[a-z]{2}-[a-zA-Z0-9]{48}$"
            if user_message == "/start":
                send_chat_action(chat_id=chat_id, action="typing")
                send_message(chat_id=chat_id, text="Hello! This is Motoko.")
            elif user_message == "/delete":
                # Check if the document exists
                if existing_user:
                    # Delete the user's document
                    users_collection.delete_one(existing_user)
                    logger.info(f"Document deleted with ObjectId: {existing_user['_id']}")
                    send_chat_action(chat_id=chat_id, action="typing")
                    send_message(chat_id=chat_id, 
                                text="Your data is deleted.")
                else:
                    send_chat_action(chat_id=chat_id, action="typing")
                    send_message(chat_id=chat_id, 
                                text="Your data is absent, there is nothing to delete.")
            elif user_message == "/help":
                # 
                send_chat_action(chat_id=chat_id, action="typing")
                send_message(chat_id=chat_id, 
                            text="Commands available: \n /start \n /auth \n /delete \n /update_token \n /help")
            elif existing_user:
                # if unique user exists
                # obtain user's openai_token from mongodb
                user_token = existing_user.get("user_token")
                # send_message(chat_id=chat_id, text="KEK")
                send_chat_action(chat_id=chat_id, action="typing")
                if "/update_token" in user_message:
                    user_token = user_message[14:]
                    if match(open_ai_token_regex, user_token):
                        # update user's token in mongodb
                        users_collection.update_one({"chat_id": chat_id},
                                                    { "$set": {"user_token": user_token}})
                        print("Token is valid, updated.")
                        send_message(chat_id=chat_id, 
                                    text="Token is updated. Now we can talk ;)")
                    else:
                        send_message(chat_id, text="Token is invalid. \n Example: sk-nmhlalUuyIHg8HF04mLBY2BBbkFJFmduTZpd5vcQkk23r2iS")
                else:
                    try:
                        send_message(chat_id, openai_response(user_token=user_token, user_message=user_message, model='gpt-3.5-turbo'))
                    except AuthenticationError as auth_error:
                        # In case of authentication error with OPEN AI API
                        logger.error(auth_error)
                        user_token_asterisk = user_token[:3] + "*" * (len(user_token) - 4) + user_token[-4:]
                        auth_error_string = f"Incorrect API key provided: {user_token_asterisk}. You can find your API key at https://platform.openai.com/account/api-keys."
                        send_message(chat_id, text=f"{auth_error_string} Thereafter to update your token in my database please use command /update_token YOUR_TOKEN")
                        raise
                        # raise AuthenticationError(auth_error_string)
                    except Exception as err:
                        # In case any errors with OPEN AI API 
                        # (should handle more and precise exceptions)
                        logger.error(err)
                        send_message(chat_id, text="I have some network issues, later.")
                        raise
            else:
                # if token does not exist
                if "/auth" not in user_message:
                    send_chat_action(chat_id=chat_id, action="typing")
                    send_message(chat_id=chat_id, 
                                text="Please enter your OPENAI_API_KEY after /auth command.\n Example: /auth YOUR_TOKEN")
                else:
                    user_token = user_message[6:]
                    if match(open_ai_token_regex, user_token):
                        # hashing username attribute before adding to database
                        # mostly done for testing/educational purposes
                        hashed_username = hashing_attribute(username)
                        # mongodb user document(table) stracture
                        user_doc = {"chat_id": chat_id, 
                                    "username": hashed_username, 
                                    "user_token": user_token}
                        # register user with token in mongodb
                        users_collection.insert_one(user_doc)
                        print("Token is valid, registered.")
                        send_message(chat_id=chat_id, 
                                    text="Token is registered. Now we can talk ;)")
                    else:
                        send_message(chat_id, text="Token is invalid. \n Example: sk-nmhlalUuyIHg8HF04mLBY2BBbkFJFmduTZpd5vcQkk23r2iS")
            return "OK"
        else:
            return "OK"
else:
    response_dict = json.loads(webhook_response.text)
    logger.warning(f"Webhook is not set: {response_dict['description']}")