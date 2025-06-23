import os
import yaml
import requests
import json
import colorama


title = "Ollama YouTube Meta Generator"
message = "YouTube Meta Generator is running..."

with open("../../config.yml", "r", encoding="utf-8") as configuration:
    config = yaml.safe_load(configuration)

metin = input("Video için konu giriniz: ")

prompt = f"""
Aşağıda verilen konu için YouTube Shorts videosuna uygun şu meta verileri oluştur:

🎯 YOUTUBE TITLE (1 adet):
- Maksimum 60 karakter
- Dikkat çekici ve merak uyandırıcı
- Emoji kullanarak göze çarpıcı
- Anahtar kelimeleri içeren

🎯 YOUTUBE DESCRIPTION (1 adet):
- 150-200 kelime arası
- Video içeriğini özetleyen
- Hashtag'ler dahil
- Call-to-action içeren
- Anahtar kelimeleri stratejik yerleştirme

🎯 SEO KEYWORDS (10 adet):
- En önemli 10 anahtar kelime
- Virgülle ayrılmış liste
- Türkçe arama terimlerine odaklı

Video konusu: {metin}

Format:
TITLE: [başlık buraya]

DESCRIPTION: 
[açıklama buraya]

KEYWORDS: 
[anahtar kelimeler buraya]
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
    
    if response.status_code == 200:
        response_data = response.json()

        if "message" in response_data:
            cevap = response_data["message"]["content"]
        elif "response" in response_data:
            cevap = response_data["response"]
        else:
            print("Beklenmeyen response format'ı:", response_data.keys())
            cevap = str(response_data)
        
        print("\n" + "="*50)
        print("🎥 YOUTUBE META VERİLERİ OLUŞTURULDU")
        print("="*50)
        print(cevap)
        print("="*50)
        
        lines = cevap.split('\n')
        title_text = ""
        description_text = ""
        keywords_text = ""
        
        current_section = ""
        for line in lines:
            if line.strip().startswith("TITLE:"):
                current_section = "title"
                title_text = line.replace("TITLE:", "").strip()
            elif line.strip().startswith("DESCRIPTION:"):
                current_section = "description"
            elif line.strip().startswith("KEYWORDS:"):
                current_section = "keywords"
            elif line.strip() and current_section == "description":
                description_text += line.strip() + " "
            elif line.strip() and current_section == "keywords":
                keywords_text += line.strip() + " "
        
        if title_text or description_text or keywords_text:
            print("\n📋 AYRIŞTIRILMIŞ META VERİLER:")
            print("-" * 30)
            if title_text:
                print(f"📌 BAŞLIK: {title_text}")
            if description_text:
                print(f"📝 AÇIKLAMA: {description_text.strip()}")
            if keywords_text:
                print(f"🔍 ANAHTAR KELİMELER: {keywords_text.strip()}")
            
    else:
        print(f"API Hatası: {response.status_code}")
        print(f"Hata mesajı: {response.text}")
        
except Exception as hata:
    print(f"Hata: {hata}")
    print(f"Hata tipi: {type(hata)}") 