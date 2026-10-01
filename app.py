#--------------------GOOGLE SHEET---------------------
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit as st

#---LOAD DATASETS---
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0, worksheet="Data")

# 🔥 FIX: Convert Date column to datetime BEFORE using .dt
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# --- PASSWORD GATE ---
def password_gate():
    pw = st.text_input("Voer het wachtwoord in om verder te gaan:", type="password")
    if pw != "fietskliniek":
        st.stop()

password_gate()




st.markdown("### Overzicht van alle afspraken")

st.markdown(
    """
    📄 **Agenda gegevens worden geladen uit Google Sheets.**  
    👉 U kunt de data ook hier bekijken:  
    **https://docs.google.com/spreadsheets/d/1mkF1s_hsoX7GfCdbb_RtaxssqYfLO-kpsJncbqc5Wpw/edit?gid=2007222776#gid=2007222776**

    ⚠️ *Verplaats geen kolommen in het Google Sheet — dit kan de app laten crashen.*
    """
)


# Date selector
view_mode = st.radio(
    "Kies een periode:",
    ["Verleden", "Vandaag", "Toekomst"],
    horizontal=True,
    index=1
)

today = pd.Timestamp.today().date()

if view_mode == "Verleden":
    selectable_dates = df[df["Date"].dt.date < today]["Date"].dt.date.unique()

elif view_mode == "Vandaag":
    selectable_dates = df[df["Date"].dt.date == today]["Date"].dt.date.unique()

else:  # Toekomst
    selectable_dates = df[df["Date"].dt.date > today]["Date"].dt.date.unique()

if len(selectable_dates) == 0:
    st.info("Geen afspraken in deze periode.")
    st.stop()

selected_date = st.selectbox("Kies een datum", selectable_dates)


# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Filter by selected date
df_day = df[df["Date"].dt.date == selected_date]

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

day_en = selected_date.strftime("%A")
day_nl = DUTCH_DAYS.get(day_en, day_en)

st.markdown(f"## 📅 {day_nl} — {selected_date.strftime('%d-%m-%Y')}")

if df_day.empty:
    st.info("Geen afspraken op deze dag.")
    st.stop()

# Group by time shift
for time_shift, group in df_day.groupby("Time shift"):
    st.markdown(f"### 🕒 {time_shift}")

    for idx, row in group.iterrows():
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
    
            delete_label = f"❌ Afspraak verwijderen ({row['Name']})"
            if st.button(delete_label, key=f"delete_{idx}"):
    
                # Read fresh data from Google Sheet
                df_full = conn.read(ttl=0, worksheet="Data")
    
                # Date in sheet is string like '2026-10-12'
                # row['Date'] in agenda is Timestamp → convert
                if isinstance(row["Date"], pd.Timestamp):
                    date_str = row["Date"].strftime("%Y-%m-%d")
                else:
                    date_str = str(row["Date"])
    
                time_shift = row["Time shift"]
                e_mail = row["e_mail"]
    
                # Find matching rows exactly like your cancel logic
                df_filter = df_full[
                    (df_full["Date"] == date_str) &
                    (df_full["Time shift"] == time_shift) &
                    (df_full["e_mail"] == e_mail)
                ]
    
                if len(df_filter) > 0:
                    df_drop = df_full[~df_full.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
                    conn.update(worksheet="Data", data=df_drop)
                    st.success(f"De afspraak van **{row['Name']}** is verwijderd.")
                    st.rerun()
                else:
                    st.warning("Kon de afspraak niet vinden in het systeem.", icon="⚠️")
    
            st.markdown("---")



    # for idx, row in group.iterrows():
    #     with st.container():
    #         st.markdown(
    #             f"""
    #             **Naam:** {row['Name']}  
    #             **E-mail:** {row['e_mail']}  
    #             **Telefoon:** {row['Phone number']}  
    #             **Membership:** {row['Membership']}  
    #             **Stadspasnummer:** {row['Membership_number']}  
    #             **Buurt:** {row['Neighborhood']}  
    #             **Ervaring:** {row['Expertise']}  
    #             **Type fiets:** {row['Type of bike']}  
    #             **Reparatie(s):** {row['Type of reparation']}  
    #             **Opmerking:** {row['Remarks']}  
    #             """
    #         )
    
            # Delete button
            # delete_label = f"❌ Afspraak verwijderen ({row['Name']})"
            # if st.button(delete_label, key=f"delete_{idx}"):
    
            #     # Load fresh data
            #     df_current = conn.read(ttl=0, worksheet="Data")
    
            #     # Identify the exact row to drop
            #     row_tuple = tuple(row)
            #     df_drop = df_current[~df_current.apply(tuple, axis=1).isin([row_tuple])]
    
            #     # Update sheet
            #     conn.update(worksheet="Data", data=df_drop)
    
            #     # Confirmation dialog
            #     st.success(f"De afspraak van **{row['Name']}** is verwijderd.")
    
            #     st.rerun()

        # delete_label = f"❌ Afspraak verwijderen ({row['Name']})"
        # if st.button(delete_label, key=f"delete_{idx}"):
        
        #     df_current = conn.read(ttl=0, worksheet="Data")
        
        #     # Convert all to string for safe comparison
        #     df_current["Date"] = df_current["Date"].astype(str)
        #     df_current["Time shift"] = df_current["Time shift"].astype(str)
        #     df_current["e_mail"] = df_current["e_mail"].astype(str)
        
        #     row_date = str(row["Date"])
        #     row_shift = str(row["Time shift"])
        #     row_email = str(row["e_mail"])
        
        #     # Identify row by unique fields
        #     mask = (
        #         (df_current["Date"] == row_date) &
        #         (df_current["Time shift"] == row_shift) &
        #         (df_current["e_mail"] == row_email)
        #     )

        #     st.write(mask)
        #     st.write(mask.sum())
        #     if mask.sum() == 0:
        #         st.error("Kon de afspraak niet vinden in het systeem.")
        #         st.stop()
        
        #     # Drop the row
        #     df_drop = df_current[~mask]
        
        #     # Update sheet
        #     conn.update(worksheet="Data", data=df_drop)
        
        #     st.success(f"De afspraak van **{row['Name']}** is verwijderd.")
        #     st.rerun()


    
        #     st.markdown("---")






  
