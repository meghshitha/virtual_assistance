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
import json
import pywhatkit
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import tkinter as tk

print("STARTED....")
MASTER = "DANGER"

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

    speak('I am your Virtual Assistant. How Can I Help You Today')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"YOU said: {query}\n")

    except sr.UnknownValueError:
        print('NO AUDIO HEARD......')
        query = takeCommand()

    return query


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
    print("ME : ", joke)
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


def getWeatherReport(city):
    api_key = "bd5e378503939ddaee76f12ad7a97608"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)

    main_weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    report = f"The weather in {city} is {main_weather}. " \
             f"The humidity is {humidity}% and the wind speed is {wind_speed} meter/second."

    return report


def search_button_clicked():
    query = search_entry.get()
    if query:
        result = searchGoogle(query, num_sentences=4)
        if result:
            result_text.config(state=tk.NORMAL)
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, result)
            result_text.config(state=tk.DISABLED)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, "No results found on Google.")
            result_text.config(state=tk.DISABLED)


def main():
    speak("STARTING...")
    wishMe()

    root = tk.Tk()
    root.title("Virtual Assistant")
    root.geometry("400x300")

    search_label = tk.Label(root, text="Enter your query:")
    search_label.pack()

    search_entry = tk.Entry(root, width=40)
    search_entry.pack()

    search_button = tk.Button(root, text="Search", command=search_button_clicked)
    search_button.pack()

    result_text = tk.Text(root, width=50, height=10, state=tk.DISABLED)
    result_text.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
