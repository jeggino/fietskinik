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

# --- HERE THE CHANGE WITH THE SHIFT, 14-16 HAS BEEN DELETED ---
time_shift_choice_dinsdag_donderdag = ["18:30-20:30"]
time_shift_choice_vrijdag = ["11:30-13:30","13:30-15:30","15:30-17:30"]

buurt_choice = ["Oud-oost","Indische Buurt/Oostelijk Havengebied",
                "Watergraafsmeer","Ijburg/Zeeburgereiland","Centrum",
                "Zuid","Zuidoost","Weesp","West","Nieuw-West"]

expertise_choice = ["None", "Low", "Average", "High"]

type_bike = ["Vouwfiets","Kinderfiets",
"Driewieler","Backfiets","E-bike","mijn fiets staat er niet op"]

materiaal_choice = ["Dont know exactly","Flat tire","Change tire front/back ",
"Chain","Chain cover","Derailleur","Cassette","Sprocket",
"Brake cable","Brake pads","Brake problem pedalbrake",
"Gear problem","Gear cable","Front Axel","Play back wheel",
"Broken front wheel","Broken back wheel","Spokes",
"Bottom bracket","Crank left or right","Pedals",
"Front fork","Handlebars /handelbars pen","Saddle/ saddle pen",
"Bike lighting","Lock removal","Nieuw lock","Luggage carrier","Front rek"]

MEMBERSHIP_CHOICE = ["ik heb een stadspads", "ik heb geen Stadspas (€12 per 2 uur)"]
TEXT = """
Fietskliniek is een buurt-, sociaal betrokken fietswerkplaats. In de fietsenwerkplaats vind je alle gereedschappen en onderdelen (nieuw en tweedehands) die je nodig hebt om je fiets te repareren en je krijgt gratis begeleiding van een ervaren fietsenmaker daarbij. Hierbij moet je rekening houden met de volgende regels

Afspraak is max 2uur

Als de fiets niet klaar is binnen 2 uur, dan moet er een nieuwe afspraak gemaakt worden.

Als je meerdere fietsen hebt om te repareren moeten er meerdere afspraken worden gemaakt.

Eenmalig gebruik van de werkplaats kost €12. Met Stadspas €4,00

Onderdelen nodig voor de reparatie moeten apart worden betaald. We hebben nieuw een 2e hands onderdelen voor een halve prijs van een nieuwe.

Vul onderstaand formulier in om te reserveren. Zodra u op Gegevens opslaan klikt, is uw reservering voltooid! Je krijgt geen bevestiging.

U kunt niet dezelfde dag reserveren waarop u langs wilt komen. Indien u een reservering heeft gemaakt en U kunt niet komen, kunt u deze gewoon annuleren via de knop hierboven, dit kan op dezelfde dag als de afspraak tot 12.00 uur.

Bij annulering tot 12.00 uur krijgt u uw geld terug minus € 2,- voor administratieve doeleinden. Bij no-show of no-cancelling krijgt U geen geld terug.

Welkom bij de Fietskliniek en geniet van je fietssessie!

ENGELS

Fietskliniek is a neighborhood, socially engaged bicycle workshop. In the bicycle workshop you will find all the tools and parts (new and second-hand) you need to repair your bicycle and you will receive free guidance from a bike mechanic. You must take the following rules into account

Appointment is max 2 hours

If the bicycle is not ready within 2 hours, a new appointment must be made.

If you have multiple bicycles to repair, multiple appointments must be made.

One-time use of the workshop costs €12. With Stadspas only €4.00

Parts required for the repair must be paid for separately. We have new and second-hand parts for half the price of new ones.

Complete the form below to make a reservation. Once you click Save Details, your reservation is complete! You will not receive confirmation.

You cannot reserve the same day you want to visit. If you have made a reservation and you cannot come, you can simply cancel it via the button above, this can be done on the same day as the appointment until 12:00 noon.

If you cancel before 12:00, you will receive your money back minus €2 for administrative purposes. In case of no-show or no-cancellation you will not receive a refund.

Welcome to the Fietskliniek and enjoy your cycling session!"""

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

# left, right = st.columns([1,3])

# with left:
    
image = Image.open('292366152_369803905279628_8461882568456452789_n.jpg')
st.image(image)
    
# with right:
st.markdown(TEXT) 

# --- INPUT & SAVE PERIODS ---
if selected == "Make an appointment":       
    
    membership = st.radio("Betaling", MEMBERSHIP_CHOICE, horizontal = False)
    if membership == "ik heb een stadspads":
        membership_number = st.text_input("", placeholder="Stadspasnummer overschrijven ...",label_visibility="collapsed")

    date = st.date_input("Datum (alleen Dinsdag, Donderdag, of Vrijdag)")
    day = date.strftime("%A")
    week = date.isocalendar()[1]
    
    if day not in ["Tuesday","Thursday","Friday"]:
        st.warning("U kunt alleen een afspraak maken op dinsdag, donderdag of vrijdag")
        st.stop()
        
    if day=="Friday":
        time_shift = st.radio("Time shift", time_shift_choice_vrijdag, horizontal = True)
    else:
        time_shift = st.radio("Time shift", time_shift_choice_dinsdag_donderdag, horizontal = True)
        
    name = st.text_input("Name*", placeholder="Enter your name here ...")
    e_mail = st.text_input("E-mail*", placeholder="Enter your e-mail here ...")
    number = int(st.text_input("Telophone number*", placeholder="Enter your number here ..."))
    buurt = st.selectbox("In which neighbourhood do you live in Amsterdam / Uit welk buurt kom je? (Voor statistic pourposes)", buurt_choice)
    expertise = st.selectbox("What is your expertise with bikes? / Welk ervaring heb je met fietsen?", expertise_choice )
    type_bike = st.selectbox("Type of bike that you have? / Wat voor fiets wil je repareren?", type_bike)
    
    if type_bike in ["Backfiets","E-bike","mijn fiets staat er niet op"]:
        picture = st.camera_input("Maak een foto")
        if not picture:
            st.warning("Upload een foto van uw fiets")
            st.stop()
            
    materiaal = st.selectbox("Repair to do / Reparatie te doen", materiaal_choice)
    opmerking = st.text_input("", placeholder="Opmerking ...",label_visibility="collapsed")
    
    """_*Mandatory fields_"""
    
    "---"

    # find if there are available shift in that data
    db_content = db.fetch().items
    df = pd.DataFrame(db_content)
    df_filter = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift)]
    df_control = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift) & (df["Name"]==name)]
    len_1 = len(df_filter)
    len_control = len(df_control)       

    # submit the data
    submitted = st.button("Save Data")
    if submitted:

        if name == None or e_mail==None or number==None:
            st.warning('Please fill the mandatory fields', icon="⚠️")
            st.stop()
            
        if len_control == 0:
            st.warning("HEREEEEEE")
            res = ((dt.strptime(str(date), "%Y-%m-%d").date() - dt.today().date()).days)
            if res == 0: 
                st.warning('Sorry, you cannot book an appointment on the same day', icon="⚠️")
                st.stop()
            else:
                day = parser.parse(str(date)).strftime("%A")
                int(number)
                st.warning("HEREEEEEE")
                if day in ["Thursday","Tuesday"]:

                    if time_shift=="18:30-20:30" and len_1 >= 3:
                        st.warning('This time shift is already full. Please choose another one', icon="⚠️")

                elif day == "Friday":

                    if time_shift=="11:30-13:30" and len_1 >= 1:
                        st.warning('This time shift is already full. Please choose another one', icon="⚠️")

                    elif time_shift=="13:30-15:30" and len_1 >= 1:
                        st.warning('This time shift is already full. Please choose another one', icon="⚠️")

                    elif time_shift=="15:30-17:30" and len_1 >= 1:
                        st.warning('This time shift is already full. Please choose another one', icon="⚠️")



                else:
                    if membership == "ik heb een stadspads":
                        insert_period(membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                    else:
                        insert_period(membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                    st.success("You booked an appointment!")
                st.stop()
        else:
            st.warning('There is already an appointment at this date and time with the same name', icon="⚠️") 

        
           
##### --- drop appointment ---
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
