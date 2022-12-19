import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from deta import Deta
import pandas as pd
import altair as alt

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])

# Create a new database
db = deta.Base("project_fietsklinik")
# -------------- FUNCTIONS --------------

def insert_period(date, time_shift, name, e_mail, buurt, werkzaamheedeb, materiaal, opmerking):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"date": date, "time_shift": time_shift, "name": name, "e_mail": e_mail, "buurt": buurt, 
                   "werkzaamheedeb": werkzaamheedeb, "materiaal":materiaal, "opmerking":opmerking})


# -------------- SETTINGS --------------
page_title = ":bike: Fietsklinik"
page_icon = ":bike:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
time_shift_choice = ["14-16", "16-18", "18-20"]
buurt_choice = ["Centrum", "Oost", "West"]
materiaal_choice = ["ruote", "parafango"]

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_icon)


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title="Fietskliniek",
    options=["Make an appointment", "Cancel an appointment"],
    icons=["bi-journal-check", "bi-x-octagon-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS ---
if selected == "Make an appointment":
    with st.form("entry_form", clear_on_submit=True):

        date = st.date_input("Date")        
        time_shift = st.selectbox("Time shift", time_shift_choice )
        name = st.text_input("", placeholder="Enter your name here ...")
        e_mail = st.text_input("", placeholder="Enter your e-mail here ...")
        buurt = st.selectbox("Buurt", buurt_choice)
        werkzaamheedeb = st.text_input("", placeholder="Enter your werkzaamheedeb here ...")
        materiaal = st.selectbox("Matiriaal", materiaal_choice)
        opmerking = st.text_input("Opmerking", placeholder="Opmerking ...")
               
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            insert_period(date, time_shift, name, e_mail, buurt, werkzaamheedeb, materiaal, opmerking)
            st.success("You booked an appointment!")
            
