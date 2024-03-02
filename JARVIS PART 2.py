import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pygame
import smtplib
import os
import threading
import spacy

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

nlp = spacy.load("en_core_web_sm")

def speak(audio, voice='male'):
    if voice == 'male':
        engine.setProperty('voice', voices[0].id)
    elif voice == 'female':
        engine.setProperty('voice', voices[1].id)

    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak('Good Morning!')

    elif 12 <= hour < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    speak("I am Jarvis Sir! Please tell me how can I help you")

def play_music():
    music_dir = 'D:\\Music'
    songs = os.listdir(music_dir)

    if len(songs) == 0:
        speak("No music files found in the specified directory.")
        return

    pygame.init()
    pygame.mixer.init()

    current_song_index = 0
    pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))
    pygame.mixer.music.play()

    def listen_for_commands():
        nonlocal current_song_index
        while pygame.mixer.music.get_busy():
            command = take_command()
            if 'pause music' in command:
                pygame.mixer.music.pause()
                speak("Music paused.")
            elif 'resume music' in command:
                pygame.mixer.music.unpause()
                speak("Resuming music.")
            elif 'next song' in command:
                current_song_index[0] = (current_song_index[0] + 1) % len(songs)
                pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index[0]]))
                pygame.mixer.music.play()
                speak("Playing next song.")
            elif 'stop music' in command:
                pygame.mixer.music.stop()
                speak("Music stopped.")
                break

    command_thread = threading.Thread(target=listen_for_commands)
    command_thread.start()

    # Wait for the command thread to finish
    command_thread.join()

def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

def take_command():
    # takes microphone input from the user

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing----")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return 'None'
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return 'None'

    return query.lower()

def get_intent(query):
    doc = nlp(query)
    intent = None

    for token in doc:
        if token.text.lower() == 'play' and token.dep_ == 'ROOT':
            intent = 'play_music'
        elif 'wikipedia' in token.text.lower():
            intent = 'search_wikipedia'
        elif intent == 'open_youtube':
            webbrowser.open("youtube.com")
        elif intent == 'open_google':
            webbrowser.open("google.com")
        elif 'sleep' in query:
            jarvis_sleep()

    return intent

def search_wikipedia(query):
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except wikipedia.DisambiguationError:
        speak(f"There are multiple results for {query}. Please be more specific.")
    except wikipedia.PageError:
        speak(f"Sorry, I couldn't find any information on {query}.")

def jarvis_sleep():
    speak("Goodbye! Jarvis is going to sleep.")
    exit()

if __name__ == '__main__':
    wish_me()
    conversation_history = []

    while True:
        query = take_command()
        intent = get_intent(query)

        # Logic for executing tasks based on intent
        if intent == 'play_music':
            play_music()
        elif intent == 'search_wikipedia':
            search_wikipedia(query)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")
        elif 'open code' in query:
            code_path = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = "recipient_email@gmail.com"
                send_email(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")

        else:
            response = f"I'm sorry, I didn't understand that."
            speak(response)
        
        # Update conversation history
        conversation_history.append(query)
