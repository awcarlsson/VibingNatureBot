import random
import math
import os
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

# randomly selects a video and grabs a sublcip from it
def get_video(list_of_docs):
    global CLIP_LENGTH
    doc_num = random.randint(0, len(list_of_docs) - 1)
    doc = VideoFileClip("docs/" + list_of_docs[doc_num])
    print("Chose doc: " + list_of_docs[doc_num])
    doc_length = math.floor(doc.duration)
    start_time = random.randint(0, doc_length - CLIP_LENGTH)
    clip = doc.subclip(start_time, start_time + CLIP_LENGTH)
    clip = clip.resize((1280, 720))
    return clip

# randomly selects a song and grabs a snippet from it
def get_song(list_of_songs):
    global CLIP_LENGTH
    global song_name
    song_num = random.randint(0, len(list_of_songs) - 1)
    song = AudioFileClip("songs/" + list_of_songs[song_num])
    print("Chose song: " + list_of_songs[song_num])
    song_name = list_of_songs[song_num].replace(".mp3", "")
    song_length = math.floor(song.duration)
    start_time = random.randint(0, song_length - CLIP_LENGTH)
    mp3 = song.subclip(start_time, start_time + CLIP_LENGTH)
    return mp3

# creates a clip by combining footage from a nature documentary with
# a randomly selected song
def create_clip(list_of_songs, list_of_docs):
    mp3 = get_song(list_of_songs)
    clip = get_video(list_of_docs)
    clip = clip.set_audio(mp3)
    return clip

# replies to the new tweet with the name of the song (and animal emoji)
def reply_song_name():
    emoji_file = open("emoji_list.txt", "r")
    emojis = emoji_file.read().split(",")
    emoji_file.close()
    new_tweet = twitter.get_user_timeline(user_id = ACNT_ID, count_id = 1)[0]
    screen_name = new_tweet['user']['screen_name']
    tweet_id = new_tweet['id']
    random_emoji = emojis[random.randint(0, len(emojis) - 1)].encode('utf-8').decode('unicode-escape')
    twitter.update_status(status = "@" + screen_name + " " + random_emoji + " song: " + song_name,
                          in_reply_to_status_id = tweet_id)
    
# main function
def main():
    global song_name
    print("Starting...")
    song_list = os.listdir("songs/")
    doc_list = os.listdir("docs/")
    print("Generating clip...")
    clip = create_clip(song_list, doc_list)
    print("Writing video...")
    clip.write_videofile("clip.mp4")
    # converts audio to the codec Twitter likes using ffmpeg
    os.system("ffmpeg -y -i clip.mp4 -c:v copy -c:a aac tweet.mp4")
    print("Tweeting video...")
    video = open('tweet.mp4', 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twitter.update_status(status='', media_ids=[response['media_id']])
    print("Done! Video has been tweeted.")
    reply_song_name()
    if (os.path.exists("clip.mp4")):
        os.remove("clip.mp4")

# starts the main function
main()
