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
import openai
import pywhatkit
from spotipy.oauth2 import SpotifyOAuth



from bs4 import BeautifulSoup


print("STARTED....")
MASTER = " DANGER"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    # print("TIME IS: ", hour)

    if 0 <= hour < 12:
        speak("Good morning Master")

    elif 12 <= hour < 18:
        speak("Good afternoon Master")

    else:
        speak("Good evening Master")

    # speak("I am your assistant. How may I help you?")
    speak(' I am your Virtual Assistant. How Can I Help You Today')



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"YOU said: {query}\n")

# //////////////////////////////////////////////////////////////
    except sr.UnknownValueError:
        print('NO AUDIO HEARED......')
        query=takeCommand()

    # except Exception as e:
    #     # print("Say that again please...")
    #     # speak("Say that again please...")
    #     query = takeCommand()

    return query



def searchGoogle(query, num_sentences=10):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    search_result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
    sentences = search_result.split(".")
    # Remove [^#^] citations in response
    
    # bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
    result = ". ".join(sentences[:num_sentences])
    return result

def tellJoke():
    joke = pyjokes.get_joke()
    print(" ME : ",joke)
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

    # Send a GET request to the API and retrieve the response
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the relevant weather information
    main_weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    # Create the weather report string
    report = f"The weather in {city} is {main_weather}  " \
             f"The humidity is {humidity}% and the wind speed is {wind_speed} meter/second. "

    return report








def main():
    speak("STARTING...")
    wishMe()

    while True:
        query = takeCommand()

        if query:
            if 'stop' in query.lower() or 'exit' in query.lower():
                speak(" ok  Master.. I am Living... !")
                break
         
        if 'wikipedia' in query.lower() or 'search wikipedia' in query.lower():
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                print("ME : ",results)
                speak(results)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any information on that topic.")
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results for that query. Please be more specific.")


        elif 'open youtube' in query.lower():
            speak("opening Youtube")
            url = "https://www.youtube.com"
            webbrowser.open(url)

        elif 'open google' in query.lower():
            speak("OPENING GOOGLE...")
            url = "https://www.google.com"
            webbrowser.open(url)

        elif 'open mail' in query.lower() or 'open g mail' in query.lower():
            speak("OPENING mail")
            url = "https://mail.google.com/mail/"
            webbrowser.open(url)

        elif 'play music' in query.lower() or 'play song' in query.lower():
            speak("Playing Music..")
            songs_dir = "C:\\Users\\manu\\Music\\MUSIC"
            songs = os.listdir(songs_dir)
            # print(songs)
            os.startfile(os.path.join(songs_dir, songs[2]))

        elif 'play youtube' in query.lower() or 'play in youtube' in query.lower() or  'youtube play' in query.lower():
            yot=query.replace('playing on youtube',"")
            speak(yot)
            pywhatkit.playonyt(yot)


        elif 'the time' in query.lower() or 'what is the time' in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Master the time is {strTime}")


        elif 'another joke' in query.lower() or 'tell me a joke' in query.lower() or  'a joke' in query.lower()  :
            tellJoke()

        elif 'who are you' in query.lower() or 'what is your name' in query.lower() or  'your name' in query.lower()  :
            speak("I AM virtual  ASSISTANT created by meggha and team for the semister project")

        elif 'latest news' in query.lower() or 'news' in query.lower():
                speak("Fetching the latest news...")
                news = getLatestNews()
                if news:
                    speak("Here are the 10 latest news headlines:")
                    for i, headline in enumerate(news):
                        speak(f"{i + 1}. {headline}")
                else:
                    speak("Sorry, I couldn't fetch the latest news at the moment.")


        elif 'weather' in query.lower() or 'weather report' in query.lower():
            speak("Please tell me the city name.")
            city_name = takeCommand()
            report = getWeatherReport(city_name)
            print( "ME : ",report)
            speak(report)

        else :
            speak("Searching on Internet...")
            result = searchGoogle(query, num_sentences=4)
            
            # below code opens and serches in google..***
            # pywhatkit.search(query)

            if result:
                # speak("Here are the top search results:")
                print("ME : ",result)
                speak(result)
            else:
                speak("ME : No results found on Google.")
    



if __name__ == "__main__":
    main()
