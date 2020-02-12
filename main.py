# HTTP
import requests
from requests_oauthlib import OAuth1

# Utils
import logging
import yaml
import time
import json

# Telegram
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start_telegram():
    global telegram_token
    updater = Updater(telegram_token, request_kwargs={
                      'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
    dp = updater.dispatcher
    dp.add_error_handler(error)

    job_minute = updater.job_queue.run_repeating(
        check_for_update, interval=300, first=30)

    updater.start_polling()
    updater.idle()


def load_config():
    with open('config.yaml') as config_yaml:
        yaml_map = yaml.safe_load(config_yaml)
        global oauth_app_key
        global oauth_app_secret
        global oauth_token
        global oauth_token_secret
        oauth_app_key = yaml_map["twitter"]["auth"]["app_key"]
        oauth_app_secret = yaml_map["twitter"]["auth"]["app_secret"]
        oauth_token = yaml_map["twitter"]["auth"]["token"]
        oauth_token_secret = yaml_map["twitter"]["auth"]["token_secret"]

        global twitter_account
        twitter_account = yaml_map["twitter"]["name"]

        global telegram_token
        global telegram_chat_id
        telegram_token = yaml_map["telegram"]["token"]
        telegram_chat_id = yaml_map["telegram"]["chat_id"]



def check_for_update(context: CallbackContext):
    global url
    global auth1
    global twitter_account
    try:
        global last_tweet
        querystring = {"screen_name": twitter_account, "tweet_mode": "extended",
                       "exclude_replies": "true", "include_rts": "true", "since_id": last_tweet}
        response = requests.get(url, params=querystring, auth=auth1)
        response_json = json.loads(response.text)
        if len(response_json) is not 0:
            print("Nuovo Tweet!")
            print(response_json[0]);
            print("ID Tweet:  " + response_json[0]["id"])
            last_tweet = response_json[0]["id"]
            print(last_tweet)
            global telegram_chat_id
            context.bot.sendMessage(chat_id=telegram_chat_id, text="prova", parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        pass


def get_last_tweet():
    global url
    global auth1
    global twitter_account
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    auth1 = OAuth1(oauth_app_key, oauth_app_secret,
                   oauth_token, oauth_token_secret)
    querystring = {"screen_name": twitter_account, "tweet_mode": "extended",
                   "exclude_replies": "true", "include_rts": "true", "count": 1}
    response = requests.get(url, params=querystring, auth=auth1)
    global last_tweet
    last_tweet = (json.loads(response.text))[0]["id"]
    print(last_tweet)


def main():
    logging.basicConfig(level=logging.ERROR)
    global logger 
    logger = logging.getLogger(__name__)
    
    load_config()
    get_last_tweet()
    start_telegram()


if __name__ == '__main__':
    main()
