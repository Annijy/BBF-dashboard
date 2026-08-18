import pandas as pd

df = pd.read_csv("data.csv")

score_terms = {
    # Nimitykset
    "toimitusjohtaja": 15,
    "aluejohtaja": 12,
    "liiketoimintajohtaja": 12,
    "kiinteistöjohtaja": 12,
    "hankekehitysjohtaja": 12,
    "projektijohtaja": 10,
    "rakennuttajapäällikkö": 10,
    "nimitetty": 10,
    "nimitys": 8,
    "johtaja": 6,

    # Investoinnit
    "investointi": 15,
    "investoi": 12,
    "kiinteistökauppa": 15,
    "tonttikauppa": 12,
    "yrityskauppa": 12,
    "rahasto": 10,
    "joint venture": 10,
    "sijoitus": 8,

    # Kaupunkikehitys
    "asemakaava": 12,
    "kaavamuutos": 12,
    "kaavoitus": 10,
    "suunnitteluvaraus": 12,
    "tonttikilpailu": 12,
    "aluekehitys": 10,
    "kiinteistökehitys": 12,
    "kehityshanke": 10,

    # Rakennus- ja toimitilahankkeet
    "rakennushanke": 15,
    "toimitilahanke": 15,
    "rakentaa": 10,
    "rakennuttaa": 10,
    "uudiskohde": 10,
    "kampus": 8,
    "business park": 10,

    # Retail
    "kauppakeskus": 12,
    "liikekiinteistö": 12,
    "liikekeskus": 10,
    "retail park": 12,
    "hypermarket": 10,
    "päivittäistavarakauppa": 8,

    # Hotellit ja matkailu
    "hotelli": 10,
    "matkailuhanke": 15,
    "resort": 12,
    "matkailukeskus": 12,
    "majoitushanke": 12,

    # Logistiikka, infra ja datakeskukset
    "logistiikkakeskus": 15,
    "datakeskus": 20,
    "terminaali": 10,
    "teollisuuskiinteistö": 12,
    "hyperscale": 20,
    "energiainvestointi": 15,
    "akkutehdas": 20,
    "vihreä siirtymä": 12,
    "infrahanke": 12,
    "ratahanke": 12,

    # Hoiva ja yhteiskuntakiinteistöt
    "hoivakiinteistö": 12,
    "yhteiskuntakiinteistö": 12,
    "hyvinvointikeskus": 12,
    "terveyskeskus": 12,
    "palvelukoti": 10,
    "sairaala": 12,
    "kouluhanke": 10,
    "päiväkoti": 8,
}

north_finland_terms = [
    "oulu", "oulun",
    "lappi", "lapin",
    "rovaniemi", "rovaniemen",
    "kemi", "tornio", "kuusamo",
    "kainuu", "kainuun",
    "kajaani", "kajaanin",
    "kokkola", "kokkolan",
    "pohjois-suomi", "pohjois-suomen",
    "pohjois-pohjanmaa", "pohjois-pohjanmaan",
    "keski-pohjanmaa", "keski-pohjanmaan"
]

region_terms = {
    "oulu": 10,
    "lappi": 10,
    "pohjois-suomi": 10,
    "pohjois-pohjanmaa": 10,
    "keski-pohjanmaa": 10,
    "kainuu": 10,
    "rovaniemi": 10,
    "kemi": 8,
    "tornio": 8,
    "kuusamo": 8,
    "kajaani": 8,
    "kokkola": 8,
}

blacklist_terms = [
    "urheilu",
    "jääkiekko",
    "salibandy",
    "ralli",
    "viihde",
    "sää",
    "lennot",
    "lentoreitti",
]


scores = []
matched_terms_all = []
detected_regions = []
north_finland_flags = []

for _, row in df.iterrows():
    title = str(row["title"]).lower()

    region_text = (
        str(row.get("title", "")) + " " +
        str(row.get("keyword", "")) + " " +
        str(row.get("url", ""))
    ).lower()

    is_north_finland = any(term in region_text for term in north_finland_terms)

    score = 0
    matched_terms = []

    region_found = "Ei tunnistettu"

    for region_term in region_terms.keys():
        if region_term in title:
            region_found = region_term.title()
            break

    for term, points in score_terms.items():
        if term in title:
            score += points
            matched_terms.append(term)

    for term, points in region_terms.items():
        if term in title:
            score += points
            matched_terms.append(term)

    for term in blacklist_terms:
        if term in title:
            score -= 15
            matched_terms.append(f"miinus: {term}")

    if score < 0:
        score = 0

    if is_north_finland:
        score += 15
        matched_terms.append("Pohjois-Suomi")

    north_finland_flags.append(is_north_finland)
    scores.append(score)
    matched_terms_all.append(", ".join(matched_terms))
    detected_regions.append(region_found)

priorities = []

for score in scores:
    if score >= 30:
        priorities.append("Korkea")
    elif score >= 15:
        priorities.append("Keskitaso")
    else:
        priorities.append("Matala")

df["bbf_score"] = scores
df["priority"] = priorities
df["matched_terms"] = matched_terms_all
df["detected_region"] = detected_regions

df = df.sort_values("bbf_score", ascending=False)

#df["is_north_finland"] = north_finland_flags

#df = df[df["is_north_finland"] == True]

df.to_csv("data_scored.csv", index=False, encoding="utf-8-sig")

print("BBF Score valmis.")
print(f"Pisteytetty {len(df)} uutista.")