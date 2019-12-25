import tweepy
import random
import math
import os
from moviepy.editor import *

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

# Length of desired clip (in seconds)
CLIP_LENGTH = 30

# Randomly selects a video and grabs a sublcip from it
def get_video(list_of_docs):
    global CLIP_LENGTH
    doc_num = random.randint(0, len(list_of_docs) - 1)
    doc = VideoFileClip("docs/" + list_of_docs[doc_num])
    doc_length = math.floor(doc.duration)
    start_time = random.randint(0, doc_length - CLIP_LENGTH)
    clip = doc.subclip(start_time, start_time + CLIP_LENGTH)
    clip = clip.resize((1280, 720))
    return clip

# Randomly selects a song and grabs a snippet from it
def get_song(list_of_songs):
    global CLIP_LENGTH
    song_num = random.randint(0, len(list_of_songs) - 1)
    song = AudioFileClip("songs/" + list_of_songs[song_num])
    song_length = math.floor(song.duration)
    start_time = random.randint(0, song_length - CLIP_LENGTH)
    mp3 = song.subclip(start_time, start_time + CLIP_LENGTH)
    return mp3

# Creates a clip by combining footage from a nature documentary with
# a randomly selected song
def create_clip(list_of_songs, list_of_docs):
    mp3 = get_song(list_of_songs)
    clip = get_video(list_of_docs)
    clip = clip.set_audio(mp3)
    return clip

# Main function
def main():
    song_list = os.listdir("songs/")
    doc_list = os.listdir("docs/")
    clip = create_clip(song_list, doc_list)
    clip.write_videofile("clip.mp4")
    # Convers audio to the codec Twitter likes
    os.system("ffmpeg -y -i clip.mp4 -c:v copy -c:a aac outfile.mp4")
    upload_result = api.media_upload('outfile.mp4')
    api.update_status(status="test tweet", media_ids=[upload_result.media_id_string])

# Starts the main function
main()
