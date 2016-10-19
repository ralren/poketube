from pokeVid import PokeVid
from slackclient import SlackClient

import configparser
import requests
import urllib

config = configparser.ConfigParser()
config.read('config.ini')

SLACK_DEV_TOKEN = config['SLACK']['api_key']
YOUTUBE_API_KEY = config['YOUTUBE']['api_key']
YOUTUBE_UPLOADS_ID = config['YOUTUBE']['uploads_id']
slack_client = SlackClient(SLACK_DEV_TOKEN)

def overwrite_last_video_id(new_video_id):
    config['YOUTUBE']['last_video_id'] = new_video_id
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def send_message(title, url):
    slack_client.api_call(
        "chat.postMessage",
        channel="#poketube_test",
        text="The Pokemon channel uploaded a new video: " + title + "!\n" + url,
        username='PokeTube',
        icon_emoji=':joystick:')

def get_new_uploads(uploads):
    last_video_id = config['YOUTUBE']['last_video_id']
    new_uploads = []

    for i in range(len(uploads)):
        upload = uploads[i]
        current_video_id = upload['snippet']['resourceId']['videoId']
        if (current_video_id == last_video_id):
            break
        title = upload['snippet']['title']
        new_uploads.append(PokeVid(title, current_video_id))

    return new_uploads

def build_uploads_request():
    params = {"part": "snippet",
        "playlistId": YOUTUBE_UPLOADS_ID,
        "key": YOUTUBE_API_KEY}

    base_url = "https://www.googleapis.com/youtube/v3/playlistItems?"

    return base_url + urllib.urlencode(params)

def get_uploads():
    request = build_uploads_request()
    response = requests.get(request)
    return response.json()

if __name__ == '__main__':
    uploads = get_uploads()["items"]
    new_uploads = get_new_uploads(uploads)

    if (len(new_uploads) > 0):
        for upload in new_uploads:
            send_message(upload.title, upload.get_url())
        overwrite_last_video_id(new_uploads[0].video_id)
