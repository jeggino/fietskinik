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


# --- SETTINGS ---
page_title = None
page_icon = " :bike: "  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --- HERE THE CHANGE WITH THE SHIFT, 14-16 HAS BEEN DELETED ---
time_shift_choice_dinsdag_donderdag = ["18:30-20:30"]
time_shift_choice_vrijdag = ["11:00-13:00","13:30-15:30","15:30-17:30"]
time_shift_choice_cancel = ["11:00-13:00","13:30-15:30","15:30-17:30","18:30-20:30"]

name_picture = f"{random.randint(1,1000000000000)}.jpeg"


buurt_choice = ["Oud-oost","Indische Buurt/Oostelijk Havengebied",
                "Watergraafsmeer","Ijburg/Zeeburgereiland","Centrum",
                "Zuid","Zuidoost","Weesp","West","Nieuw-West"]

expertise_choice = ['Geen','Laag','Gemiddeld','Ervaren']

type_bike = ["Terugtraprem", "Racefiets","Versnellingen buiten","Versnellingen binnen","Vouwfiets","Kinderfiets",
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

MEMBERSHIP_CHOICE = [ "ik heb geen Stadspas (€12 per 2 uur)", "ik heb een Stadspas"]

TEXT = """
Fietskliniek is een buurt-, sociaal betrokken fietswerkplaats. In de fietsenwerkplaats vind u alle gereedschappen en onderdelen (nieuw en tweedehands) die u nodig hebt om uw fiets te repareren en u krijgt begeleiding van een ervaren vrijwilliger fietsenmaker daarbij. Hierbij moet je rekening houden met de volgende regels:

- Afspraak is max 2uur.
- Als de fiets niet klaar is binnen 2 uur, dan moet er een nieuwe afspraak gemaakt worden.
- Als u meerdere fietsen hebt om te repareren moeten er meerdere afspraken worden gemaakt.
- Eenmalig gebruik van de werkplaats kost €12. Met Stadspas €4,00.
- Onderdelen nodig voor de reparatie moeten apart worden betaald. We hebben nieuwe - en 2e hands onderdelen voor de halve prijs van een nieuwe.
- Vul onderstaand formulier in om te reserveren. Zodra u op Gegevens opslaan klikt, is uw reservering voltooid! U krijgt geen bevestiging.
- U kunt niet dezelfde dag reserveren waarop u langs wilt komen. Indien u een reservering heeft gemaakt en u kunt niet komen, kunt u deze gewoon annuleren via de knop hierboven, dit kan op dezelfde dag als de afspraak tot 12.00 uur.
- Bij annulering tot 12.00 uur krijgt u uw geld terug minus € 2,- voor administratieve doeleinden. Bij no-show of no-cancelling krijgt u geen geld terug.

Welkom bij de Fietskliniek en geniet van uw fietssessie!
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

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Maak een afspraak", "Afspraak afzeggen"],
    icons=["bi-journal-check", "bi-x-octagon-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

def Nederland():
        
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
        type_bike = st.selectbox("Wat voor fiets wilt u repareren?", type_bike)
        if type_bike in ["Backfiets - Stuur een foto aub","E-bike - Stuur een foto aub","mijn fiets staat er niet op"]:
            picture = st.file_uploader("Upload een foto")
            
            if picture:
                st.image(picture,width = 300)
                
            if not picture:
                st.warning("Upload een foto van uw fiets")
                st.stop()  
                
        materiaal = st.multiselect("Reparatie te doen", materiaal_choice)
        opmerking = st.text_input("", placeholder="Stuur een berich, vraag, enz ...",label_visibility="collapsed")
        
        """_*Verplichte velden_"""
        
        "---"
    
        # find if there are available shift in that data
        db_content = db.fetch().items
        df = pd.DataFrame(db_content)
        df_filter = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift)]
        df_control = df[(df["Date"]==str(date)) & (df["Time shift"]==time_shift) & (df["Name"]==name)]
        len_1 = len(df_filter)
        len_control = len(df_control)       
    
        # submit the data
        submitted = st.button("Gegevens opslaan")
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
        
                            if time_shift=="18:30-20:30" and len_1 >= 3:
                                st.warning('Deze tijdsverschuiving is al vol. Kies een andere', icon="⚠️")
        
                            else:
                                try:
                                    bytes_data = picture.getvalue()
                                    drive.put(name_picture, data=bytes_data)
                                    if membership == "ik heb een stadspads":
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                    else:
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                except:
                                    if membership == "ik heb een stadspads":
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                    else:
                                        insert_period(name_picture,membership,  str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                st.success("🚲🚲 U heeft een afspraak gemaakt! 🚲🚲")
        
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
                                    if membership == "ik heb een stadspads":
                                        insert_period(name_picture,membership,str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                    else:
                                        insert_period(name_picture,membership,str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                except:
                                    if membership == "ik heb een stadspads":
                                        insert_period(name_picture, membership, str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number)
                                    else:
                                        insert_period(name_picture, membership, str(date), day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking)
                                st.success("🚲🚲 U heeft een afspraak gemaakt! 🚲🚲")
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




pg = st.navigation([st.Page(Netherlands,icon="🇳🇱")])
pg.run()
