__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import os
import time
import random

is_windows = os.name == 'nt'
if not is_windows:
    import pygame

mood_mapping = {'happy':'happy',
                'sad':'happy',
                'miss':'light',
                'normal':'light',
                'love':'light'}

rand = random.Random()

def play(mood='happy'):
    global rand
    print("Playing the song for mood %s..."%mood)

    if is_windows:  
        print("Faking music playback for 5 seconds...")      
        time.sleep(5)
    else:
        music_path = 'music/' + mood_mapping[mood]
        song_list = [os.path.join(music_path, f) \
                        for f in os.listdir(music_path) \
                        if os.path.isfile(os.path.join(music_path, f))]

        if song_list is None or len(song_list) <= 0:
            raise ValueError("The requested music mood was not defined or no songs found for the mood (%s)."%mood)

        rand.shuffle(song_list)

        pygame.mixer.init()
        pygame.mixer.music.load(song_list[0])
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            time.sleep(1)