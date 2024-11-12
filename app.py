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
    'ru': 'Russian',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'sw': 'Kiswahili'
}

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
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
        
        try:
            translated_text = translate_text(text, src_lang, dest_lang)
            audio_file = translate_text_to_speech(translated_text, dest_lang)
            return jsonify({'translated_text': translated_text, 'audio_file': '/' + audio_file})
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.mkdir('static')
    app.run(debug=True)
