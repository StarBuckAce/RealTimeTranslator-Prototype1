import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import easyocr
import tkinter as tk
from tkinter import ttk, filedialog
import time

# Speech-to-Text
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

# Text Translation
def translate_text(text, dest_language='es'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest_language)
        print(f"Translated: {translated.text}")
        return translated.text
    except Exception as e:
        return f"Translation error: {e}"

# Text-to-Speech
def text_to_speech(text, language='es'):
    timestamp = int(time.time())  # Generate a unique timestamp
    filename = f"output_{timestamp}.mp3"  # Use timestamp in the filename
    tts = gTTS(text=text, lang=language)
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

# Image-to-Text
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    extracted_text = " ".join([result[1] for result in results])
    return extracted_text

# GUI Actions
def start_translation():
    source_text = speech_to_text()
    if source_text:
        source_text_var.set(source_text)
        translated_text = translate_text(source_text, dest_language=target_language_var.get())
        translated_text_var.set(translated_text)
        text_to_speech(translated_text, language=target_language_var.get())

def translate_from_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        extracted_text = extract_text_from_image(file_path)
        source_text_var.set(extracted_text)
        translated_text = translate_text(extracted_text, dest_language=target_language_var.get())
        translated_text_var.set(translated_text)
        text_to_speech(translated_text, language=target_language_var.get())

# GUI Setup
root = tk.Tk()
root.title("Real-Time Translator")
root.geometry("1080x1920")

# Variables
source_text_var = tk.StringVar()
translated_text_var = tk.StringVar()
target_language_var = tk.StringVar(value="es")  # Default to Spanish

# Layout
tk.Label(root, text="Speech-to-Text Translator", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Translate Speech", command=start_translation).pack(pady=5)

tk.Label(root, text="Image-to-Text Translator", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Translate Image", command=translate_from_image).pack(pady=5)

tk.Label(root, text="Source Text:").pack(pady=5)
tk.Entry(root, textvariable=source_text_var, state='readonly', width=50).pack(pady=15)

tk.Label(root, text="Translated Text:").pack(pady=5)
tk.Entry(root, textvariable=translated_text_var, state='readonly', width=50).pack(pady=15)

tk.Label(root, text="Target Language:").pack(pady=5)
ttk.Combobox(root, textvariable=target_language_var, values=["es", "fr", "de", "it", "hi", "zh-cn","ta","te","ja"]).pack(pady=5)

# Run App
root.mainloop()
