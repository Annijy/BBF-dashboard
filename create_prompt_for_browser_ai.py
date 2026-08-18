import pandas as pd

df = pd.read_csv("data.csv")
df = df.head(10)

prompt = """
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

Palauta vastauksesi taulukkona sarakkeilla:
id | ai_category | region_detected | confidence | summary | relevance | priority | suggested_action

Uutiset:
"""

for index, row in df.iterrows():
    prompt += f"""
ID: {index}
Otsikko: {row["title"]}
Hakukategoria: {row["category"]}
Alue hakuvaiheessa: {row["region"]}
Hakusana: {row["keyword"]}
URL: {row["url"]}
"""

with open("browser_ai_prompt.txt", "w", encoding="utf-8") as file:
    file.write(prompt)

print("Valmis. Kopioi tiedoston browser_ai_prompt.txt sisältö Gemman/Geminin selainversioon.")