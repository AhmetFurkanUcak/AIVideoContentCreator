import requests
import yaml
import colorama
import os
import json
import time
from openai import OpenAI

with open("../../config.yml", "r", encoding="utf-8") as configuration:
    config = yaml.safe_load(configuration)

api_key = config["OPENAI_API_KEY"]

def generate_content_with_openai(api_key, prompt):
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Sen bir Video Metin Oluşturucu Asistanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            max_tokens=1000
        )
        
        return response
    except Exception as hata:
        print(f"API çağrısında hata: {hata}")
        return None


def main():
    """
    Örnek kullanım
    """
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

    cevap verirken sadece metni yaz uzun uzun cevap yazma.
    """


    result = generate_content_with_openai(api_key, prompt)
    
    if result:
        try:
            response_text = result.choices[0].message.content
            print("OpenAI Yanıtı:")
            print(response_text)
        except (AttributeError, IndexError) as hata:
            print("Yanıt formatında hata:", hata)
            print("Ham yanıt:", result)
    else:
        print("API çağrısı başarısız!")


if __name__ == "__main__":
    main()
