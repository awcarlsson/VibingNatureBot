import random
import math
import os
import time
from dotenv import load_dotenv
from moviepy.editor import *
from twython import Twython
from google.cloud import storage

load_dotenv()

AP_KY = os.getenv('APP_KEY')
AP_SEC = os.getenv('APP_SECRET')
AUTH_TOK = os.getenv('OAUTH_TOKEN')
AUTH_SEC = os.getenv('OAUTH_SECRET')
ACNT_ID = os.getenv('ACCOUNT_ID')
CL_JSON = os.getenv('CLIENT_JSON')

# initializes twitter object
twitter = Twython(AP_KY, AP_SEC, AUTH_TOK, AUTH_SEC)

# initializes google cloud storage client, stores videos/songs
storage_client = storage.Client.from_service_account_json(CL_JSON)

# length of desired clip (in seconds)
CLIP_LENGTH = 30

# name of song for the current tweet
song_name = ""

# globals to assist with closing mp4/mp3 input streams
mp4_download = None
mp3_download = None
mp4_subclip = None
mp3_subclip = None

# randomly selects a video and downloads it from cloud
def download_video():
    bucket = storage_client.get_bucket('nature_docs')
    filenames = list(bucket.list_blobs(prefix = ''))
    doc_num = random.randint(0, len(filenames) - 1)
    print('Chose doc: ' + filenames[doc_num].name)
    blob = bucket.blob(filenames[doc_num].name)
    print('Downloading from cloud...')
    blob.download_to_filename('vid_download.mp4')

#  grabs a subclip from downloaded video
def get_video():
    global CLIP_LENGTH
    global mp4_download
    global mp4_subclip
    download_video()
    mp4_download = VideoFileClip('vid_download.mp4')
    doc_length = math.floor(mp4_download.duration)
    start_time = random.randint(0, doc_length - CLIP_LENGTH - 1)
    mp4_subclip = mp4_download.subclip(start_time, start_time + CLIP_LENGTH)
    mp4_subclip = mp4_subclip.resize((1280, 720))

# randomly selects a song and downloads it from cloud
def download_song():
    global song_name
    bucket = storage_client.get_bucket('nature_songs')
    filenames = list(bucket.list_blobs(prefix = ''))
    song_num = random.randint(0, len(filenames) - 1)
    print('Chose song: ' + filenames[song_num].name)
    song_name = filenames[song_num].name.replace('.mp3', '')
    blob = bucket.blob(filenames[song_num].name)
    print('Downloading from cloud...')
    blob.download_to_filename('song_download.mp3')

# grabs a snippet from downloaded song
def get_song():
    global CLIP_LENGTH
    global mp3_download
    global mp3_subclip
    download_song()
    mp3_download = AudioFileClip('song_download.mp3')
    song_length = math.floor(mp3_download.duration)
    start_time = random.randint(0, song_length - CLIP_LENGTH - 1)
    mp3_subclip = mp3_download.subclip(start_time, start_time + CLIP_LENGTH)

# creates a clip by combining footage from a nature documentary with a randomly selected song
def create_clip():
    global mp4_subclip
    global mp3_subclip
    get_video()
    get_song()
    mp4_subclip = mp4_subclip.set_audio(mp3_subclip)

# replies to the new tweet with the name of the song (and animal emoji)
def reply_song_name():
    emoji_file = open('emoji_list.txt', 'r')
    emojis = emoji_file.read().split(',')
    emoji_file.close()
    new_tweet = twitter.get_user_timeline(user_id = ACNT_ID, count_id = 1)[0]
    screen_name = new_tweet['user']['screen_name']
    tweet_id = new_tweet['id']
    random_emoji = emojis[random.randint(0, len(emojis) - 1)].encode('utf-8').decode('unicode-escape')
    twitter.update_status(status = '@' + screen_name + ' ' + random_emoji + ' song: ' + song_name,
                          in_reply_to_status_id = tweet_id)
    
# main function
def generate_and_tweet():
    print('Generating clip...')
    create_clip()
    print('Writing video...')
    mp4_subclip.write_videofile('clip.mp4')
    # cleans up from previous video creation steps
    mp4_download.close()
    mp3_download.close()
    mp4_subclip.close()
    mp3_subclip.close()
    if (os.path.exists('vid_download.mp4')):
        os.remove('vid_download.mp4')
    if (os.path.exists('song_download.mp3')):
        os.remove('song_download.mp3')
    # converts audio to the codec twitter likes using ffmpeg
    os.system('ffmpeg -y -i clip.mp4 -c:v copy -c:a aac tweet.mp4')
    # for older versions of ffmpeg
    # os.system('ffmpeg -y -i clip.mp4 -c:v copy -strict experimental -c:a aac tweet.mp4')
    print('Tweeting video...')
    video = open('tweet.mp4', 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twitter.update_status(status='', media_ids=[response['media_id']])
    video.close()
    print('Done! Video has been tweeted.')
    reply_song_name()
    if (os.path.exists('clip.mp4')):
        os.remove('clip.mp4')
    if (os.path.exists('tweet.mp4')):
        os.remove('tweet.mp4')

# loop to control when to tweet
tweeting = True
while tweeting:
    print("Running")
    generate_and_tweet()
    time.sleep(3600)
