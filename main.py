import requests
from requests_oauthlib import OAuth1
import yaml
import time
import json

def load_settings():
    with open('auth.yaml') as yaml_auth:
        auth_map = yaml.safe_load(yaml_auth)
        global oauth_app_key
        global oauth_app_secret
        global oauth_token
        global oauth_token_secret
        oauth_app_key = auth_map["oauth_app_key"]
        oauth_app_secret = auth_map["oauth_app_secret"]
        oauth_token = auth_map["oauth_token"]
        oauth_token_secret = auth_map["oauth_token_secret"]

def main():
    load_settings()
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    auth1 = OAuth1(oauth_app_key, oauth_app_secret, oauth_token, oauth_token_secret)
    querystring = {"screen_name":"azione_it","tweet_mode":"extended","exclude_replies":"true","include_rts":"true","count":1}
    response = requests.get(url, params=querystring, auth=auth1)
    last_tweet = (json.loads(response.text))[0]["id"]
    print(last_tweet)
    time.sleep(300)

    while(True):
        try:
            querystring = {"screen_name":"azione_it","tweet_mode":"extended","exclude_replies":"true","include_rts":"true", "since_id": last_tweet}
            auth1 = OAuth1(oauth_app_key, oauth_app_secret, oauth_token, oauth_token_secret)
            response = requests.get(url, params=querystring, auth=auth1)
            response_json = json.loads(response.text)
            if len(response_json) is not 0:
                print("----------------")
                print(response_json)
                last_tweet = response_json[0]["id"]
        except Exception as e:
            print("Errore")
        time.sleep(300)

if __name__ == '__main__':
    main()