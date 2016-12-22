import pyttsx
import time
import os
import re
from datetime import datetime
import util.sys_helpers as sysh
import music as music
is_windows = os.name == 'nt'

if not is_windows:
    from pyvona.pyvona import create_voice
    
pyvona_engine=None

class CustomEspeak(object):
    def __init__(self):
        if is_windows:
            self._engine = pyttsx.init()
            self._engine.setProperty('rate', 160)
            self._engine.setProperty('voice', 'english')

    _engine = None

    def say(self, phrase):
        if is_windows:
            self._engine.say(phrase)
            self._engine.runAndWait()
        else:
            sysh.execute_unix("espeak -s150 \"%s\""%phrase)

PAUSE_SHORT = '[Pause-Short]'
PAUSE_MEDIUM = '[Pause-Medium]'
PAUSE_LONG = '[Pause-Long]'
NAME_LOCATOR = '[name]'
AGE_LOCATOR = '[age]'
MUSIC_LOCATOR = r'\[music\-\w+\]'

IVONA_ACCESS_KEY = 'YOUR ACCESS KEY'
IVONA_SECRET_KEY = 'YOUR SECRET KEY'


engine = CustomEspeak()

def say(phrases, human_name="human", is_online=False):
    global pyvona_engine
    if not is_windows and is_online:
        if not pyvona_engine:
            pyvona_engine=create_voice(IVONA_ACCESS_KEY, IVONA_SECRET_KEY)

        phrases = [process_replacements(x, human_name) for x in phrases if x != PAUSE_SHORT and x != PAUSE_MEDIUM and x != PAUSE_LONG]
        compound_phrase = ""
        for phrase in phrases:
            if re.match(MUSIC_LOCATOR, phrase):
                pyvona_engine.speak(compound_phrase)
                compound_phrase=""
                mood = phrase.split('-')[1].replace(']', '')
                music.play(mood)
            else:
                compound_phrase += " " + phrase
                
        if compound_phrase:
            pyvona_engine.speak(compound_phrase)

        #compound_phrase = " ".join([process_replacements(x, human_name) for x in phrases if x != PAUSE_SHORT and x != PAUSE_MEDIUM and x != PAUSE_LONG])
        #pyvona_engine.speak(compound_phrase)
    else:
        for phrase in phrases:
            phrase = process_replacements(phrase, human_name)
            if phrase == PAUSE_SHORT:
                time.sleep(0.5)
            elif phrase == PAUSE_MEDIUM:
                time.sleep(1)
            elif phrase == PAUSE_LONG:
                time.sleep(2)
            elif re.match(MUSIC_LOCATOR, phrase):
                mood = phrase.split('-')[1].replace(']', '')
                music.play(mood)
            else:
                print("Saying: " + phrase)
                engine.say(phrase)


def process_replacements(input, human_name):
    birth_date = datetime(2016,8,21)
    age_hours = (datetime.now()-birth_date).total_seconds()/3600
    return input.replace(NAME_LOCATOR, human_name).replace(AGE_LOCATOR, get_age_phrase(age_hours))

def get_age_phrase(hours):
    if hours < 1:
        mins = int(hours/60)
        return "%d minute%s"%(mins, "s" if mins > 1 else "")
    if hours < 24:
        return "%d hour%s"%(int(hours), "s" if hours > 1 else "")
    if hours < 24*7:
        days = int(hours/24)
        return "%d day%s"%(days, "s" if days > 1 else "")
    if hours < 24*30:
        weeks = int(hours/(24*7))
        return "%d week%s"%(weeks, "s" if weeks > 1 else "")
    if hours < 365:
        months = int(hours/(24*30))
        return "%d month%s"%(months, "s" if months > 1 else "")
    
    years = int(hours/(365))
    return "%d year%s"%(years, "s" if years > 1 else "")