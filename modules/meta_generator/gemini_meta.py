import requests
import yaml
import colorama
import os
import json
import time


with open("../../config.yml", "r", encoding="utf-8") as configuration:
    config = yaml.safe_load(configuration)

api_key = config["GEMINI_API_KEY"]

def generate_content_with_gemini(api_key, prompt):

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as hata:
        print(f"API çağrısında hata: {hata}")
        return None


def main():
    """
    YouTube Meta Generator
    """
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

    Cevap verirken sadece istenen formatı kullan, ekstra açıklama yapma.
    """

    result = generate_content_with_gemini(api_key, prompt)
    
    if result:
        try:
            response_text = result["candidates"][0]["content"]["parts"][0]["text"]
            
            print("\n" + "="*50)
            print("🎥 YOUTUBE META VERİLERİ OLUŞTURULDU (Gemini)")
            print("="*50)
            print(response_text)
            print("="*50)
            
            lines = response_text.split('\n')
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
                    
        except (KeyError, IndexError) as hata:
            print("Yanıt formatında hata:", hata)
            print("Ham yanıt:", json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("API çağrısı başarısız!")


if __name__ == "__main__":
    main()