import pyttsx3
import speech_recognition as sr
import datetime
import os
import subprocess
import webbrowser

def speak(audio):
    print(f"Assistant: {audio}")
    engine.say(audio)
    engine.runAndWait()

def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("LISTENING.....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You just said: {query}")
    except:
        speak("Sorry, I did not catch that. Please say it again.")
        return "none"
    return query.lower()

def wishings():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning madam")
    elif hour < 17:
        speak("Good afternoon madam")
    elif hour < 21:
        speak("Good evening madam")
    else:
        speak("Good night madam")

def open_browser(browser_name):
    try:
        subprocess.run(f"start {browser_name}", shell=True, check=True)
        return True
    except:
        browser_paths = {
            "chrome": [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
        }
        paths = browser_paths.get(browser_name.lower(), [])
        for path in paths:
            if os.path.exists(path):
                os.startfile(path)
                return True
        return False

def close_app(app_name):
    app_process = {
        "chrome": "chrome.exe",
        "calculator": "Calculator.exe",
        "calc": "Calculator.exe"
    }
    process = app_process.get(app_name)
    if process:
        try:
            subprocess.run(f"taskkill /f /im {process}", shell=True)
            speak(f"Closed {app_name}")
        except:
            speak(f"Could not close {app_name}")
    else:
        speak(f"I don't know how to close {app_name}")

# Initialize TTS
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

if __name__ == "__main__":
    wishings()
    while True:
        query = commands()
        if query == "none":
            continue

        if any(stop_word in query for stop_word in ['stop', 'exit', 'quit']):
            speak("Thank you madam. Stopping the assistant.")
            break

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open chrome' in query:
            speak("Opening Chrome application madam")
            if open_browser("chrome"):
                speak("What would you like to search on Google?")
                search_query = commands()
                if search_query != "none":
                    url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                    webbrowser.open(url)
                    speak(f"Searching Google for {search_query}")
            else:
                speak("Sorry madam, I could not open Chrome. Please check if it is installed.")

        elif 'close chrome' in query:
            close_app("chrome")

        elif 'youtube' in query:
            speak("What would you like to search on YouTube?")
            yt_query = commands()
            if yt_query != "none":
                yt_url = f"https://www.youtube.com/results?search_query={yt_query.replace(' ', '+')}"
                webbrowser.open(yt_url)
                speak(f"Searching YouTube for {yt_query}")

        elif 'maps' in query or 'google maps' in query:
            speak("Which location would you like to search on Google Maps?")
            maps_query = commands()
            if maps_query != "none":
                maps_url = f"https://www.google.com/maps/search/{maps_query.replace(' ', '+')}"
                webbrowser.open(maps_url)
                speak(f"Showing {maps_query} on Google Maps")

        elif 'weather' in query:
            speak("Which city's weather would you like to check?")
            city_query = commands()
            if city_query != "none":
                weather_url = f"https://www.google.com/search?q=weather+{city_query.replace(' ', '+')}"
                webbrowser.open(weather_url)
                speak(f"Showing weather for {city_query}")

        elif 'open calculator' in query:
            speak("Opening calculator madam")
            try:
                subprocess.run("calc", shell=True)
            except:
                speak("Sorry madam, I could not open the calculator.")

        elif 'close calculator' in query or 'close calc' in query:
            close_app("calc")

        elif 'open website' in query:
            speak("Please say the website you want to open, for example google.com")
            site_query = commands()
            if site_query != "none":
                if not site_query.startswith("http"):
                    site_query = "https://" + site_query
                webbrowser.open(site_query)
                speak(f"Opening {site_query}")

        else:
            speak("Sorry madam, I don't recognize that command.")
