import random

import pandas as pd
import streamlit as st
from sqlalchemy import text

# Replace only url in quotes
google_sheets_url = "https://docs.google.com/spreadsheets/d/1kws524HbFLr2Q_0_YeNgZ5FubDbUEVLzDNJz5HFK1Gw/edit?usp=sharing"

conn = st.connection("postgresql", type="sql")
google_sheets_gifters = google_sheets_url.replace(
    "/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=gifters"
)
google_sheets_results = google_sheets_url.replace(
    "/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=results"
)

try:
    pd.read_csv(google_sheets_gifters).to_sql("gifters", conn.engine, index=False)
    pd.read_csv(google_sheets_gifters).to_sql("resiviers", conn.engine, index=False)
    pd.read_csv(google_sheets_results).to_sql("results", conn.engine, index=False)
except ValueError:
    pass

gifters = pd.read_sql_table("gifters", conn.engine)
resiviers = pd.read_sql_table("resiviers", conn.engine)
conn.engine.dispose()

st.title("Magic Hat 🎩")

name = st.selectbox(
    "Please select your name...",
    gifters["name"].sort_values(),
    index=None,
    placeholder="Please select your name...",
    label_visibility="collapsed",
)

if name is not None:
    st.text(f"Hi {name} 👋 ")
    st.text("Press the button to know who you are gifting to:")
    if st.button("Hocus Pocus 🪄", type="primary"):
        choice = random.choice(resiviers["name"])
        while (name == choice) or (
            gifters[gifters["name"] == name]["familyID"]
            .isin(resiviers[resiviers["name"] == choice]["familyID"])
            .iloc[0]
        ):
            choice = random.choice(resiviers["name"])

        with conn.session as s:
            s.execute(text("DELETE FROM gifters WHERE name = :name"), {"name": name})
            s.execute(
                text("DELETE FROM resiviers WHERE name = :choice"), {"choice": choice}
            )
            s.execute(
                text("INSERT INTO results VALUES (:result)"),
                {"result": f"{name} is gifting to {choice}"},
            )
            s.commit()
            st.header(f"{name} is gifting to {choice}")

        st.balloons()
