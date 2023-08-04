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
import openai
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

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

    if 0 <= hour < 12:
        speak("Good morning Master")

    elif 12 <= hour < 18:
        speak("Good afternoon Master")

    else:
        speak("Good evening Master")

    speak("I am your assistant. How may I help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query

    except Exception as e:
        query = takeCommand()


def searchGoogle(query, num_sentences=10):
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


def getLatestNews():
    url = "https://news.google.com/rss"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    news_list = soup.find_all("item")
    latest_news = []

    for i, news in enumerate(news_list[:10]):
        title = news.title.text
        latest_news.append(title)
        if i == 9:
            break

    return latest_news



def main():
    wishMe()
    while True:
        query = takeCommand()

        if query:
            if 'stop' in query.lower() or 'exit' in query.lower():
                speak("ok...shutting down...!")
                break

            if 'wikipedia' in query.lower():
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=4)
                    print(results)
                    speak(results)
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any information on that topic.")
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple results for that query. Please be more specific.")

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

            elif 'the time' in query.lower() or 'what is the time' in query.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Master the time is {strTime}")

            elif 'tell a joke' in query.lower() or 'tell me a joke' in query.lower() or 'another joke' in query.lower():
                tellJoke()

            elif 'latest news' in query.lower() or 'news' in query.lower():
                speak("Fetching the latest news...")
                news = getLatestNews()
                if news:
                    speak("Here are the 10 latest news headlines:")
                    for i, headline in enumerate(news):
                        speak(f"{i + 1}. {headline}")
                else:
                    speak("Sorry, I couldn't fetch the latest news at the moment.")

            else:
                speak("Searching on Internet...")
                result = searchGoogle(query, num_sentences=4)
                if result:
                    print(result)
                    speak(result)
                else:
                    speak("No results found on Google.")


if __name__ == "__main__":
    main()
