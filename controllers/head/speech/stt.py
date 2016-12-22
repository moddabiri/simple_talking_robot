import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()

def listen(engine='sphinx*'):
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        print("Done listening...")

    try:
        if engine == 'sphinx':
            text = r.recognize_sphinx(audio)
        else:
            text = r.recognize_google(audio)
        print("Heard: " + text)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Could not reach the service {0}".format(e))
        return None