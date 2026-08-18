import streamlit as st
import pandas as pd

st.set_page_config(page_title="BBF Market Dashboard", layout="wide")

st.title("BBF Market Intelligence Dashboard")
st.write("Pohjois-Suomen markkinasignaalien seuranta")

df = pd.read_csv("data_scored.csv")

st.write("Uutisia yhteensä:", len(df))

all_categories = sorted(
    list(df["category"].dropna().unique())
)

selected_category = st.sidebar.selectbox(
    "Valitse kategoria",
    all_categories
)

all_regions = sorted(
    list(df["region"].dropna().unique())
)

all_regions.insert(0, "Kaikki alueet")

selected_region = st.sidebar.selectbox(
    "Valitse alue",
    all_regions
)

filtered = df[
    df["category"] == selected_category
]

if selected_region != "Kaikki alueet":
    filtered = filtered[
        filtered["region"] == selected_region
    ]

filtered = filtered.sort_values(
    "bbf_score",
    ascending=False
)

if selected_region == "Kaikki alueet":
    st.header(
        f"Top 10 - {selected_category}"
    )
else:
    st.header(
        f"Top 10 - {selected_category} ({selected_region})"
    )

if selected_region == "Kaikki alueet":
    st.info(
        f"Löydetty {len(filtered)} uutista kategoriassa '{selected_category}'"
    )
else:
    st.info(
        f"Löydetty {len(filtered)} uutista kategoriassa '{selected_category}' alueella '{selected_region}'"
    )
    
top10 = filtered.head(10)

st.dataframe(
    top10[["bbf_score", "priority", "title", "keyword", "matched_terms"]],
    use_container_width=True
)

st.info(
    f"Löydetty {len(filtered)} uutista kategoriassa '{selected_category}'"
)

st.divider()

st.dataframe(filtered, use_container_width=True)

for _, row in filtered.iterrows():
    st.subheader(row["title"])
    st.write(f"**BBF Score:** {row['bbf_score']}")
    st.write(f"**Prioriteetti:** {row['priority']}")
    st.write(f"**Kategoria:** {row['category']}")
    st.write(f"**Alue:** {row['region']}")
    st.write(f"**Hakusana:** {row['keyword']}")
    st.write(f"**Lähde:** {row.get('source', '')}")
    st.write(f"[Avaa lähde]({row['url']})")
    st.divider()