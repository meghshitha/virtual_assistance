import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import requests
import pyjokes

from bs4 import BeautifulSoup

print("STARTED....")
MASTER = "MANOHAR"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    print("TIME IS: ", hour)

    if 0 <= hour < 12:
        speak("Good morning" + MASTER)

    elif 12 <= hour < 18:
        speak("Good afternoon" + MASTER)

    else:
        speak("Good evening" + MASTER)

    speak("I am your assistant. How may I help you?")



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        query = takeCommand()

    return query


# def searchGoogle(query):
#     url = f"https://www.google.com/search?q={query}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     search_result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
#     return search_result

def searchGoogle(query, num_sentences=5):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    search_result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
    sentences = search_result.split(".")
    result = ". ".join(sentences[:num_sentences])
    return result

def tellJoke():
    joke = pyjokes.get_joke()
    print(joke)
    speak("Here's a joke for you:")
    speak(joke)





def main():
    speak("STARTING...")
    wishMe()
    query = takeCommand()

    if query:
        
        if 'wikipedia'  in query.lower():
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)

        elif 'open youtube' in query.lower():
            url = "https://www.youtube.com"
            webbrowser.open(url)

        elif 'open google' in query.lower():
            url = "https://www.google.com"
            webbrowser.open(url)

        elif 'play music' in query.lower() or 'play song' in query.lower():
            songs_dir = "C:\\Users\\manu\\Music\\MUSIC"
            songs = os.listdir(songs_dir)
            print(songs)
            os.startfile(os.path.join(songs_dir, songs[0]))

        elif 'the time' in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"{MASTER}, the time is {strTime}")


        elif 'tell a joke' or 'say a joke' or 'a joke' or 'joke' in query.lower():
            tellJoke()


        else :
            speak("Searching on Google...")
            result = searchGoogle(query, num_sentences=4)
            if result:
                speak("Here are the top search results:")
                print(result)
                speak(result)
            else:
                speak("No results found on Google.")
    



if __name__ == "__main__":
    main()
