import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
from dateutil import parser
from datetime import datetime as dt

from PIL import Image



# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])

# Create a new database
db = deta.Base("project_fietskliniek")

# --- FUNCTIONS ---
def insert_period(date, time_shift, name, e_mail, number, buurt, expertise, werkzaamheedeb, materiaal, opmerking):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.insert({"date": date, "time_shift": time_shift, 
                   "name": name, "e_mail": e_mail, "number": number,
                   "buurt": buurt, "expertise": expertise, "werkzaamheden": werkzaamheedeb, 
                   "reparatie":materiaal, "opmerking":opmerking
                  })


# --- SETTINGS ---
page_title = None
page_icon = " :bike: "  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
time_shift_choice = ["14-16", "16-18", "18-20"]
buurt_choice = ["Centrum", "Oost", "West"]
expertise_choice = ["None", "Low", "Average", "High"]
materiaal_choice = ["wielen", "spatbord", "keten"]

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


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

left, right = st.columns([1,3])

with left:
    
    image = Image.open('292366152_369803905279628_8461882568456452789_n.jpg')
    st.image(image)
    
with right:
    st.markdown("Fietskliniek is a wonderful place where you can repair your own bike for just 5 euros! we will help you, and make our tools and space available, but, as we :red[MUST] pay the rent every month. For this reason, we ask you to pay in advance at this :blue[_link_]. If you cancel the appointment we will give you the money back.") 
    st.markdown("At moment, the space is available only on Tuesday and Thursday and you can book an appointment only with two days in advance. Furthermore, we wish to ask you about your experiences and also some other information that you will find in the form...see you soon!")


# --- INPUT & SAVE PERIODS ---
if selected == "Make an appointment":
    with st.form("entry_form", clear_on_submit=False):
        
        # create the inputs
        
        date = str(st.date_input("Date (only Tuesday or Thursday)", help="Here some explination text if you want"))
        st.write(date)
        time_shift = st.selectbox("Time shift", time_shift_choice )
        name = st.text_input("Name*", placeholder="Enter your name here ...")
        e_mail = st.text_input("E-mail*", placeholder="Enter your e-mail here ...")
        number = st.text_input("Telophone number*", placeholder="Enter your number here ...")
        buurt = st.selectbox("Buurt", buurt_choice)
        expertise = st.selectbox("What is your expertise?", expertise_choice )
        werkzaamheedeb = st.text_input("", placeholder="Werkzaamheden ...")
        materiaal = st.selectbox("Reparatie", materiaal_choice)
        opmerking = st.text_input("", placeholder="Opmerking ...")
        """_*Mandatory fields_"""
        "---"

        # find if there are available shift in that data
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df.date==date) & (df.time_shift==time_shift)]
        len = len(df_filter)

        # submit the data
        submitted = st.form_submit_button("Save Data")
        if submitted:         

            res = (dt.strptime(date, "%Y/%m/%d") - dt.strptime('2023/1/9', "%Y/%m/%d")).days
            if res < 2: 
                st.warning('kjhvkvkjhgv', icon="⚠️")
            elif name and e_mail and number:
                day = parser.parse(date).strftime("%A")
                
                try:
                    int(number)
                    if day == "Thursday" or day == "Tuesday":

                        if time_shift=="14-16" and len >= 1:
                            st.warning('please choice another time-shift', icon="⚠️")

                        elif time_shift=="16-18" and len >= 2:
                            st.warning('please choice another time-shift', icon="⚠️")

                        elif time_shift=="18-20" and len >= 3:
                            st.warning('please choice another time-shift', icon="⚠️")

                        else:
                            insert_period(date, time_shift, name, e_mail, number, buurt, expertise, werkzaamheedeb, materiaal, opmerking)
                            st.success("You booked an appointment!")
                    else:
                        st.warning('At the moment it is only possible to make an appointment on Tuesday or Thursday', icon="⚠️")
                except:
                    st.error('Telephone number incorrect', icon="💥")
            else:
                st.warning('Please fill the mandatory fields', icon="⚠️") 
            
           
# --- drop appointment ---
if selected == "Cancel an appointment":
    with st.form("cancel_form", clear_on_submit=False):

        date = str(st.date_input("Date"))
        time_shift = st.selectbox("Time shift", time_shift_choice )
        e_mail = st.text_input("", placeholder="Enter your e-mail here ...")
        
        "---"
        
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df.date==date) & (df.time_shift==time_shift) & (df.e_mail==e_mail)]
        submitted = st.form_submit_button("Cancel appointment")
        if submitted:
            if e_mail:
                if len(df_filter) > 0:
                    key = df_filter["key"].values[0]       
                    db.delete(key)
                    st.success("Your appointment has been canceled!") 
                else:
                    st.warning('there is no appointment at this email', icon="⚠️")

            else:
                st.warning('please write your e_mail', icon="⚠️")
