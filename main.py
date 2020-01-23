import requests
from requests_oauthlib import OAuth1
import yaml
import time

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
    querystring = {"screen_name":"azione_it","tweet_mode":"extended","exclude_replies":"true","include_rts":"false"}
    auth1 = OAuth1(oauth_app_key, oauth_app_secret, oauth_token, oauth_token_secret)

    response = requests.get(url, params=querystring, auth=auth1)

    print(response.text)

if __name__ == '__main__':
    main()