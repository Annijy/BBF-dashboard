import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_news_batch(df):
    news_items = ""

    for i, row in df.iterrows():
        news_items += f"""
ID: {i}
Otsikko: {row["title"]}
Alkuperäinen hakukategoria: {row["category"]}
Alue hakuvaiheessa: {row["region"]}
Hakusana: {row["keyword"]}
URL: {row["url"]}
"""

    prompt = f"""
Analysoi seuraavat uutiset Bonnier Business Forumin näkökulmasta.

Bonnier Business Forum on kiinnostunut erityisesti:
- kiinteistöalasta
- rakentamisesta
- kaupunkikehityksestä
- investoinneista
- datakeskuksista
- logistiikasta
- matkailuhankkeista
- yritysten avainhenkilönimityksistä

Luokittele jokainen uutinen yhteen seuraavista kategorioista:
1. Nimitykset & organisaatiomuutokset
2. Investoinnit & transaktiot
3. Kaupunkikehitys & kiinteistökehitys
4. Rakennus- & toimitilahankkeet
5. Retail & kaupalliset kiinteistöt
6. Hotellit & hospitality
7. Logistiikka, infra & datakeskukset
8. Hoiva- & yhteiskuntakiinteistöt
9. Ei relevantti

Tunnista myös alue:
- Oulu
- Pohjois-Pohjanmaa
- Kainuu
- Keski-Pohjanmaa
- Lappi
- Muu Suomi

Anna confidence-arvio välillä 0-100.

Käytä "Ei relevantti" vain, jos uutinen ei liity millään tavalla liiketoimintaan, aluekehitykseen, investointeihin, rakentamiseen, infraan, kiinteistöihin, matkailuun tai organisaatiomuutoksiin.

Palauta vastaus AINOASTAAN validina JSON-listana.
Jokaisessa listan objektissa tulee olla täsmälleen nämä kentät:

[
  {{
    "id": 0,
    "confidence": 0,
    "region_detected": "",
    "ai_category": "",
    "summary": "",
    "relevance": "",
    "priority": "",
    "suggested_action": ""
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

        print("\n=== GEMINI VASTAUS ===")
        print(text)

        return json.loads(text)

    except Exception as error:
        print("\n=== VIRHE ===")
        print(error)
        return []


df = pd.read_csv("data.csv")

# Testissä analysoidaan vain 5 uutista yhdellä Gemini-kutsulla
df = df.head(5)

results = analyze_news_batch(df)

results_df = pd.DataFrame(results)

if results_df.empty:
    print("Gemini ei palauttanut analyysituloksia.")
    df["confidence"] = 0
    df["region_detected"] = "Ei tunnistettu"
    df["ai_category"] = "Ei relevantti"
    df["summary"] = ""
    df["relevance"] = ""
    df["priority"] = "Ei analysoitu"
    df["suggested_action"] = ""
else:
    results_df = results_df.rename(columns={"id": "index"})
    df = df.reset_index().merge(results_df, on="index", how="left")

    df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0).astype(int)
    df["region_detected"] = df["region_detected"].fillna("Ei tunnistettu")
    df["ai_category"] = df["ai_category"].fillna("Ei relevantti")
    df["summary"] = df["summary"].fillna("")
    df["relevance"] = df["relevance"].fillna("")
    df["priority"] = df["priority"].fillna("")
    df["suggested_action"] = df["suggested_action"].fillna("")

print("\n=== AI-KATEGORIAT ===")
print(df["ai_category"].value_counts())

print("\n=== CONFIDENCE ===")
print(df["confidence"].describe())

# Näytetään vain relevantit ja riittävän varmat löydökset
df = df[(df["confidence"] > 70) & (df["ai_category"] != "Ei relevantti")]

df.to_csv("data_analyzed.csv", index=False, encoding="utf-8-sig")

print("Gemini-eräanalyysi valmis. Tallennettu tiedostoon data_analyzed.csv")