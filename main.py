import subprocess
import wolframalpha
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import smtplib
import ctypes
import time
import shutil
from ecapture import ecapture as ec
from urllib.request import urlopen
import urllib.parse
import re
from pynput.keyboard import Key, Controller
import timeit

VA_NAME = "aleksa"
VA_ENG_NAME = "alexa"

#set our engine to Pyttsx3 which is used for text to speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id) #voices[0].id for female voice
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
# Use female Russian voice
engine.setProperty('voice', ru_voice_id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Jutro !")

    elif hour >= 12 and hour < 18:
        speak("Ugodno popodne !")

    else:
        speak("Dobra večer !")

    assname = ("Sunčica")
    speak("Ja sam tvoj asistent")
    speak(assname)


def usrname():
    speak("Kako da tebe zovem")
    uname = takeCommand()
    speak("Pozdravljen budi")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

    speak("Kako da ti pomognem")


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        #query_eng = r.recognize_google(audio, language='en-in')
        query_hrv = r.recognize_google(audio, language='hr_HR')
        print(f"User said: {query_hrv}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query_hrv


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('your email id', 'your email passowrd')
    server.sendmail('your email id', to, content)
    server.close()


if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any
    # command before execution of this python file
    clear()
    speak("Radim")

    while True:

        start_time = timeit.default_timer()
        query = takeCommand().lower()

        # All the commands said by user will be
        # stored here in 'query' and will be
        # converted to lower case for easily
        # recognition of command
        if VA_NAME in query or VA_ENG_NAME in query:
            query = query.replace(VA_NAME, "")
            query = query.replace(VA_ENG_NAME, "")
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in query or "otvori youtube" in query:
                speak("Youtube\n")
                webbrowser.open("youtube.com")

            elif 'open google' in query or "otvori google" in query:
                speak("Here you go to Google\n")
                webbrowser.open("google.com")

            elif 'open stackoverflow' in query or "otvori stackoverflow" in query:
                speak("Here you go to Stack Over flow.Happy coding")
                webbrowser.open("stackoverflow.com")

            elif "play" in query or "pusti" in query:
                play_index = query.find("play")
                if play_index == -1:
                    play_index = query.find("pusti")
                    song_name = query[play_index + 6:]
                else:
                    song_name = query[play_index + 5:]
                speak(f"ide pjesma {song_name}")

                query_string = urllib.parse.urlencode({"search_query": song_name})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'\"url\":\"\/watch\?v=(.{11})', html_content.read().decode())
                #print("http://www.youtube.com/watch?v=" + search_results[0])
                webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])

            elif "sljedeća" in query:
                speak("Ide sljedeća")
                keyboard = Controller()
                keyboard.press(Key.media_next)
                keyboard.release(Key.media_next)

            elif "prethodna" in query:
                speak("Ide prethodna")
                keyboard = Controller()
                keyboard.press(Key.media_previous)
                keyboard.release(Key.media_previous)

            elif "pauza" in query:
                speak("Ide pauza")
                keyboard = Controller()
                keyboard.press(Key.media_play_pause)
                keyboard.release(Key.media_play_pause)

            elif "nastavi" in query:
                speak("Nastavljam")
                keyboard = Controller()
                keyboard.press(Key.media_play_pause)
                keyboard.release(Key.media_play_pause)

            elif 'sati' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sada je {strTime}")

            elif 'upali lol' in query or "upalilo" in query:
                codePath = os.path.join("C:", "Riot Games", "League of Legends", "LeagueClient.exe")
                os.startfile(codePath)

            elif 'exit' in query:
                speak("Thanks for giving me your time")
                exit()

            elif "who made you" in query or "who created you" in query:
                speak("I have been created by Piki.")


            elif "calculate" in query:

                app_id = "Wolframalpha api id"
                client = wolframalpha.Client(app_id)
                indx = query.lower().split().index('calculate')
                query = query.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                print("The answer is " + answer)
                speak("The answer is " + answer)

            elif 'search' in query or 'traži' in query:
                query = query.replace(VA_NAME, "")
                query = query.replace("search", "")
                query = query.replace("traži", "")
                webbrowser.open(query)


            elif 'change background' in query:
                ctypes.windll.user32.SystemParametersInfoW(20,
                                                           0,
                                                           "Location of wallpaper",
                                                           0)
                speak("Background changed succesfully")


            elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()

            elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')

            elif 'empty recycle bin' in query:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                speak("Recycle Bin Recycled")

            elif "pauza" in query or "stop listening" in query:
                speak("for how much time you want to stop aleksa from listening commands")
                try:
                    a = int(takeCommand())
                except:
                    speak("To nije broj")
                    continue

                time.sleep(a)
                print(a)

            elif "gdje je" in query:
                query = query.replace("gdje je", "")
                location = query
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.nl/maps/place/" + location + "")

            elif "kamera" in query or "take a photo" in query:
                ec.capture(0, "Jarvis Camera ", "img.jpg")

            elif "restart" in query:
                subprocess.call(["shutdown", "/r"])

            elif "hibernate" in query or "sleep" in query:
                speak("Hibernating")
                subprocess.call("shutdown / h")

            elif "log off" in query or "sign out" in query:
                speak("Make sure all the application are closed before sign-out")
                time.sleep(5)
                subprocess.call(["shutdown", "/l"])

            elif "wikipedia" in query:
                webbrowser.open("wikipedia.com")

            elif "ide gas" in query:
                speak("IDE GASSSSSS")

            if "exit" in str(query) or "bye" in str(query) or "sleep" in str(query) or "ugasi se" in query:
                speak("Ok bye!")
                break

        end_time = timeit.default_timer()
        print(f"Time: {end_time-start_time}")
