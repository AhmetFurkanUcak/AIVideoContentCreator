import os
import yaml
import requests
import json
import colorama


title = "Audio Generator"
message = "Audio Generator is running..."

with open("../config.yml", "r", encoding="utf-8") as configuration:
    config = yaml.safe_load(configuration)

with open("./audio_generator/voice.json", "r", encoding="utf-8") as voice_file:
    voices = json.load(voice_file)

def select_voice():
    global choice
    for i, voice in enumerate(voices):
        print(f"{i + 1}. Voice ID: {voice['id']}, 'name': {voice['name']}, 'native_language': {voice['native_language']}, 'Gender': {voice['gender']}")
    choice = input("Enter the number of the voice you want to select: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(voices):
            return voices[choice]['id']
            selected_voice = voices[choice]
            print(f"You selected: {voices[choice]['name']} (ID: {voices[choice]['id']})")
        else:
            print("Invalid choice. Please try again.")
            return select_voice()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return select_voice()

select_voice()
choised_voice = voices[choice]['id']


def input_text():
    global text
    text = input("Enter the text you want to convert to audio: ")
    if not text.strip():
        print("Text cannot be empty. Please try again.")
        return input_text()
    return text

input_text()

def generate_audio(text, voice_id):

    key = config.get("ELEVENLABS_API_KEY")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voices[choice]['id']}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key
    }
    
    print(f"Debug - stability: {voices[choice]['default_stability']} (type: {type(voices[choice]['default_stability'])})")
    print(f"Debug - similarity_boost: {voices[choice]['default_similarity_boost']} (type: {type(voices[choice]['default_similarity_boost'])})")
    print(f"Debug - speed: {voices[choice]['default_speed']} (type: {type(voices[choice]['default_speed'])})")
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": voices[choice]['default_stability'],
            "similarity_boost": voices[choice]['default_similarity_boost'],
            "speed": voices[choice]['default_speed']
        }
    }
    
    print(f"Debug - data: {data}")

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        safe_text = "".join(c for c in text[:20] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{voices[choice]['name']}_{safe_text}.mp3"
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Ses dosyası oluşturuldu: {filename}")
        return filename
    else:
        print(f"❌ Hata: {response.status_code} - {response.text}")
        return None

generate_audio(text, choised_voice) 