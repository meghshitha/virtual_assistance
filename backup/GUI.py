import turtle
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
import subprocess
import pyautogui
from bs4 import BeautifulSoup
import random
# from ecapture import ecapture as ec

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def textcreate(message):
    output_text.clear()  # Clear the output text
    output_text.write(message, align="center", font=("Arial", 14, "normal"))

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
        message = "Listening..." #to output the msg to Screen
        textcreate(message)  #the function that outputs the msg to GUI      
        audio = r.listen(source) # to leaston the audio/input

    try: #to analyse or recognise the input 
        message = "Recognizing..." 
        textcreate(message)
        query = r.recognize_google(audio, language='en-in') # perform speech recognition using the Google Web Speech API.
        message = f"YOU said: {query}\n"
        textcreate(message)

        # if no voice/audio heard 
    except sr.UnknownValueError:
        message = 'NO AUDIO HEARD......'
        textcreate(message)
        query = takeCommand()
    return query

# TO FETCH THE DATE
def get_current_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    message = current_date
    textcreate(message)
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
# def tellJoke():
#     joke = pyjokes.get_joke()
#     message = "ME :" + joke
#     textcreate(message)    
#     speak("Here's a joke for you:")
#     speak(joke)
def load_jokes():
    jokes = []
    with open('jokes.txt', 'r') as file:
        for line in file:
            joke = line.strip()
            jokes.append(joke)
    return jokes

def get_random_joke(jokes):
    random_joke = random.choice(jokes)
    return random_joke

def tell_joke():
    all_jokes = load_jokes()
    joke = get_random_joke(all_jokes)
    return joke

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
    api_key = "bd5e378503939ddaee76f12ad7a97608"      # THE CODE IS IMPORTANT ,IT IS THE OPENWETHER USER API KEY THAT ALLOW ACCES TO FETCH THE DETAILS
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)     # Send a GET request to the API and retrieve the response
    data = json.loads(response.text)      # Parse the JSON response

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
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #just to save the pic with the date
    screenshot_path = os.path.join("screenshots", f"screenshot_{current_time}.png")
    pyautogui.screenshot(screenshot_path)
    speak("Screenshot taken and saved in Screenshot folder.")

# TIME COUNTER
def countdown(seconds):
    try :
        for i in range(seconds, 0, -1):
            message = f"Countdown: {i} seconds"
            textcreate(message)
            time.sleep(1)
            message = f"Countdown: {i} seconds"
            textcreate(message)
        speak("Countdown complete!")

    except ValueError:
        speak("Invalid input. Please enter a valid number of seconds.")
        textcreate("Invalid input. Please enter a valid number of seconds.")
        takeCommand()

# CODE TO OPEN ANY WEBSITE
def open_website(website):
    speak(f"Opening {website}")
    url = f"https://www.{website}.com"
    webbrowser.open(url)

# Open a local application
def open_application(application_name):
    application_name = application_name.lower()
    application_path = None
    
    # Define the paths for your applications
    application_paths = {
        "notepad": r"C:\\Windows\\System32\\notepad.exe",
        "calculator": r"C:\\Windows\\System32\\calc.exe",
        # "paint": r"C:\\Windows\\System32\\mspaint.exe",
        "explorer": r"C:\\Windows\\explorer.exe",
        "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "control pannel": r"C:\Users\USER\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools\controlpanel.exe",
        "task manager": r"C:\\Windows\\System32\\taskmgr.exe",
        "pictures" :r"C:\Users\USER\Pictures",
        "Documents":r"C:\Users\USER\Documents"
        # Add more applications and their paths here
    }
    # Find the path of the requested application
    if application_name in application_paths:
        application_path = application_paths[application_name]

    # Open the application if the path is found
    if application_path:
        subprocess.Popen(application_path)
        speak(f"Opening {application_name} application")
    else:
        speak(f"Sorry, I couldn't find the {application_name} application")

# Show the list of operations
def showOperations():
    speak("Here are some of the operations I can perform:")
    operations =[
        "1. Get the current time",
        "2. Get the current date",
        "3. Tell a joke",
        "4. Take a screenshot",
        "5. Start a countdown",
        "6. Play videos on YouTube",
        "7. Get the latest news",
        "8. Get the weather report",
        "9. Open The websites",
        "10. Open Mail ",
        "11. play music"
        "13. Search information on Wikipedia",
        "14. Search on Google"
        "15. open application"
    ]
    for operation in operations:
        speak(operation)
        # message = operation
        textcreate(operation)
        # return operation

# Function to stop the virtual assistant
def stop_virtual_assistant(x, y):
    textcreate("Stopping virtual assistant...")
    speak("Stopping virtual assistant...")
    turtle.bye()


# MAIN EXECUTIVE PART 
# def main():
def start_virtual_assistant(x, y):
    #speak("STARTING...")
    textcreate("Starting virtual assistant...")
    wishMe()

    while True:
        query = takeCommand() #to take the input when program starts

        if query:
            if 'shutdown' in query.lower() or 'exit' in query.lower() or 'stop' in query.lower():
                speak(" ok  Master  I am Living... !")
                stop_virtual_assistant(x, y)
                break

            elif 'time' in query.lower() or 'what is the time' in query.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Master the time is {strTime}")

            elif 'date' in query.lower() or 'what is the date' in query.lower() or 'today date' in query.lower():
                 get_current_date()
                 
            elif 'wikipedia' in query.lower() or 'search wikipedia' in query.lower() or 'in wikipedia' in query.lower() :
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    textcreate(results)
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

            elif 'another joke' in query.lower() or 'tell me a joke' in query.lower() or  'a joke' in query.lower() or  'some joke' in query.lower() or  'joke' in query.lower() :
                    # tellJoke()
                    j=tell_joke()
                    textcreate(j)
                    speak(j)


            elif 'who are you' in query.lower() or 'what is your name' in query.lower() or  'about you' in query.lower()  :
                    speak("I AM virtual  ASSISTANT created by Finall year students of Seshadripuram degree college ")

            elif 'operations' in query.lower() or 'what can you do' in query.lower() or 'what do you do' in query.lower():
                    speak("the operations are given Below...")
                    textcreate("the operations are given Below...")
                    # showOperations()

            elif 'open youtube' in query.lower():
                speak("opening Youtube")
                url = "https://www.youtube.com"
                webbrowser.open(url)

            elif 'open google' in query.lower():
                speak("OPENING GOOGLE...")
                url = "https://www.google.com"
                webbrowser.open(url)


            elif 'open mail' in query.lower() or 'open g mail' in query.lower() or 'mail' in query.lower():
                    speak("OPENING mail")
                    url = "https://mail.google.com/mail/"
                    webbrowser.open(url)

            elif 'play music' in query.lower() or 'play song' in query.lower() or 'play some music' in query.lower():
                    speak("Playing Music..")
                    songs_dir = "C:\\Users\\USER\\Desktop\\dhanu-music\\music-2"
                    songs = os.listdir(songs_dir)
                    os.startfile(os.path.join(songs_dir, songs[0]))

            elif 'in youtube' in query.lower() or 'play in youtube' in query.lower() or  'search youtube' in query.lower():
                    yot=query.replace('playing on youtube',"")
                    speak(yot)
                    pywhatkit.playonyt(yot)

            elif 'hello' in query.lower()or 'hii' in query.lower() :
                    textcreate("Hello...")
                    speak('Hello Master')

            elif 'sing a song' in query.lower() or 'sing me a song' in query.lower() or 'can you sing a song' in query.lower() :
                    textcreate("sorry Master... i'm not so good at it.. if you want i can play some good music for you... do you want me to do that")
                    speak("sorry Master... I'm not so good at it.. if you want i can play some good music for you... do you want me to do that")
                    r=takeCommand()
                    if 'yes' in r or 's' in r or 'ya' in r or 'ok' in r:
                        speak("Playing Music..")
                        songs_dir = "C:\\Users\\USER\\Desktop\\dhanu-music\\music-2"
                        songs = os.listdir(songs_dir)
                        os.startfile(os.path.join(songs_dir, songs[0]))
                         
                    elif 'no' in r:
                        speak("ok master")

            elif 'can you dance' in query.lower() or 'dance with me' in query.lower():
                    textcreate('sorry... i skipped those classes...')
                    speak('sorry...Master  i skipped those classes...')


            elif 'open website' in query.lower() or 'website' in query.lower():
                    speak("Sure, what website would you like to open?")
                    website_name = takeCommand().lower()
                    open_website(website_name)

            elif 'open application' in query.lower() or 'open app' in query.lower():
                    speak("Sure, what application would you like to open?")
                    app_name = takeCommand().lower()
                    open_application(app_name)

            elif 'latest news' in query.lower() or 'news' in query.lower():
                    speak("Fetching the latest news...")
                    news = getLatestNews()
                    # this code print 10 headlines but reads onlu 2 NEWS....
                    if news:
                        speak("Here are the top 10 latest news headlines. I will read four of them for you. please check remainingin the console.:")

                        for i, headline in enumerate(news[:4]):  # Limiting to the top two headlines
                            textcreate(f"{i + 1}. {headline}")
                            # print(f"{i + 1}. {headline}")
                            speak(f"{i + 1}. {headline}")

                        if len(news) > 2:
                            speak("You can check the remaining headlines in the console.")
                            for i, headline in enumerate(news[2:]):  # Printing the remaining headlines
                            #  print(f"{i + 3}. {headline}")
                             textcreate(f"{i + 3}. {headline}")
                             
            #elif ' Do you have any hidden talents ' in query or ' hidden talents ':
                    #textcreate("Oh, I have plenty of hidden talents. Unfortunately, they're all hidden from me too.")
                    #speak("Oh, I have plenty of hidden talents. Unfortunately, they're all hidden from me too.")
                        

            elif 'weather' in query.lower() or 'weather report' in query.lower():
                    speak("Please tell me the city name.")
                    city_name = takeCommand()
                    report = getWeatherReport(city_name)
                    textcreate(report)
                    speak(report)

            
            elif 'who is ' in query.lower():
                person = query.split('for')[-1]
                info = wikipedia.summary(person, sentences = 3)
                textcreate(info)
                speak(info)
                

            elif 'google' in query.lower():
                 pywhatkit.search(query)

            # elif 'google' in query.lower() or ' search in google' in query.lower() :
            else:
                speak("Searching on Internet...")
                result = searchGoogle(query, num_sentences=3)
                # below code opens and serches in google..***
                # pywhatkit.search(query)
                if result:
                    # speak("Here are the top search results:")
                    textcreate(result)
                    speak(result)
                else:
                    speak("No results found on Google.")

            


# /////// GUI PART /////


turtle.tracer(1, 0)  # to hide graphics animation
turtle.hideturtle() 
turtle.speed(10) 

# Create the turtle window
window = turtle.Screen()
window.title("Virtual Assistant GUI")
window.bgcolor("white")

# /// FOR BUTTON

# Create the start button
start_button = turtle.Turtle()
start_button.penup()
start_button.goto(-400, -35)
start_button.shape("square")
start_button.color("green")
start_button.shapesize(4, 8)
start_button.onclick(start_virtual_assistant)

# Add text to the start button
start_text = turtle.Turtle()
start_text.penup()
start_text.goto(-400, -55)
start_text.color("black")
start_text.write("START", align="center", font=("Impact", 19, "bold"))
start_text.goto(-600,500) #this makes the pen hidde/out of screen

# Create the stop button
stop_button = turtle.Turtle()
stop_button.penup()
stop_button.goto(400, -35)
stop_button.shape("square")
stop_button.color("red")
stop_button.shapesize(4, 8)
stop_button.onclick(stop_virtual_assistant)


# Add text to the stop button
stop_text = turtle.Turtle()
stop_text.penup()
stop_text.goto(400, -55)
stop_text.color("black")
stop_text.write("STOP", align="center", font=("Impact", 19, "bold"))
stop_text.goto(-600,500) #this makes the pen hidde/out of screen

# Create the output text turtle
output_text = turtle.Turtle()
output_text.penup()
output_text.goto(-570, 280)
output_text.color("black")
output_text.hideturtle()
# output_text.goto(-600,500) #this makes the pen hidde/out of screen



# Create the output text box
# output_box = turtle.Turtle()
# output_box.penup()
# output_box.goto(-650, 300)
# output_box.pendown()
# output_box.color("black")
# output_box.fillcolor("white")
# output_box.begin_fill()
# for _ in range(2):
#     output_box.forward(1350)
#     output_box.right(90)
#     output_box.forward(250)
#     output_box.right(90)
# output_box.end_fill()
# output_box.penup()
# output_box.goto(0, 180)
# output_box.color("black")
# output_box.write("", align="center", font=("Arial", 14, "bold"))
# output_box.goto(-600,500) #this makes the pen hidde/out of screen




output_box = turtle.Turtle()
output_box.penup()
output_box.goto(-450, 50)
output_box.pendown()
output_box.color("black")
output_box.fillcolor("white")
output_box.begin_fill()
output_box.pensize(4)  
output_box.forward(900)
output_box.penup()

output_box.goto(-600,500)


    # output_box.right(90)
    # output_box.forward(250)
    # output_box.right(90)




# Create the output text turtle
output_text = turtle.Turtle()
output_text.penup()
output_text.goto(0, 160)
output_text.color("black")
output_text.hideturtle()
# output_text.goto(-600,500) #this makes the pen hidde/out of screen



#  operations list
op1=(   "1. Get the current time    "
        "2. Get the current date    "
        "3. Tell a joke     "
        "4. Take a screenshot    "
        "5. Start a countdown    "
    )

op2=(   "6. Play videos on YouTube    "
        "7. Get the latest news   "
        "  8. Get the weather report  "
        "  9. Open The websites   "
        " 10. Open Mail  "
        
        )
op3=( "11. play music    "
        "13. Search information on Wikipedia     "
        "14. Search on Google     "
        "15. open application    ")


stext = turtle.Turtle()
stext.penup()
stext.goto(100, -250)
stext.color("black")
stext.write(op1, align="center", font=("Arial", 15, "bold"))
stext.penup()
stext.goto(50, -320)
stext.write(op2, align="center", font=("Arial", 15, "bold"))
stext.penup()
stext.goto(50, -390)
stext.write(op3, align="center", font=("Arial", 15, "bold"))
stext.penup()
stext.goto(-600,500) #this makes the pen hidde/out of screen


# Run the turtle event loop
turtle.mainloop()
# The turtle.mainloop() function is used in the turtle module of Python to start the event loop for the turtle graphics. It continuously listens for and handles events such as mouse clicks and keypresses. It keeps the turtle window open until the user closes it.