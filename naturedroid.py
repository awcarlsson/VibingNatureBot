import tweepy
import random
import math
from moviepy.editor import *
from os import listdir

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

# Length of desired clip (in seconds)
CLIP_LENGTH = 30

# Number of episodes per season
S1_E_NUMBER = 10
S2_E_NUMBER = 6

# Number of song choices
SONG_NUMBER = 1

# Randomly selects a video and grabs a sublcip from it
def get_video():
    global CLIP_LENGTH
    global S1_E_NUMBER
    global S2_E_NUMBER
    szn = random.randint(1, 2)
    if (szn == 1):
        e_num = S1_E_NUMBER
    if (szn == 2):
        e_num = S2_E_NUMBER
    doc_name = "s" + str(szn) + "e" + str(random.randint(1, e_num))
    print("Picked doc: " + doc_name)
    #TODO: Replace clip with doc_name
    doc = VideoFileClip("docs/planetearth.mp4")
    doc_length = math.floor(doc.duration)
    start_time = random.randint(0, doc_length - CLIP_LENGTH)
    clip = doc.subclip(start_time, start_time + CLIP_LENGTH)
    return clip

# Randomly selects a song and grabs a snippet from it
def get_song(list_of_songs):
    global CLIP_LENGTH
    global SONG_NUMBER
    song_num = random.randint(0, SONG_NUMBER - 1)
    print(list_of_songs[song_num])
    song = AudioFileClip("songs/" + list_of_songs[song_num])
    song_length = math.floor(song.duration)
    start_time = random.randint(0, song_length - CLIP_LENGTH)
    print(start_time)
    mp3 = song.subclip(start_time, start_time + CLIP_LENGTH)
    return mp3

# Creates a clip by combining footage from a nature documentary with
# a randomly selected song
def create_clip(list_of_songs):
    mp3 = get_song(list_of_songs)
    clip = get_video()
    clip = clip.set_audio(mp3)
    return clip

# Main function
def main():
    song_list = os.listdir("songs/")
    clip = create_clip(song_list)
    clip.write_videofile("new_clip.mp4")
    # api.update_status(video)

# Starts the main function
main()
