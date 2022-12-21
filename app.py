import calendar  
from datetime import datetime 
import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
from dateutil import parser

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])

# Create a new database
db = deta.Base("project_fietskliniek")

# -------------- FUNCTIONS --------------
def insert_period(date, time_shift, name, e_mail, buurt, werkzaamheedeb, materiaal, opmerking):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.insert({"date": date, "time_shift": time_shift, 
                   "name": name, "e_mail": e_mail, 
                   "buurt": buurt, "werkzaamheedeb": werkzaamheedeb, 
                   "materiaal":materiaal, "opmerking":opmerking
                  })


# -------------- SETTINGS --------------
page_title = None
page_icon = " :bike: "  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
time_shift_choice = ["14-16", "16-18", "18-20"]
buurt_choice = ["Centrum", "Oost", "West"]
materiaal_choice = ["ruote", "parafango"]

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
# st.title(page_icon)


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
    menu_title=None,
    options=["Make an appointment", "Cancel an appointment"],
    icons=["bi-journal-check", "bi-x-octagon-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS ---
if selected == "Make an appointment":
    with st.form("entry_form", clear_on_submit=True):

        date = str(st.date_input("Date"))
        time_shift = st.selectbox("Time shift", time_shift_choice )
        name = st.text_input("", placeholder="Enter your name here ...")
        e_mail = st.text_input("", placeholder="Enter your e-mail here ...")
        buurt = st.selectbox("Buurt", buurt_choice)
        werkzaamheedeb = st.text_input("", placeholder="Enter your werkzaamheedeb here ...")
        materiaal = st.selectbox("Matiriaal", materiaal_choice)
        opmerking = st.text_input("Opmerking", placeholder="Opmerking ...")
               
        "---"
        
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
       
        df_filter = df[(df.date==date) & (df.time_shift==time_shift)]
        pr = df_filter.profile_report()
        st_profile_report(pr)
        len = len(df_filter)
        st.dataframe(df_filter, use_container_width=True)
        st.metric(label="Number of shifts", value=len)
            
        submitted = st.form_submit_button("Save Data")

        if submitted:
            
            day = parser.parse(date).strftime("%A")
            if day == "Thursday" or day == "Tuesday":
                
                if time_shift=="14-16" and a > 1:
                    st.warning('please choice another time-shift', icon="⚠️")

                elif time_shift=="16-18" and a > 2:
                    st.warning('please choice another time-shift', icon="⚠️")

                elif time_shift=="18-20" and a > 3:
                    st.warning('please choice another time-shift', icon="⚠️")
                    
                else:
                    insert_period(date, time_shift, name, e_mail, buurt, werkzaamheedeb, materiaal, opmerking)
                    st.success("You booked an appointment!")
                    
            else:
                st.warning('At the moment it is only possible to make an appointment on Tuesday or Thursday', icon="⚠️")
            
           
# --- drop appointment ---
if selected == "Cancel an appointment":
    with st.form("cancel_form", clear_on_submit=True):

        date = str(st.date_input("Date"))
        time_shift = st.selectbox("Time shift", time_shift_choice )
        e_mail = st.text_input("", placeholder="Enter your e-mail here ...")
        
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        
        key = df[(df.date==date) & (df.time_shift==time_shift) & (df.e_mail==e_mail)]["key"].values[0]
        
        "---"
        
        submitted = st.form_submit_button("Cancel appointment")
        if submitted:
            db.delete(key)
            st.success("Your appointment has been canceled!") 
