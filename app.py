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
def insert_period(membership,date, day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number = None, ):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.insert({"Membership":membership, "Membership_number":membership_number, "Date": date, "Day":day, "Week":week, "Time shift": time_shift, 
                   "Name": name, "e_mail": e_mail, "Phone number": number,
                   "Neighborhood": buurt, "Expertise": expertise, "Type of bike": type_bike,
                   "Type of reparation":materiaal, "Remarks":opmerking
                  })


# --- SETTINGS ---
page_title = None
page_icon = " :bike: "  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
time_shift_choice = ["14-16", "16-18", "18-20"]
buurt_choice = ["Oud-oost","Indische Buurt/Oostelijk Havengebied",
                "Watergraafsmeer","Ijburg/Zeeburgereiland","Centrum",
                "Zuid","Zuidoost","Weesp","West","Nieuw-West"]
expertise_choice = ["None", "Low", "Average", "High"]
type_bike = ["City Bike Pedal Brake","City Bike Internal Gears",
"Cyty Bike External Gears","Mountain Bike","Race Bike"]
materiaal_choice = ["Dont know exactly","Flat tire","Change tire front/back ",
"Chain","Chain cover","Derailleur","Cassette","Sprocket",
"Brake cable","Brake pads","Brake problem pedalbrake",
"Gear problem","Gear cable","Front Axel","Play back wheel",
"Broken front wheel","Broken back wheel","Spokes",
"Bottom bracket","Crank left or right","Pedals",
"Front fork","Handlebars /handelbars pen","Saddle/ saddle pen",
"Bike lighting","Lock removal","Nieuw lock","Luggage carrier","Front rek"]

MEMBERSHIP_CHOICE = ["I want a membership (€50 for 10x workspace usage)", "I will use it only Once (€10 per 2 hours)","I have a Membership",]

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
    st.markdown("Fietskliniek is a membership based workspace. Membership is €50 a year voor 10 times use of the space 2 hours per session. Membership is ‘transferable’, you and your friends, collegues  can make use of it. In the bike workspace you will find all the tools and parts you need to repair your bike and you will get free guidance in the process.") 
    st.markdown("In case you want to use the workspace only once the minimum price is €10 a 2 hour session paid in advance. After making a reservation online you will get  a payement request to your phone number, when paid, then your reservation is confirmed. When cancelled you will get your money back minus €2 for admin pourposes.")
    st.markdown("Welcome to the Fietskliniek and enjoy your bike session!")

# --- INPUT & SAVE PERIODS ---
if selected == "Make an appointment":
    membership = st.radio("Payement / betaling", MEMBERSHIP_CHOICE, horizontal = False)
    if membership == "I have a Membership":
        membership_number = st.text_input("", placeholder="Membership number to fill in ...",label_visibility="collapsed")
    elif membership == "I will use it only Once (€10 per 2 hours)":
        "https://www.ing.nl/particulier/betaalverzoek/index.html?trxid=4xGXt7LA0Kaipfn9tEllAPl7AcrbDhjR"
        
    with st.form("entry_form", clear_on_submit=False):                  
        date = st.date_input("Date (only Tuesday or Thursday)")
        day = date.strftime("%A")
        week = date.isocalendar()[1]
        time_shift = st.radio("Time shift", time_shift_choice, horizontal = True)
        name = st.text_input("Name*", placeholder="Enter your name here ...")
        e_mail = st.text_input("E-mail*", placeholder="Enter your e-mail here ...")
        number = st.text_input("Telophone number*", placeholder="Enter your number here ...")
        buurt = st.selectbox("In which neighbourhood do you live in Amsterdam / Uit welk buurt kom je? (Voor statistic pourposes)", buurt_choice)
        expertise = st.selectbox("What is your expertise with bikes? / Welk ervaring heb je met fietsen?", expertise_choice )
        type_bike = st.selectbox("Type of bike that you have? / Wat voor fiets wil je repareren?", type_bike)
        materiaal = st.selectbox("Repair to do / Reparatie te doen", materiaal_choice)
        opmerking = st.text_input("", placeholder="Opmerking ...",label_visibility="collapsed")
        
        """_*Mandatory fields_"""
        
        "---"

        # find if there are available shift in that data
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift)]
        df_control = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift) & (df["Name"]==name)]
        len = len(df_filter)

        # submit the data
        submitted = st.form_submit_button("Save Data")
        if len(df_control) == 0:
            if submitted:

                res = (dt.strptime(str(date), "%Y-%m-%d") - dt.today()).days
                if res < 1: 
                    st.warning('Please book an appointment at least two days in advance', icon="⚠️")
                elif name and e_mail and number:
                    day = parser.parse(str(date)).strftime("%A")

                    try:
                        int(number)
                        if day == "Thursday" or day == "Tuesday":

                            if time_shift=="14-16" and len >= 1:
                                st.warning('This time shift is already full. Please choose another one', icon="⚠️")

                            elif time_shift=="16-18" and len >= 2:
                                st.warning('This time shift is already full. Please choose another one', icon="⚠️")

                            elif time_shift=="18-20" and len >= 3:
                                st.warning('This time shift is already full. Please choose another one', icon="⚠️")



                            else:
                                if membership == "I have a Membership":
                                    insert_period(membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                else:
                                    insert_period(membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                st.success("You booked an appointment!")
                        else:
                            st.warning('At the moment it is only possible to make an appointment on Tuesday or Thursday', icon="⚠️")
                    except:
                        st.error('Telephone number incorrect', icon="💥")
                else:
                    st.warning('Please fill the mandatory fields', icon="⚠️") 
            else:
                st.warning('There is already an appointment at this date and time with the same name', icon="⚠️") 
        
            
           
# --- drop appointment ---
if selected == "Cancel an appointment":
    with st.form("cancel_form", clear_on_submit=False):

        date = str(st.date_input("Date"))
        time_shift = st.selectbox("Time shift", time_shift_choice )
        e_mail = st.text_input("", placeholder="Enter your e-mail here ...")
        
        "---"
        
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df["Date"]==date) & (df["Time shift"]==time_shift) & (df.e_mail==e_mail)]
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
