import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
from dateutil import parser
from datetime import datetime as dt
import random

from PIL import Image



# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])

# Create a new database
db = deta.Base("db_data")
drive = deta.Drive("df_pictures")

# --- FUNCTIONS ---
def insert_period(name_picture,membership,date, day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number = None, ):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.insert({"Name_picture":name_picture,"Membership":membership, "Membership_number":membership_number, "Date": date, "Day":day, "Week":week, "Time shift": time_shift, 
                   "Name": name, "e_mail": e_mail, "Phone number": number,
                   "Neighborhood": buurt, "Expertise": expertise, "Type of bike": type_bike,
                   "Type of reparation":materiaal, "Remarks":opmerking
                  })
    
#_________vakantie_______
def fun(dict_, date):
    for holiday_name, list_date in dict_.items():
        if date in list_date:
            return True, holiday_name
#_________vakantie_______


# HORIZONTAL_RED = "images/horizontal_red.png"
# ICON_RED = "images/icon_red.png"
# HORIZONTAL_BLUE = "images/horizontal_blue.png"
# ICON_BLUE = "images/icon_blue.png"

# options = [HORIZONTAL_RED, ICON_RED, HORIZONTAL_BLUE, ICON_BLUE]
# sidebar_logo = st.selectbox("Sidebar logo", options, 0)
# main_body_logo = st.selectbox("Main body logo", options, 1)

# --- SETTINGS ---
page_title = None
page_icon = " :bike: "  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --- HERE THE CHANGE WITH THE SHIFT, 14-16 HAS BEEN DELETED ---
time_shift_choice_dinsdag_donderdag = ["18:00-20:30"]
time_shift_choice_vrijdag = ["11:00-13:00","13:30-15:30","15:30-17:30"]
time_shift_choice_cancel = ["11:00-13:00","13:30-15:30","15:30-17:30","18:00-20:30"]

name_picture = f"{random.randint(1,1000000000000)}.jpeg"

PAYMENT_LINK_STADPASS = "https://www.ing.nl/payreq/m/?trxid=E9z1j5CtPzvaEY6gsUDwLCtGfhPxHK7T"
PAYMENT_LINK_NO_STADPASS = "https://www.ing.nl/payreq/m/?trxid=nT6szaulTjl68azo82hIuQ1FjeJOS4VR"


#_________vakantie_______
holidays = {'Herfstvakantie' : pd.date_range(start="2024-10-26", end="2024-11-03"),
'Kerstvakantie' : pd.date_range(start="2024-12-21", end="2025-01-05"),
'Voorjaarsvakantie' : pd.date_range(start="2025-02-15", end="2025-02-23"),
'Meivakantie' : pd.date_range(start="2025-04-26", end="2025-05-04"),
'Zomervakantie' : pd.date_range(start="2025-07-12", end="2025-08-04"),
            'Vrije dag' : []
            }

DAY_OFF = None
hol_dict = {}

for holiday in holidays.keys():
    
    list_holidays = []
    
    for date in holidays[holiday]:
        list_holidays.append(str(date.date()))
        
    hol_dict[holiday] = list_holidays

hol_dict['Vrije dag'].append(DAY_OFF)
#_________vakantie_______




buurt_choice = ['Bijlmer-West', 'Bijlmer-Centrum', 'Bijlmer-Oost', 'Bos en Lommer',
       'Oud-Zuid', 'Osdorp', 'Indische Buurt, Oostelijk Havengebied',
       'Centrum-West', 'Noord-West', 'Gaasperdam',
       'Sloterdijk Nieuw-West', 'De Aker, Sloten, Nieuw-Sloten',
       'Centrum-Oost', 'IJburg, Zeeburgereiland',
       'Geuzenveld, Slotermeer', 'Oud-Oost', 'Westerpark',
       'Buitenveldert, Zuidas', 'Weesp, Driemond', 'Noord-Oost',
       'Oud-West, De Baarsjes', 'De Pijp, Rivierenbuurt', 'Oud-Noord',
       'Slotervaart', 'Watergraafsmeer']

expertise_choice = ['Geen','Laag','Gemiddeld','Ervaren']

type_bikes = ["Terugtraprem", "Racefiets","Versnellingen buiten","Versnellingen binnen","Vouwfiets","Kinderfiets",
             "Driewieler","Backfiets - Stuur een foto aub","E-bike - Stuur een foto aub","mijn fiets staat er niet op"]

materiaal_choice = ['Ik weet niet precies', 
'Nieuw buitenband voor of achter',
'Ketting',
'Kettingkast',
'Derailleur' ,
'Cassette',
'Tandwiel',
'Remkabel',
'Remschoen',
'Terugtraprem probleem',
'Versnellings probleem binnenwerk',
'Versnellingsprobleem cassette',
'Versnellingskabel',
'Vooras',
'Achterwiel speling',
'Spaken',
'Trapas',
'Kettingwiel links of rechts',
'Pedalen',
'Voorvork',
'Stuur, stuurprn/Handlebars, handlebars pen',
'Zadel, zadelpen',
'Verlichting',
'Slot verwijderen',
'Nieuw lock',
'Achter, Voor rek']

MEMBERSHIP_CHOICE = [ "ik heb geen Stadspas (€15 per 2 uur)", "ik heb een Stadspas"]

TEXT = """
Fietskliniek is een buurt-, sociaal betrokken fietswerkplaats. In de fietsenwerkplaats vind u alle gereedschappen en onderdelen (nieuw en tweedehands) die u nodig hebt om uw fiets te repareren en u krijgt begeleiding van een ervaren vrijwilliger fietsenmaker daarbij. Hierbij moet je rekening houden met de volgende regels:

- Afspraak is max 2uur.
- Als de fiets niet klaar is binnen 2 uur, dan moet er een nieuwe afspraak gemaakt worden.
- Als u meerdere fietsen hebt om te repareren moeten er meerdere afspraken worden gemaakt.
- Eenmalig gebruik van de werkplaats kost €15. Met Stadspas €4,00.
- Onderdelen nodig voor de reparatie moeten apart worden betaald. We hebben nieuwe - en 2e hands onderdelen voor de halve prijs van een nieuwe.
- Vul onderstaand formulier in om te reserveren. Zodra u op Gegevens opslaan klikt, is uw reservering voltooid! U krijgt geen bevestiging.
- U kunt niet dezelfde dag reserveren waarop u langs wilt komen. 
- Indien u een reservering heeft gemaakt en u kunt niet komen, kunt u deze gewoon annuleren via de knop hierboven, dit kan op dezelfde dag als de afspraak tot 12.00 uur.
- Bij annulering tot 12.00 uur krijgt u uw geld terug minus € 4,- voor administratieve doeleinden. Bij no-show of no-cancelling krijgt u geen geld terug.

Welkom bij de Fietskliniek en geniet van uw fietssessie!
"""

#---COSTANTS IN ENGLISH---
expertise_choice_english = ['None', 'Low', 'Average', 'Experienced']

type_bikes_english = ["Coaster brake", "Racing bike","Outside gears","Inside gears","Folding bike","Children's bike", "Tricycle","Cargo bike - Please send a photo","E-bike - Please send a photo","my bike is not listed"]


materiaal_choice_english = ['I dont know exactly',
'New outer tire front or rear',
'Chain',
'Chain case',
'Derailleur',
'Cassette',
'Sprocket',
'Brake cable',
'Brake shoe',
'Coaster brake problem',
'Gear internals problem',
'Gear cassette problem',
'Gear cable',
'Front axle',
'Rear wheel play',
'Spokes',
'Bottom bracket',
'Left or right sprocket',
'Pedals',
'Front fork',
'Handlebars, handlebars pin',
'Saddle, seat post',
'Lighting',
'Remove lock',
'New lock',
'Rear, Front rack']

MEMBERSHIP_CHOICE_english = ["I don't have a City Pass (€15 per 2 hours)", "I have a City Pass"]

TEXT_english = """
Fietskliniek is a neighbourhood, socially involved bicycle workshop. In the bicycle workshop you will find all the tools and parts (new and second-hand) that you need to repair your bicycle and you will be guided by an experienced volunteer bicycle mechanic. You must take the following rules into account:

- Appointment is max 2 hours.
- If the bicycle is not ready within 2 hours, a new appointment must be made.
- If you have multiple bicycles to repair, multiple appointments must be made.
- One-time use of the workshop costs €15. With City Pass €4.00.
- Parts needed for the repair must be paid for separately. We have new - and second-hand parts for half the price of a new one.
- Fill in the form below to make a reservation. As soon as you click on Save data, your reservation is complete! You will not receive a confirmation.
- You cannot make a reservation on the same day that you want to come by. If you have made a reservation and you cannot come, you can simply cancel it via the button above, this can be done on the same day as the appointment until 12:00.
- If you cancel until 12:00, you will receive your money back minus €4,- for administrative purposes. In case of no-show or no-cancellation, you will not receive any money back.

Welcome to the Cycling Clinic and enjoy your cycling session!
"""




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

on = st.toggle("🇬🇧")

if not on:
    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Maak een afspraak", "Afspraak afzeggen"],
        icons=["bi-journal-check", "bi-x-octagon-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )


        
    image = Image.open('292366152_369803905279628_8461882568456452789_n.jpg')
    st.image(image)
        
    # with right:
    st.markdown(TEXT) 
    
    "---"
    
    # --- INPUT & SAVE PERIODS ---
    if selected == "Maak een afspraak":       
        
        membership = st.radio("Betaling", MEMBERSHIP_CHOICE, horizontal = False)
        if membership == "ik heb een Stadspas":
            membership_number = st.text_input("", placeholder="Stadspasnummer overschrijven ...",label_visibility="collapsed")
            
            if  len(membership_number) == 0:
                st.warning("Vul het Stadspasnummer in aub")
                st.stop()
    
        date = st.date_input("Datum (alleen Dinsdag, Donderdag, of Vrijdag)")
        day = date.strftime("%A")
        week = date.isocalendar()[1]
        

        #_________vakantie_______
        res_holiday = fun(hol_dict, str(date))

        try:
            if res_holiday[0]==True:
                st.warning(f"Het is {res_holiday[1]}! Excuus, de Fietskliniek is gesloten.")
                st.stop()
        except:
            pass
        #_________vakantie_______

        
        if day not in ["Tuesday","Thursday","Friday"]:
            st.warning("U kunt alleen een afspraak maken op dinsdag, donderdag of vrijdag")
            st.stop()
            
        if day=="Friday":
            time_shift = st.radio("Tijdsverschuiving", time_shift_choice_vrijdag, horizontal = True)
        else:
            time_shift = st.radio("Tijdsverschuiving", time_shift_choice_dinsdag_donderdag, horizontal = True)
            
        name = st.text_input("Naam*", placeholder="Vul hier uw naam in ...")
        e_mail = st.text_input("E-mail*", placeholder="Voer hier uw e-mailadres in ...")
        number = st.text_input("Telefoonnummer*", placeholder="Voer hier uw nummer in ...")
        buurt = st.selectbox("Uit welke buurt komt u? (voor statistieken doeleinden)", buurt_choice)
        expertise = st.selectbox("Welke ervaring heeft u met fietsen?", expertise_choice )
        type_bike = st.selectbox("Wat voor fiets wilt u repareren?", type_bikes)
        if type_bike in ["Backfiets - Stuur een foto aub","E-bike - Stuur een foto aub","mijn fiets staat er niet op"]:
            picture = st.file_uploader("Upload een foto")
            
            if picture:
                st.image(picture,width = 300)
                
            if not picture:
                st.warning("Upload een foto van uw fiets")
                st.stop()  
                
        materiaal = st.multiselect("Reparatie te doen (Meer opties mogelijk)", materiaal_choice)
        opmerking = st.text_input("", placeholder="Stuur een bericht, vraag, enz ...",label_visibility="collapsed")
        
        """_*Verplichte velden_"""
        """:orange-background[_Persoonlijke data wordt niet opgeslagen, alleen gebruikt voor administratieve doeleinden van de gemaakte afspraak_]"""
        
        "---"
    
        # find if there are available shift in that data
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift)]
        df_control = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift) & (df["Name"]==name)]
        len_1 = len(df_filter)
        len_control = len(df_control)       
    
        # submit the data
        submitted = st.button(":red[**Gegevens opslaan**]")
        if submitted:
    
            if len(name) == 0 or len(e_mail)==0 or len(number)==0:
                st.warning('Vul de verplichte velden in', icon="⚠️")
                st.stop()
                
            if len_control == 0:
                res = ((dt.strptime(str(date), "%Y-%m-%d").date() - dt.today().date()).days)
                if res == 0: 
                    st.warning('Helaas kunt u geen afspraak op dezelfde dag boeken', icon="⚠️")
                    st.stop()
                else:
                    day = parser.parse(str(date)).strftime("%A")
                    try:
                        int(number)
                        if day in ["Thursday","Tuesday"]:
        
                            if time_shift=="18:00-20:30" and len_1 >= 3:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            else:
                                try:
                                    bytes_data = picture.getvalue()
                                    drive.put(name_picture, data=bytes_data)
                                    if membership == "ik heb een Stadspas":
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                        
                                except:
                                    if membership == "ik heb een Stadspas":
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                st.success("🚲🚲 U heeft een afspraak gemaakt! 🚲🚲")
                                st.warning("Bij het maken van een afspraak dient u te betalen om uw reservering veilig te stellen")
        
                        elif day == "Friday":
        
                            if time_shift=="11:00-13:00" and len_1 >= 1:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            elif time_shift=="13:30-15:30" and len_1 >= 1:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            elif time_shift=="15:30-17:30" and len_1 >= 1:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            else:
                                try:
                                    bytes_data = picture.getvalue()
                                    drive.put(name_picture, data=bytes_data)
                                    if membership == "ik heb een Stadspas":
                                        insert_period(name_picture,membership,str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture,membership,str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                except:
                                    if membership == "ik heb een Stadspas":
                                        insert_period(name_picture, membership, str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture, membership, str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                st.success("🚲🚲 U heeft een afspraak gemaakt! 🚲🚲")
                                st.warning("Bij het maken van een afspraak dient u te betalen om uw reservering veilig te stellen")
                    except:
                        st.error("Vul alstublieft een juist telefoonnummer in")
    
            else:
                st.warning('Er is al een afspraak op deze datum en tijd met dezelfde naam', icon="⚠️") 
    
            
               
    ##### --- drop appointment ---
    if selected == "Afspraak afzeggen":
        with st.form("cancel_form", clear_on_submit=False):
    
            date = str(st.date_input("Datum"))
            time_shift = st.selectbox("Tijdsverschuiving", time_shift_choice_cancel )
            e_mail = st.text_input("", placeholder="Voer hier uw e-mailadres in ...")
            
            "---"
            
            db_content = db.fetch().items
            df = pd.DataFrame(db_content)
            df_filter = df[(df["Date"]==date) & (df["Time shift"]==time_shift) & (df.e_mail==e_mail)]
            submitted = st.form_submit_button("Afspraak annuleren")
            if submitted:
                if e_mail:
                    if len(df_filter) > 0:
                        key = df_filter["key"].values[0]       
                        db.delete(key)
                        st.success("Uw afspraak is geannuleerd!") 
                    else:
                        st.warning('Er is geen afspraak op dit e-mailadres', icon="⚠️")
    
                else:
                    st.warning('schrijf alstublieft uw e-mail', icon="⚠️")


else:    
    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Make an appointment", "Cancel appointment"],
        icons=["bi-journal-check", "bi-x-octagon-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )


        
    image = Image.open('292366152_369803905279628_8461882568456452789_n.jpg')
    st.image(image)
        
    # with right:
    st.markdown(TEXT_english) 
    
    "---"
    
    # --- INPUT & SAVE PERIODS ---
    if selected == "Make an appointment":       
        
        membership = st.radio("Payment", MEMBERSHIP_CHOICE_english, horizontal = False)
        if membership == "I have a City Pass":
            membership_number = st.text_input("", placeholder="Transfer city pass number ...",label_visibility="collapsed")
            
            if  len(membership_number) == 0:
                st.warning("Please enter the City Pass number")
                st.stop()
    
        date = st.date_input("Date (Tuesday, Thursday, or Friday only)")
        day = date.strftime("%A")
        week = date.isocalendar()[1]

                #_________vakantie_______
        res_holiday = fun(hol_dict, str(date))

        try:
            if res_holiday[0]==True:
                st.warning(f"It's {res_holiday[1]}! Sorry, the Fietskliniek is closed.")
                st.stop()
        except:
            pass
        #_________vakantie_______
        
        if day not in ["Tuesday","Thursday","Friday"]:
            st.warning("You can only make an appointment on Tuesday, Thursday or Friday")
            st.stop()
            
        if day=="Friday":
            time_shift = st.radio("Time shift", time_shift_choice_vrijdag, horizontal = True)
        else:
            time_shift = st.radio("Time shift", time_shift_choice_dinsdag_donderdag, horizontal = True)
            
        name = st.text_input("Name*", placeholder="Enter your name here ...")
        e_mail = st.text_input("E-mail*", placeholder="Enter your email address here ...")
        number = st.text_input("Phone number*", placeholder="Enter your number here ...")
        buurt = st.selectbox("What neighborhood are you from? (for statistics purposes)", buurt_choice)
        expertise = st.selectbox("What experience do you have with cycling?", expertise_choice_english )
        type_bike = st.selectbox("What kind of bicycle do you want to repair?", type_bikes_english)
        if type_bike in ["Cargo bike - Please send a photo","E-bike - Please send a photo","my bike is not listed"]:
            picture = st.file_uploader("Upload a photo")
            
            if picture:
                st.image(picture,width = 300)
                
            if not picture:
                st.warning("Upload a photo of your bike")
                st.stop()  
                
        materiaal = st.multiselect("Repair to be done (More options possible)", materiaal_choice_english)
        opmerking = st.text_input("", placeholder="Send a message, question, etc. ...",label_visibility="collapsed")
        
        """_*Required fields_"""
        """:orange-background[_personal data is not stored, only used for administrative purposes of the appointment made_]"""
        
        "---"
    
        # find if there are available shift in that data
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift)]
        df_control = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift) & (df["Name"]==name)]
        len_1 = len(df_filter)
        len_control = len(df_control)       
    
        # submit the data
        submitted = st.button(":red[**Save data**]")
        if submitted:
    
            if len(name) == 0 or len(e_mail)==0 or len(number)==0:
                st.warning('Please fill in the required fields', icon="⚠️")
                st.stop()
                
            if len_control == 0:
                res = ((dt.strptime(str(date), "%Y-%m-%d").date() - dt.today().date()).days)
                if res == 0: 
                    st.warning('Unfortunately, you cannot book an appointment on the same day', icon="⚠️")
                    st.stop()
                else:
                    day = parser.parse(str(date)).strftime("%A")
                    try:
                        int(number)
                        if day in ["Thursday","Tuesday"]:
        
                            if time_shift=="18:00-20:30" and len_1 >= 3:
                                st.warning('This time shift is already full. Choose another one', icon="⚠️")
        
                            else:
                                try:
                                    bytes_data = picture.getvalue()
                                    drive.put(name_picture, data=bytes_data)
                                    if membership == "I have a City Pass":
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                except:
                                    if membership == "I have a City Pass":
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                st.success("🚲🚲 You have booked an appointment! 🚲🚲")
                                st.warning("When making an appointment, payement has to be done to secure your reservation")
                    
        
                        elif day == "Friday":
        
                            if time_shift=="11:00-13:00" and len_1 >= 1:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            elif time_shift=="13:30-15:30" and len_1 >= 1:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            elif time_shift=="15:30-17:30" and len_1 >= 1:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            else:
                                try:
                                    bytes_data = picture.getvalue()
                                    drive.put(name_picture, data=bytes_data)
                                    if membership == "I have a City Pass":
                                        insert_period(name_picture,membership,str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture,membership,str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                except:
                                    if membership == "I have a City Pass":
                                        insert_period(name_picture, membership, str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                        st.markdown(PAYMENT_LINK_STADPASS)
                                    else:
                                        insert_period(name_picture, membership, str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                        st.markdown(PAYMENT_LINK_NO_STADPASS)
                                st.success("🚲🚲 You have booked an appointment! 🚲🚲")
                                st.warning("When making an appointment, payement has to be done to secure your reservation")
                    except:
                        st.error("Please enter a correct phone number")
    
            else:
                st.warning('There is already an appointment on this date and time with the same name', icon="⚠️") 
    
            
               
    ##### --- drop appointment ---
    if selected == "Cancel appointment":
        with st.form("cancel_form", clear_on_submit=False):
    
            date = str(st.date_input("Date"))
            time_shift = st.selectbox("Time shift", time_shift_choice_cancel )
            e_mail = st.text_input("", placeholder="Enter your email address here ...")
            
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
                        st.success("Your appointment has been cancelled!") 
                    else:
                        st.warning('There is no appointment at this email address', icon="⚠️")
    
                else:
                    st.warning('Please write your email', icon="⚠️")
