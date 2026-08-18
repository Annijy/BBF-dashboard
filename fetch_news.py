import feedparser
import pandas as pd
from datetime import datetime
from urllib.parse import quote

regions = [
    "Oulu",
    "Lappi",
    "Pohjois-Suomi",
    "Pohjois-Pohjanmaa",
    "Keski-Pohjanmaa",
    "Kainuu",
    "Rovaniemi",
    "Kemi",
    "Tornio",
    "Kuusamo",
    "Kajaani",
    "Kokkola"
]

categories = {
    "Nimitykset & organisaatiomuutokset": [
        "nimitetty toimitusjohtajaksi",
        "nimitetty johtajaksi",
        "aloittaa toimitusjohtajana",
        "aloittaa johtajana",
        "uusi aluejohtaja",
        "uusi liiketoimintajohtaja",
        "uusi kiinteistöjohtaja",
        "vahvistaa johtoryhmää",
        "rekrytoi johtajan",
        "asset manager",
        "country manager"
    ],

    "Investoinnit & transaktiot": [
        "investoi",
        "investointi",
        "kiinteistösijoittaja",
        "kiinteistökauppa",
        "kiinteistökaupan aiesopimus",
        "tonttikauppa",
        "yrityskauppa",
        "rahasto osti",
        "portfolio",
        "joint venture",
        "sijoitus"
    ],

    "Kaupunkikehitys & kiinteistökehitys": [
        "asemakaava",
        "kaavamuutos",
        "kaavoitus",
        "suunnitteluvaraus",
        "tonttikilpailu",
        "aluekehitys",
        "kiinteistökehitys",
        "kiinteistökehittäjä",
        "kehityshanke",
        "masterplan"
    ],

    "Rakennus- & toimitilahankkeet": [
        "rakennushanke",
        "toimitilahanke",
        "rakentaa",
        "rakennuttaa",
        "uudiskohde",
        "toimitilaprojekti",
        "kampus",
        "business park",
        "monitoimihanke"
    ],

    "Retail & kaupalliset kiinteistöt": [
        "kauppakeskus",
        "liikekiinteistö",
        "liikekeskus",
        "retail park",
        "retail",
        "big box",
        "hypermarket",
        "päivittäistavarakauppa",
        "kaupallinen kiinteistö"
    ],

    "Hotellit & hospitality": [
        "hotelli",
        "matkailuhanke",
        "resort",
        "matkailukeskus",
        "majoitushanke",
        "hospitality"
    ],

    "Logistiikka, infra & datakeskukset": [
        "logistiikkakeskus",
        "datakeskus",
        "varasto",
        "terminaali",
        "teollisuuskiinteistö",
        "hyperscale",
        "energiainvestointi",
        "akkutehdas",
        "vihreä siirtymä",
        "infrahanke",
        "ratahanke"
    ],

    "Hoiva- & yhteiskuntakiinteistöt": [
        "hoivakiinteistö",
        "yhteiskuntakiinteistö",
        "hyvinvointikeskus",
        "terveyskeskus",
        "palvelukoti",
        "sairaala",
        "kouluhanke",
        "päiväkoti"
    ]
}

rows = []
count = 0

for category, keywords in categories.items():
    for keyword in keywords:

        count += 1
        print(f"Haku #{count}: {category} | {keyword}")

        query = quote(f"{keyword} when:7d")
        url = f"https://news.google.com/rss/search?q={query}&hl=fi&gl=FI&ceid=FI:fi"

        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            rows.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "category": category,
                "region": "Tunnistetaan myöhemmin",
                "keyword": keyword,
                "title": entry.title,
                "source": getattr(entry, "source", {}).get("title", ""),
                "url": entry.link
            })

df = pd.DataFrame(rows).drop_duplicates(subset=["title"])
df.to_csv("data.csv", index=False, encoding="utf-8-sig")

print(f"Tallennettu {len(df)} uutista tiedostoon data.csv")