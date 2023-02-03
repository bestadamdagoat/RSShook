from configparser import ConfigParser
import time
import requests
import feedparser

def sendwebhook(title, description, url):
    data = {
        "username": username,
        "avatar_url": avatar_url,
        "embeds": [{
        "title": title,
        "description": description,
        "url": url,
        "author": {
        "name": name,
        "icon_url": icon_url,
        },
        "footer": {
        "text": "RSSHook by BestAdamDaGoat",
        "icon_url": "https://raw.githubusercontent.com/bestadamdagoat/RSShook/1fadda3b95361d49582139e0f1f33aa8d4fd2cfe/rsshooklogo.jpg",
        },
        }]
    }
    result = requests.post(webhook, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        time.sleep(2)
        print("Quitting, restart the bot.")
        quit(time.sleep(2))

config_object = ConfigParser(interpolation=None)
config_object.read("config.ini")
try:
    config = config_object["CONFIG"]
except KeyError:
    writeconfig = open("config.ini", "w")
    writeconfig.write("[CONFIG]\nrssfeed = https://yourfeed.net/rss\nwebhook = https://www.yourwebhook.com/\nchecktime = 60\nusername = RSShook\navatar_url = https://raw.githubusercontent.com/bestadamdagoat/RSShook/1fadda3b95361d49582139e0f1f33aa8d4fd2cfe/rsshooklogo.jpg\nname = Unconfigured RSShook\nicon_url = https://raw.githubusercontent.com/bestadamdagoat/RSShook/1fadda3b95361d49582139e0f1f33aa8d4fd2cfe/rsshooklogo.jpg")
    print("Config file missing. Don't worry though, I made one for you with the default options. Make sure to change the webhook to your own webhook.")
    time.sleep(2)
    print("Quitting, restart the bot.")
    sendwebhook("RSShook Error", "Config file missing. Don't worry though, I made one for you with the default options. Make sure to change the webhook to your own webhook.", "https://github.com/bestadamdagoat/RSShook")
    quit(time.sleep(2))

rssfeed = config["rssfeed"]
webhook = str(config["webhook"])
try:
    checktime = float(config["checktime"])
except ValueError:
    print("Please specify checktime in seconds (ex. 60) next time. Defaulting to 60.")
    writeconfig("checktime", "60")
    checktime = float(config["checktime"])
    time.sleep(3)
username = config["username"]
avatar_url = config["avatar_url"]
name = config["name"]
icon_url = config["icon_url"]

sendwebhook("RSShook Started", "RSShook has started. If you see this message, it means that the bot is working.", "https://github.com/bestadamdagoat/RSShook")

while True:
    # first request
    feed = feedparser.parse(rssfeed)

    # store the modified
    previous_post = feed.entries[0].title

    # check if new version exists
    feed_update = feedparser.parse(rssfeed)

    if feed_update.entries[0].title == previous_post:
        print("No new post")
    else:
        print("New post exists")
        sendwebhook(feed.entries[0].title, feed.entries[0].description, feed.entries[0].link)
    time.sleep(checktime)