
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

# Ladataan AI-analyysit ja yhdistetään ne uutisiin
try:
    ai_df = pd.read_csv("data_ai_analyzed.csv")

    ai_columns = [
        "url",
        "summary",
        "relevance_reason",
        "relevant",
        "north_finland",
        "ai_category",
        "detected_region"
    ]

    ai_df = ai_df[ai_columns].drop_duplicates(subset=["url"])

    df = df.merge(
        ai_df,
        on="url",
        how="left"
    )

except (FileNotFoundError, KeyError):
    st.warning(
        "AI-analyysitiedostoa ei löytynyt tai sen rakenne on muuttunut."
    )

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

    # Näytetään AI-analyysi, jos sellainen löytyy
    summary = row.get("summary")

    if pd.notna(summary) and str(summary).strip():

        st.markdown("### AI-yhteenveto")
        st.write(summary)

        reason = row.get("relevance_reason")

        if pd.notna(reason):
            st.write(
                f"**Miksi uutinen on merkittävä:** {reason}"
            )

        ai_category = row.get("ai_category")

        if pd.notna(ai_category):
            st.write(
                f"**AI:n ehdottama kategoria:** {ai_category}"
            )

        detected_region = row.get("detected_region")

        if pd.notna(detected_region):
            st.write(
                f"**Tunnistettu alue:** {detected_region}"
            )

        # AI:n relevanssiarvio
        relevant = row.get("relevant")
        north_finland = row.get("north_finland")

        if pd.notna(relevant) and pd.notna(north_finland):

            is_relevant = str(relevant).strip().lower() == "true"
            is_north = str(north_finland).strip().lower() == "true"

            if not is_north:
                st.error(
                    "Ei liity Pohjois-Suomeen"
                )

            elif not is_relevant:
                st.error(
                    "Ei liiketoiminnallisesti relevantti"
                )

            else:
                st.success(
                    "Relevantti Pohjois-Suomen markkinasignaali"
                )

    st.link_button(
        "Avaa alkuperäinen uutinen",
        row["url"]
    )

    st.divider()
