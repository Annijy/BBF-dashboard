import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

df = pd.read_csv("data_scored.csv")

# Otetaan vain 10 korkeimmin pisteytettyä uutista
top_news = df.sort_values("bbf_score", ascending=False).head(10)

news_items = ""

for i, row in top_news.reset_index(drop=True).iterrows():
    news_items += f"""
ID: {i}
Otsikko: {row["title"]}
Kategoria: {row["category"]}
BBF Score: {row["bbf_score"]}
Prioriteetti: {row["priority"]}
Hakusana: {row["keyword"]}
Lähde: {row["source"]}
URL: {row["url"]}
"""

prompt = f"""
Analysoi seuraavat uutiset Bonnier Business Forumin näkökulmasta.

Tarkoitus on tunnistaa Pohjois-Suomen liiketoiminnan kannalta relevantit markkinasignaalit.

Arvioi jokaisesta uutisesta:

1. Onko uutinen relevantti Bonnier Business Forumille?
2. Liittyykö uutinen Pohjois-Suomeen?
3. Mikä seuraavista kategorioista sopii parhaiten?
   - Nimitykset & organisaatiomuutokset
   - Investoinnit & transaktiot
   - Kaupunkikehitys & kiinteistökehitys
   - Rakennus- & toimitilahankkeet
   - Retail & kaupalliset kiinteistöt
   - Hotellit & hospitality
   - Logistiikka, infra & datakeskukset
   - Hoiva- & yhteiskuntakiinteistöt
   - Ei relevantti

4. Tee korkeintaan kahden virkkeen tiivistelmä.
5. Kerro lyhyesti, miksi uutinen on tai ei ole relevantti.
6. Anna confidence-arvio välillä 0-100.

Palauta vastaus AINOASTAAN validina JSON-listana tässä muodossa:

[
  {{
    "id": 0,
    "relevant": true,
    "north_finland": true,
    "ai_category": "",
    "summary": "",
    "relevance_reason": "",
    "confidence": 0
  }}
]

Uutiset:
{news_items}
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    results = json.loads(text)

    results_df = pd.DataFrame(results)

    top_news = top_news.reset_index(drop=True)
    top_news = top_news.reset_index().rename(columns={"index": "id"})

    merged = top_news.merge(results_df, on="id", how="left")

    merged.to_csv(
        "data_ai_analyzed.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Gemini-analyysi valmis.")
    print("Tallennettu tiedostoon data_ai_analyzed.csv")

except Exception as error:
    print("Gemini-analyysi epäonnistui.")
    print(error)