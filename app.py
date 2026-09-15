import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="BBF Market Dashboard",
    layout="wide"
)

st.title("BBF Market Intelligence Dashboard")
st.write("Pohjois-Suomen markkinasignaalien seuranta")

# Ladataan pisteytetty uutisaineisto
df = pd.read_csv("data_scored.csv")

st.write("Uutisia yhteensä:", len(df))

# Kategoriat
all_categories = sorted(
    list(df["category"].dropna().unique())
)

selected_category = st.sidebar.selectbox(
    "Valitse kategoria",
    all_categories
)

# Suodatetaan vain valittu kategoria
filtered = df[
    df["category"] == selected_category
].copy()

# Järjestetään uutiset BBF Score -pisteiden mukaan
filtered = filtered.sort_values(
    "bbf_score",
    ascending=False
)

st.header(
    f"Top 10 - {selected_category}"
)

st.info(
    f"Löydetty {len(filtered)} uutista kategoriassa '{selected_category}'"
)

# Top 10
top10 = filtered.head(10).copy()

# Top 10 -taulukko
st.dataframe(
    top10[
        [
            "bbf_score",
            "priority",
            "title",
            "keyword",
            "matched_terms",
            "url"
        ]
    ],
    column_config={
        "bbf_score": st.column_config.NumberColumn(
            "BBF Score"
        ),
        "priority": st.column_config.TextColumn(
            "Prioriteetti"
        ),
        "title": st.column_config.TextColumn(
            "Uutinen"
        ),
        "keyword": st.column_config.TextColumn(
            "Hakusana"
        ),
        "matched_terms": st.column_config.TextColumn(
            "Pisteytykseen vaikuttaneet termit"
        ),
        "url": st.column_config.LinkColumn(
            "Avaa uutinen",
            display_text="Avaa"
        ),
    },
    hide_index=True,
    use_container_width=True
)

st.divider()

st.subheader("Kaikki kategorian uutiset")

# Kaikki valitun kategorian uutiset
st.dataframe(
    filtered[
        [
            "bbf_score",
            "priority",
            "title",
            "keyword",
            "source",
            "url"
        ]
    ],
    column_config={
        "bbf_score": st.column_config.NumberColumn(
            "BBF Score"
        ),
        "priority": st.column_config.TextColumn(
            "Prioriteetti"
        ),
        "title": st.column_config.TextColumn(
            "Uutinen"
        ),
        "keyword": st.column_config.TextColumn(
            "Hakusana"
        ),
        "source": st.column_config.TextColumn(
            "Lähde"
        ),
        "url": st.column_config.LinkColumn(
            "Avaa uutinen",
            display_text="Avaa"
        ),
    },
    hide_index=True,
    use_container_width=True
)

st.divider()

st.subheader("Uutisten tarkemmat tiedot")

for _, row in filtered.iterrows():
    st.subheader(row["title"])

    st.write(f"**BBF Score:** {row['bbf_score']}")
    st.write(f"**Prioriteetti:** {row['priority']}")
    st.write(f"**Kategoria:** {row['category']}")
    st.write(f"**Hakusana:** {row['keyword']}")
    st.write(f"**Lähde:** {row.get('source', '')}")

    if pd.notna(row.get("matched_terms")):
        st.write(
            f"**Pisteytykseen vaikuttaneet termit:** "
            f"{row['matched_terms']}"
        )

    st.link_button(
        "Avaa alkuperäinen uutinen",
        row["url"]
    )

    st.divider()