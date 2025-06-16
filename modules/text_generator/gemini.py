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
        response.raise_for_status()  # HTTP hatalarını kontrol et
        return response.json()
    except requests.exceptions.RequestException as hata:
        print(f"API çağrısında hata: {hata}")
        return None


def main():
    """
    Örnek kullanım
    """
    # metin = input("Video için konu giriniz: ")

    # # Örnek prompt
    # prompt = "Selam Gemini, Nasıl gidiyor?"
    
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

    örnek tip bir metinde yazayım ama konusu bu olmayacak.
    Uçakta sigara yasaksa, neden tuvalette kül tablası var? Garip değil mi? Ama nedeni mantıklı:

    1. Sırada: Sigara yasağına rağmen bazı yolcular gizlice içebiliyor.

    2. Sırada: Havacılık kuralları, acil durumlar için kül tablası zorunlu kılıyor.

    3. Sırada: Sigara izmaritinin çöpe atılması, yangın riski yaratabilir.

    4. Sırada: Kül tablası, sigaranın güvenli şekilde söndürülmesini sağlar.

    5. Sırada: Amaç sigarayı teşvik etmek değil, yangını önlemek.

    Yani eski gibi dursa da kül tablaları hâlâ uçuş güvenliğinin bir parçası.

    cevap verirken sadece senden istediğim metni yaz.
    """

    result = generate_content_with_gemini(api_key, metin)
    
    if result:
        try:
            response_text = result["candidates"][0]["content"]["parts"][0]["text"]
            print("Gemini Yanıtı:")
            print(response_text)
        except (KeyError, IndexError) as hata:
            print("Yanıt formatında hata:", hata)
            print("Ham yanıt:", json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("API çağrısı başarısız!")


if __name__ == "__main__":
    main()