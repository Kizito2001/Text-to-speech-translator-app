from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Add a list of supported languages for Google Translate and gTTS
supported_languages = {
    'en': 'English',
    'tl': 'Tagalog (Philippines)',
    'ms': 'Malay (Indonesia, Brunei, Malaysia, and Singapore)',
    'fr': 'French',
    'ru': 'Russian',  # Added Russian
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'sw': 'Kiswahili'  # Kiswahili language added
}

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    # Detect source language automatically if 'auto' is selected
    translated = translator.translate(text, src=src_lang if src_lang != 'auto' else None, dest=dest_lang)
    return translated.text

def translate_text_to_speech(text, dest_lang):
    audio_file = f'static/{str(uuid.uuid4())}.mp3'
    tts = gTTS(text, lang=dest_lang)
    tts.save(audio_file)
    return audio_file

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        src_lang = request.form['src_lang']
        dest_lang = request.form['dest_lang']
        translated_text = translate_text(text, src_lang, dest_lang)
        audio_file = translate_text_to_speech(translated_text, dest_lang)
        return jsonify({'audio_file': audio_file, 'translated_text': translated_text})
    return render_template('index.html', supported_languages=supported_languages)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the port specified by Render or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)

