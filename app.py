from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio_files'

# Handle translation and speech generation
@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    src_lang = request.form['src_lang']
    dest_lang = request.form['dest_lang']
    
    # Translate text
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    
    # Generate speech
    tts = gTTS(translated_text, lang=dest_lang)
    audio_file_name = f"{uuid.uuid4()}.mp3"
    audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file_name)
    tts.save(audio_file_path)
    
    return jsonify({
        "audio_file": audio_file_path,
        "translated_text": translated_text  # Send translated text as well
    })

# Display the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
