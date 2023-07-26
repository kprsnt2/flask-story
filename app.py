import speech_recognition as sr
from gtts import gTTS
import pygame
import random
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = "12333222"  # Add a secret key for session management

# Sample stories database
stories = [
    "Once upon a time, there was a little rabbit.",
    "In a magical land far away, there lived a brave knight.",
    "A long time ago, in a deep forest, there was a wise owl.",
    "On a sunny day, a mischievous monkey swung from tree to tree.",
    "Once upon a time, there was a shiny red train chugging along the tracks.",
    "In a bustling city, a double-decker bus roamed the streets, picking up passengers.",
    "A long drive through the countryside, a family of bears went on a car adventure.",
]


def listen_for_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)
        return user_input.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Could not request results. Please check your internet connection.")
        return ""

def generate_story_response():
    return random.choice(stories)

def speak_text(text):
    tts = gTTS(text=text, lang="en")
    audio_file = "response.mp3"
    tts.save(audio_file)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    print("Chatbot:", text)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST", "GET"])
def chat():
    if "user_input" not in session:
        session["user_input"] = ""

    user_input = request.form["user_input"].lower()

    if "exit" in user_input:
        response = "Goodbye!"
    elif "tell me a story" in user_input or session.get("last_story"):
        story_response = generate_story_response()
        speak_text(story_response)
        session["last_story"] = story_response  # Save the last story in the session
        return render_template("chat.html", user_input=user_input, response=story_response)
    else:
        response = "Sorry, I didn't understand that. Please say 'tell me a story' or 'exit'."
        return render_template("chat.html", user_input=user_input, response=response)

@app.route("/voice_input", methods=["POST"])
def voice_input():
    user_input = listen_for_voice()
    return user_input

if __name__ == "__main__":
    app.run(debug=True)