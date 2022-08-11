import tweepy
import requests


def postTweet(argv):
    twitter_auth_keys = {
        "consumer_key": "LfEsVGQNWgf1G2FRIirYsASox",
        "consumer_secret": "ipOxZbKV1TZP1h6ZKL1OWb92OCQLEXPQ9Ih6NJ4UaFEimMRJCC",
        "access_token": "1410285704060485633-rfsHIg9lEKPh7AqYXH09AF5NtHT0jR",
        "access_token_secret": "xjlfh5GQJwWxsx62RbLpxAtvZF4n2SYYHsRwZHJfjRmb2"
    }

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)

    content = argv
    status = api.update_status(status=content)


def postTelegram(argv):
    url = "https://api.telegram.org/bot1945580972:AAHD7xB-aN6Y-Jz0vSNqoZjtQwM9kevrBwM/sendMessage?chat_id=@AMA_cryptobot&text="
    url += argv
    requests.post(url)
