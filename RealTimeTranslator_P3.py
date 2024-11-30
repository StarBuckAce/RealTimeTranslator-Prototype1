import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import tkinter as tk
from tkinter import ttk
import time

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "API is not available"

# Function to translate text
def translate_text(text, dest_language='es'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest_language)
        print(f"Translated: {translated.text}")
        return translated.text
    except Exception as e:
        return f"Translation error: {e}"

# Function to convert text to speech with unique filenames
def text_to_speech(text, language='es'):
    timestamp = int(time.time())  # Generate a unique timestamp
    filename = f"output_{timestamp}.mp3"  # Use timestamp in the filename
    tts = gTTS(text=text, lang=language)
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

# Function to start the translation process
def start_translation():
    source_text = speech_to_text()
    if source_text:
        source_text_var.set(source_text)
        translated_text = translate_text(source_text, dest_language=target_language_var.get())
        translated_text_var.set(translated_text)
        text_to_speech(translated_text, language=target_language_var.get())

# Create main window
root = tk.Tk()
root.title("Real-Time Translator")
root.geometry("400x300")

# Variables
source_text_var = tk.StringVar()
translated_text_var = tk.StringVar()
target_language_var = tk.StringVar(value="es")  # Default to Spanish

# Widgets
tk.Label(root, text="Source Text:").pack(pady=5)
tk.Entry(root, textvariable=source_text_var, state='readonly', width=50).pack(pady=5)

tk.Label(root, text="Translated Text:").pack(pady=5)
tk.Entry(root, textvariable=translated_text_var, state='readonly', width=50).pack(pady=5)

tk.Label(root, text="Target Language:").pack(pady=5)
ttk.Combobox(root, textvariable=target_language_var, values=["es", "fr", "de", "it", "hi","ta","te","ja"]).pack(pady=8)

tk.Button(root, text="Translate", command=start_translation).pack(pady=20)

# Run the application
root.mainloop()
