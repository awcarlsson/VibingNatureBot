import tweepy
import random
from moviepy.editor import *

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

# Number of episodes per season
S1_E_NUMBER = 10
S2_E_NUMBER = 6

# Randomly selects a video and grabs a 30 second sublcip from it
def get_video():
    global S1_E_NUMBER;
    global S2_E_NUMBER;
    s = random.randint(1, 2)
    if (s == 1):
        e_num = S1_E_NUMBER
    if (s == 2):
        e_num = S2_E_NUMBER
    doc_name = "s" + str(s) + "e" + str(random.randint(1, e_num))
    print("Picked doc: " + doc_name)
    #TODO: Replace clip with doc_name
    # clip = VideoFileClip("docs/planetearth.mp4")
    # intro_clip = clip.subclip("00:02:00", "00:02:15")
    # intro_clip.write_videofile("new_clip2.mp4")

# Creates a clip by combining footage from a nature documentary with a randomly
# selected song
def create_clip():
    #mp3 = get_song()
    get_video()
    #TODO: Combine MP3 and MP4

# Main function
def main():
    create_clip()
    # api.update_status(video)
    return 1

# Starts the main function
main()
