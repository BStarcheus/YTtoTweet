import logging
import json
import html
import base64
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import datastore
import twitter


YOUTUBE_DEVELOPER_KEY = 'YOUR_DEVELOPER_KEY'
YOUTUBE_CHANNEL_ID = 'YOUR_CHANNEL_ID'

TWITTER_CONSUMER_KEY='YOUR_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET='YOUR_CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN_KEY='YOUR_ACCESS_TOKEN_KEY'
TWITTER_ACCESS_TOKEN_SECRET='YOUR_ACCESS_TOKEN_SECRET'


def checkYT(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=YOUTUBE_DEVELOPER_KEY, cache_discovery=False)

    # Setup Datastore client, key, and entity
    client = datastore.Client()
    kind = 'date'
    name = 'lastTime'
    key = client.key(kind, name)

    ent = client.get(key)
    lastTime = ""

    # Get the last time checkYT ran successfully
    if ent:
        lastTime = ent['lastTime']
    else:
        ent = datastore.Entity(key=key)
        lastTime = str(datetime.now() - timedelta(days=1))

    # Convert from string into RFC 3339 format
    lastTime = datetime.strptime(lastTime, '%Y-%m-%d %H:%M:%S.%f').isoformat()
    lastTime = lastTime[:19] + 'Z'

    # Get new YouTube uploads
    request = youtube.search().list(
        part="id,snippet",
        channelId=YOUTUBE_CHANNEL_ID,
        order="date",
        publishedAfter=lastTime
    )
    response = request.execute()

    # Twitter API
    api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                  consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=TWITTER_ACCESS_TOKEN_KEY,
                  access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

    # Tweet the videos in chronological order
    videos = reversed(response["items"])
    status = True

    for vid in videos:
        try:
            message = "New Upload!\n{0}\nhttps://www.youtube.com/watch?v={1}".format(vid['snippet']['title'][:70], vid['id']['videoId'])
            message = html.unescape(message)
            status = api.PostUpdate(message)
            print("{0} just posted: {1}".format(status.user.name, status.text))
            status = True
        except Exception as inst:
            status = False
            print(inst, "Unable to tweet.")


    if status:
        # Update Datastore with last successful run of checkYT
        ent['lastTime'] = str(datetime.now())
        client.put(ent)
        return "checkYT completed"

    return "checkYT failed"
