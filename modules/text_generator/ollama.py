import os
import yaml
import requests
import json
import colorama


title = "Ollama Text Generator"
message = "Text Generator is running..."

with open("../../config.yml", "r", encoding="utf-8") as configuration:
    config = yaml.safe_load(configuration)

metin = input("Video için konu giriniz: ")

prompt = f"""
Aşağıda verilen başlık ve madde sırasına göre, YouTube Shorts için kısa, dikkat çekici ve konuşma diliyle yazılmış bir video metni hazırla.

🎥 Video Yapısı:

Dikkat çekici giriş (1 cümle)

Madde madde bilgi akışı (doğal ve kısa anlatımlı, 5 sebep)

Net, akılda kalıcı kapanış cümlesi (video kapanış metni)

🎯 Amaç: İzleyiciyi şaşırtmak, kısa sürede bilgi vermek.
🎯 Hedef kittle: Meraklı, genç sosyal medya kullanıcıları.
🕐 Süre: En fazla 700 karaktere sığacak uzunlukta yaz.

Video konusu: {metin}

"""

try:
    response = requests.post(
        'http://localhost:11434/api/chat',
        json={
            "model": "gemma3:12b",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )
    
    # Debug için response
    # print("Response status:", response.status_code)
    # print("Response content:", response.text)
    
    if response.status_code == 200:
        response_data = response.json()
        print("Response JSON:", response_data)

        if "message" in response_data:
            cevap = response_data["message"]["content"]
        elif "response" in response_data:
            cevap = response_data["response"]
        else:
            print("Beklenmeyen response format'ı:", response_data.keys())
            cevap = str(response_data)
        
        print("\n=== OLUŞTURULAN METİN ===")
        print(cevap)
    else:
        print(f"API Hatası: {response.status_code}")
        print(f"Hata mesajı: {response.text}")
        
except Exception as hata:
    print(f"Hata: {hata}")
    print(f"Hata tipi: {type(hata)}")
