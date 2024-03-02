import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pygame
import smtplib
import os



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        speak('Good Morning!')

    elif hour >=12 and hour < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    speak("I am Jarvis Sir ! Please tell me how can i help you")

def playMusic():
    music_dir = 'D:\\Music'
    songs = os.listdir(music_dir)
    
    if len(songs) == 0:
        speak("No music files found in the specified directory.")
        return

    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(os.path.join(music_dir, songs[0]))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('rohitraman0512@gmail.com', 'your_password')
    server.sendmail('rohitraman0512@gmail.com', to, content)
    server.close()

def takeCommand():
    # takes microphone input from user

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing----")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)

        print("Say that again please!------------")
        return 'None'
    return query

if __name__ == '__main__':
    wishMe()
    if 1:
        query = takeCommand().lower()
         # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")
        
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            playMusic()

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\ROHIT.R\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "rohitraman0512@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend Rohit. I am not able to send this email")   

        


