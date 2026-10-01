#--------------------GOOGLE SHEET---------------------
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit as st

# Load data
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0, worksheet="Data")

# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Sort by date + time
df = df.sort_values(["Date", "Time shift"])

# Dutch day names
DUTCH_DAYS = {
    "Monday": "Maandag",
    "Tuesday": "Dinsdag",
    "Wednesday": "Woensdag",
    "Thursday": "Donderdag",
    "Friday": "Vrijdag",
    "Saturday": "Zaterdag",
    "Sunday": "Zondag"
}

st.title("📅 Agenda Fietskliniek")

st.markdown("### Overzicht van alle afspraken")

# Date selector
unique_dates = df["Date"].dropna().dt.date.unique()
selected_date = st.selectbox("Kies een datum", unique_dates)

# Filter by selected date
df_day = df[df["Date"].dt.date == selected_date]

if df_day.empty:
    st.info("Geen afspraken op deze dag.")
    st.stop()

# Determine Dutch day name
day_en = selected_date.strftime("%A")
day_nl = DUTCH_DAYS.get(day_en, day_en)

st.markdown(f"## {day_nl} — {selected_date.strftime('%d-%m-%Y')}")

# Group by time shift
for time_shift, group in df_day.groupby("Time shift"):
    st.markdown(f"### 🕒 {time_shift}")

    for _, row in group.iterrows():
        with st.container():
            st.markdown(
                f"""
                **Naam:** {row['Name']}  
                **E-mail:** {row['e_mail']}  
                **Telefoon:** {row['Phone number']}  
                **Membership:** {row['Membership']}  
                **Stadspasnummer:** {row['Membership_number']}  
                **Buurt:** {row['Neighborhood']}  
                **Ervaring:** {row['Expertise']}  
                **Type fiets:** {row['Type of bike']}  
                **Reparatie(s):** {row['Type of reparation']}  
                **Opmerking:** {row['Remarks']}  
                """
            )
            st.markdown("---")




  
