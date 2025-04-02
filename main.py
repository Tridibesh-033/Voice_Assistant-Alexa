import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import os
import psutil  # For battery status
import datetime
import wikipedia
import feedparser
import socket

recognizer=sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)   # female voice
engine.setProperty("rate", 170)             # Reduce speed for clarity

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    # Exit Command
    if "stop" in c.lower() or "exit" in c.lower():
        speak("Goodbye, have a nice day")
        exit()
    
    # Web & Social Media Commands
    elif "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open twitter" in c.lower():
        webbrowser.open("https://www.twitter.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")

    elif "open github" in c.lower():
        webbrowser.open("https://www.github.com")
    
    elif "open whatsapp web" in c.lower():
        webbrowser.open("https://web.whatsapp.com/")

    # Play music
    elif c.lower().startswith("play"):
        song=c.lower().split(" ", 1)[1]
        if song in musicLibrary.music:
            link=musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")

    # News
    elif "news" in c.lower():
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        news_feed = feedparser.parse(url)

        for entry in news_feed.entries[:5]:
            print(entry.title)
            speak(entry.title)

    # Wikipedia Search
    elif "who is" in c.lower() or "what is" in c.lower():
        query = c.replace("who is", "").replace("what is", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {result}")
            print(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any information. Here is a Google search.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    # Time and Date
    elif "current time" in c.lower():
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time}")
        print(f"The current time is {time}")

    elif "today's date" in c.lower():
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {date}")
        print(f"Today's date is {date}")

    # System Status Commands
    elif "battery status" in c.lower():
        battery = psutil.sensors_battery()
        percent = battery.percent
        speak(f"Your system's battery is at {percent} percent")
        print(f"Your system's battery is at {percent} percent")

    elif "ip address" in c.lower():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        speak(f"Your IP address is {ip_address}")
        print(f"Your IP address is {ip_address}")

    elif "cpu usage" in c.lower():
        cpu_usage = psutil.cpu_percent(interval=1)
        speak(f"Your CPU usage is at {cpu_usage} percent")
        print(f"Your CPU usage is at {cpu_usage} percent")

    elif "ram usage" in c.lower():
        ram_usage = psutil.virtual_memory().percent
        speak(f"Your RAM usage is at {ram_usage} percent")
        print(f"Your RAM usage is at {ram_usage} percent")

    # Open Installed Applications
    elif "open notepad" in c.lower():
        os.system("notepad")

    elif "open calculator" in c.lower():
        os.system("calc")

    elif "open command prompt" in c.lower() or "open cmd" in c.lower():
        os.system("cmd")

    elif "open task manager" in c.lower():
        os.system("taskmgr")

    elif "open paint" in c.lower():
        os.system("mspaint")

    elif "open control panel" in c.lower():
        os.system("control")

    elif "open settings" in c.lower():
        os.system("start ms-settings:")


if __name__ == "__main__":
    speak("Initializing Alexa")
    while True:
        r = sr.Recognizer()
        r.energy_threshold = 300
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=10, phrase_time_limit=8)

            print("Recognizing...")
            try:
                greet = r.recognize_google(audio)
                print(greet)
                if greet.lower() == "alexa":
                    speak("Yes, I am listening")
                with sr.Microphone() as source:
                    print("Alexa Active...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=10, phrase_time_limit=8)
                    try:
                        command = r.recognize_google(audio)
                        processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I couldn't understand that.")
                    except sr.RequestError:
                        speak("Network error: Please check your internet connection.")
            except sr.RequestError:
                speak("Network error: Please check your internet connection.")
        except Exception as e:
            print("Error; {0}".format(e))
