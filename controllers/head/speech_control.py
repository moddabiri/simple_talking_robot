__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import tts
import stt
import time
from random import Random
from pythonds.graphs import Graph
from controllers.state.state_machine import StateMachineNode
import util.sys_helpers as sysh
import music as music
import re
import speech.conversation as conv

env_state = None
on_before_shutdown_action = None
mood = 'NORMAL'

joke_rand = Random()
def get_joke():
    random_index = joke_rand.randint(0, len(conv.jokes)-1)
    return conv.jokes[random_index] + ['Huh Huh Huh Huh Huh Huh.']

def play_music():
    global env_state

    tts.say(["Here you go. Some nice music for your mood [name]."], env_state.human_name, is_online=env_state.internet)
    music.play(env_state.mood)
    tts.say(["Hope I helped you feel better [name] with this song."], env_state.human_name, is_online=env_state.internet)

    return 'NULL'

def say_listen(state, silent, accepted):
    say(state, silent, accepted)
    return listen(state, accepted)

var_rand = Random()
def say(state, silent, accepted):
    global env_state
    print("Saying...")

    if not silent:
        phrases = conv.conversations.get(state, None)

        if not phrases is None:
            action_points = {'joke': get_joke(), 'music': '[music-%s]'%env_state.mood}
            vars = {}
            processed = []
            for phrase in phrases:
                var_matches = re.findall(r'\{{2}\w{1}\}\{[^\}]+\}{2}', phrase)
                for exp in var_matches:
                    action = None
                    var_exp = re.findall(r'\{{2}\w{1}\}', exp)[0]
                    var_name = var_exp.replace('}', '').replace('{', '')
                    options_exp = exp.replace(var_exp, '').replace('}', '').replace('{', '').split('/')
                    var_rand.shuffle(options_exp)
                    action = options_exp[0].split(':')[1].split('=')[0]
                    option_id = options_exp[0].split(':')[0]
                    replacement = options_exp[0].split(':')[1].split('=')[1]
                    vars[var_name] = action
                    phrase = phrase.replace(exp, replacement)

                value_matches = re.findall(r'\[.+\]', phrase)
                for exp in value_matches:
                    var_name = exp.replace('[', '').replace(']', '')
                    action = vars.get(var_name, None)
                    action_point = None

                    if action is None:
                        if action_points.get(var_name):
                            action_point = action_points.get(var_name)
                    else:
                        action_point = action_points.get(action)

                    if action_point:
                        if isinstance(action_point, str):
                            phrase = phrase.replace(exp, action_point)
                        elif isinstance(action_point, list):
                            phrase = None
                            processed = processed + action_point
                        else:
                            raise ValueError("The variable was mapped to an unacceptable type of action point. Possible implementation bug. Only string and list of strings are acceptable.")
                
                if phrase:
                    processed.append(phrase)

            if len(processed) > 0:
                tts.say(processed, env_state.human_name, is_online=env_state.internet)

    return 'NULL'
    #return 'DEBUG'

def listen(state, accepted):
    global env_state

    time.sleep(0.5)
    text = stt.listen('google' if env_state.internet else 'sphinx*')
    if text is None or text == "":
        tts.say(['Sorry', 'Didn\'t quite understand you.', 'Please repeat.'], is_online=env_state.internet)
        return 'NOTHINGSAID'

    text = text.strip()
    activation = conv.responses.get(text, None)

    if activation:
        if 'HAPPY' in activation:
            env_state.mood = 'happy'
        elif 'SAD' in activation:
            env_state.mood = 'sad'
        elif 'LOVE' in activation:
            env_state.mood = 'love'
        elif 'NORMAL' in activation:
            env_state.mood = 'normal'

    if activation is None:
        tts.say(['Excuse me?'], is_online=env_state.internet)
        return 'OTHERWISE'

    activation = activation.split('*')[0]

    if activation not in accepted:
        tts.say(['Ah, Sorry, but I did not expect to hear that as a response to what I said.'], is_online=env_state.internet)

    return activation

def shutdown():
    global on_before_shutdown_action

    if on_before_shutdown_action:
        on_before_shutdown_action()

    say('R-BYE', False, True)
    sysh.shutdown()

    return "NULL"

def read_ip_addresses():
    global env_state
    tts.say(["Speech IP address is " + env_state.ip], env_state.human_name, is_online=env_state.internet)
    tts.say(["Head IP address is " + env_state.buddy_ip], env_state.human_name, is_online=env_state.internet)
    return 'NULL'

def start(state, on_before_shutdown):
    global env_state
    global on_before_shutdown_action

    env_state = state
    on_before_shutdown_action = on_before_shutdown
    
    state_awake = StateMachineNode('R-AWAKE', lambda silent, accepted:say_listen('R-AWAKE',silent, accepted))
    state_awake.loop('NOTHINGSAID')
    state_awake.loop('OTHERWISE')
    state_awake.set_unknown_target(state_awake)

    state_hello = StateMachineNode('R-HELLO', lambda silent, accepted:say_listen('R-HELLO', silent, accepted))
    state_awake.add_edge(state_hello, 'TOLD-HELLO')
    state_hello.loop('NOTHINGSAID')
    state_hello.loop('OTHERWISE')
    state_hello.set_unknown_target(state_hello)

    state_greet = StateMachineNode('R-GREET', lambda silent, accepted:say_listen('R-GREET', silent, accepted))
    state_greet.add_edge(state_hello, 'TOLD-HELLO')
    state_hello.add_edge(state_greet, 'TOLD-GREET')
    state_greet.loop('NOTHINGSAID')
    state_greet.loop('OTHERWISE')

    state_greet_resp_pos = StateMachineNode('R-GREET-RESP-NORMAL', lambda silent, accepted:say('R-GREET-RESP-NORMAL', silent, accepted))
    state_greet.add_edge(state_greet_resp_pos, 'TOLD-GREET-RESP-NORMAL')
    state_greet.add_edge(state_greet_resp_pos, 'TOLD-GREET-RESP-HAPPY')
    state_greet_resp_pos.loop('NOTHINGSAID')

    state_greet_resp_neg = StateMachineNode('R-GREET-RESP-SAD', lambda silent, accepted:say('R-GREET-RESP-SAD', silent, accepted))
    state_greet.add_edge(state_greet_resp_neg, 'TOLD-GREET-RESP-SAD')
    state_greet_resp_neg.loop('NOTHINGSAID')

    state_askme = StateMachineNode('R-ASKME', lambda silent, accepted:say_listen('R-ASKME', silent, accepted))
    state_greet_resp_pos.add_edge(state_askme, 'NULL')
    state_askme.loop('NOTHINGSAID')
    state_askme.loop('OTHERWISE')

    state_debug = StateMachineNode('R-DEBUG', lambda silent, accepted:'DEBUG')
    state_greet_resp_pos.add_edge(state_debug, 'DEBUG')
    state_greet_resp_neg.add_edge(state_debug, 'DEBUG')
    state_debug.return_back('DEBUG')

    state_how_old = StateMachineNode('R-AGE', lambda silent, accepted:say('R-AGE', silent, accepted))
    state_askme.add_edge(state_how_old, 'TOLD-HOW-OLD')
    state_how_old.add_edge(state_askme, 'NULL')

    state_whats_name = StateMachineNode('R-INTRODUCE', lambda silent, accepted:say('R-INTRODUCE', silent, accepted))
    state_askme.add_edge(state_whats_name, 'TOLD-WHATS-NAME')
    state_whats_name.add_edge(state_askme, 'NULL')

    state_how_old = StateMachineNode('R-AGE', lambda silent, accepted:say('R-AGE', silent, accepted))
    state_askme.add_edge(state_how_old, 'TOLD-HOW-OLD')
    state_how_old.add_edge(state_askme, 'NULL')

    state_where_from = StateMachineNode('R-WHERE-FROM', lambda silent, accepted:say('R-WHERE-FROM', silent, accepted))
    state_askme.add_edge(state_where_from, 'TOLD-WHERE-FROM')
    state_where_from.add_edge(state_askme, 'NULL')

    state_ip = StateMachineNode('R-IP', lambda silent, accepted:read_ip_addresses())
    state_askme.add_edge(state_ip, 'TOLD-IP')
    state_ip.add_edge(state_askme, 'NULL')

    state_music = StateMachineNode('R-MUSIC', lambda silent, accepted:play_music())
    state_askme.add_edge(state_music, 'TOLD-MUSIC')
    state_greet.add_edge(state_music, 'TOLD-GREET-RESP-LOVE')
    state_music.add_edge(state_askme, 'NULL')

    state_check_mood = StateMachineNode('R-CHECKMOOD', lambda silent, accepted:say_listen('R-CHECKMOOD', silent, accepted))
    state_greet_resp_neg.add_edge(state_check_mood, 'NULL')
    state_check_mood.add_edge(state_greet_resp_pos, 'TOLD-YES')
    state_check_mood.add_edge(state_greet_resp_neg, 'TOLD-NO')
    state_check_mood.loop('NOTHINGSAID')
    state_check_mood.loop('OTHERWISE')

    state_bye = StateMachineNode('R-BYE', lambda silent, accepted:shutdown())
    state_askme.add_edge(state_bye, 'TOLD-BYE')

    StateMachineNode.start(state_awake)
    #StateMachineNode.start(state_greet_resp_neg)
    
if __name__ == "__main__":
    from State import State

    def on_shutdown():
        print("SHUTTING DOWN...")

    state = State()
    state.internet = True
    start(state, on_shutdown)