import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
import pyjokes
import json
import pywhatkit
import time
import threading
import pyautogui

from bs4 import BeautifulSoup


print("STARTED....")
# MASTER = " DANGER"

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
    speak(' I am your Virtual Assistant. How Can I Help You Today')


# to take voice input and recognise the text
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"YOU said : {query}\n")
    except sr.UnknownValueError:
        print('NO AUDIO HEARED......')
        query=takeCommand()

    # except Exception as e:
    #     # print("Say that again please...")
    #     # speak("Say that again please...")
    #     query = takeCommand()
    return query

# TO FETCH THE DATE
def get_current_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f" Master Today's date is {current_date}")

# for google search
def searchGoogle(query, num_sentences=5):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    search_result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
    sentences = search_result.split(".")
    result = ". ".join(sentences[:num_sentences])
    return result

# CODE TO TELL JOKE 
def tellJoke():
    joke = pyjokes.get_joke()
    print(" ME : ",joke)
    speak("Here's a joke for you:")
    speak(joke)

# CODE TO FETCH LATEST  NEWS
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

# WETHER REPORT
def getWeatherReport(city):
    # THE CODE IS IMPORTANT ,IT IS THE OPENWETHER USER API KEY THAT ALLOW ACCES TO FETCH THE DETAILS
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
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

# to take screen shot
def take_screenshot():
    # Create the screenshots folder if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    screenshot_path = os.path.join("screenshots", "screenshot.png")
    pyautogui.screenshot(screenshot_path)
    speak("Screenshot taken and saved in Screenshot folder.")


# TIME COUNTER
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Countdown: {i} seconds")
        time.sleep(1)
    print("Countdown complete!")
    speak("Countdown complete!")


# CODE TO OPEN ANY WEBSITE
def open_website(website):
    speak(f"Opening {website}")
    url = f"https://www.{website}.com"
    webbrowser.open(url)



# Show the list of operations
def showOperations():
    speak("Here are some of the operations I can perform:")
    operations = [
        "1. Get the current time",
        "2. Get the current date",
        "3. Tell a joke",
        "4. Take a screenshot",
        "5. Start a countdown",
        "6. Play videos on YouTube",
        "7. Get the latest news",
        "8. Get the weather report",
        "9. Open The websites",
        "10.Open Mail ",
        "11. play music"
        "13. Search information on Wikipedia",
        "14. Search on Google"
    ]
    for operation in operations:
        print(operation)
        # speak(operation)


# MAIN EXECUTIVE PART 
def main():
    speak("STARTING...")
    wishMe()
    while True:
        query = takeCommand()
        if query:
            if 'shutdown' in query.lower() or 'exit' in query.lower() or 'stop' in query.lower():
                speak(" ok  Master.. I am Living... !")
                break

            elif 'time' in query.lower() or 'what is the time' in query.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Master the time is {strTime}")

            elif 'date' in query.lower() or 'what is the date' in query.lower():
                 get_current_date()
                 
         
            elif 'wikipedia' in query.lower() or 'search wikipedia' in query.lower() or 'in wikipedia' in query.lower() :
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    print("ME : ",results)
                    speak(results)
                    # this line also search on wikipidia
                    # pywhatkit.info(query)

                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any information on that topic.")
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple results for that query. Please be more specific.")


            elif 'screenshot' in query.lower() or 'take a screenshot' in query.lower():
                speak(" Taking a screenshot...")
                take_screenshot()

            elif 'countdown' in query.lower() or ' start countdown' in query.lower():
                    speak("How many seconds for the countdown?")
                    countdown_seconds = int(takeCommand())
                    speak(f"Starting countdown for {countdown_seconds} seconds...")
                    countdown(countdown_seconds)

            elif 'another joke' in query.lower() or 'tell me a joke' in query.lower() or  'a joke' in query.lower()  :
                tellJoke()

            elif 'who are you' in query.lower() or 'what is your name' in query.lower() or  'your name' in query.lower()  :
                speak("I AM virtual  ASSISTANT created by meggha and team.")

            elif 'operations' in query.lower() or 'what can you do' in query.lower():
                showOperations()

            # elif 'open youtube' in query.lower():
            #     speak("opening Youtube")
            #     url = "https://www.youtube.com"
            #     webbrowser.open(url)

            # elif 'open google' in query.lower():
            #     speak("OPENING GOOGLE...")
            #     url = "https://www.google.com"
            #     webbrowser.open(url)



            elif 'open mail' in query.lower() or 'open g mail' in query.lower() or 'mail' in query.lower():
                speak("OPENING mail")
                url = "https://mail.google.com/mail/"
                webbrowser.open(url)

            elif 'play music' in query.lower() or 'play song' in query.lower():
                speak("Playing Music..")
                songs_dir = "C:\\Users\\manu\\Music\\MUSIC"
                songs = os.listdir(songs_dir)
                # print(songs)
                os.startfile(os.path.join(songs_dir, songs[2]))

            elif 'in youtube' in query.lower() or 'play in youtube' in query.lower() or  'youtube play' in query.lower():
                yot=query.replace('playing on youtube',"")
                speak(yot)
                pywhatkit.playonyt(yot)

            elif 'open website' in query.lower() or 'open' in query.lower():
                speak("Sure, what website would you like to open?")
                website_name = takeCommand().lower()
                open_website(website_name)


            elif 'latest news' in query.lower() or 'news' in query.lower():
                    speak("Fetching the latest news...")
                    news = getLatestNews()
                    # this code print 10 headlines but reads onlu 2 NEWS....
                    if news:
                        speak("Here are the top 10 latest news headlines. I will read two of them for you. please check remainingin the console.:")
                        for i, headline in enumerate(news[:2]):  # Limiting to the top two headlines
                            print(f"{i + 1}. {headline}")
                            speak(f"{i + 1}. {headline}")
                        if len(news) > 2:
                            speak("You can check the remaining headlines in the console.")
                            for i, headline in enumerate(news[2:]):  # Printing the remaining headlines
                             print(f"{i + 3}. {headline}")

                    # THIS READS ALL THE 10 NEWS
                    # if news:
                    #     speak("Here are the 10 latest news headlines , i can read two of them for you :")
                    #     for i, headline in enumerate(news):
                    #         print(f"{i + 1}. {headline}")
                    # else:
                    #     speak("Sorry, I couldn't fetch the latest news at the moment.")


            elif 'weather' in query.lower() or 'weather report' in query.lower():
                speak("Please tell me the city name.")
                city_name = takeCommand()
                report = getWeatherReport(city_name)
                print( "ME : ",report)
                speak(report)

            else :
                speak("Searching on Internet...")
                result = searchGoogle(query, num_sentences=3)
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
