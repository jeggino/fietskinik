#--------------------GOOGLE SHEET---------------------
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from streamlit_option_menu import option_menu  
from datetime import datetime as dt
import random
from dateutil import parser
import smtplib
from email.mime.text import MIMEText





# Maximum allowed bookings per day/time
SCHEDULE = {
    "Monday": {
        "10:00-12:00": 2,
        "13:00-15:00": 2,
        "15:00-17:00": 2
    },
    "Tuesday": {
        "10:00-12:00": 0,
        "13:00-15:00": 0,
        "15:00-17:00": 0,
    },
    "Wednesday": {
        "10:00-12:00": 0,
        "13:00-15:00": 0,
        "15:00-17:00": 0,
    },
    "Thursday": {
        "10:00-12:00": 0,
        "13:00-15:00": 0,
        "15:00-17:00": 0,
    },
    "Friday": {
        "10:00-12:00": 0,
        "13:00-15:00": 0,
        "15:00-17:00": 0,
    },
    "Saturday": {
        "10:00-12:00": 0,
        "13:00-15:00": 0,
        "15:00-17:00": 0,
    },
    "Sunday": {
        "10:00-12:00": 0,
        "13:00-15:00": 0,
        "15:00-17:00": 0,
    },
}

DUTCH_DAYS = {
    "Monday": "Maandag",
    "Tuesday": "Dinsdag",
    "Wednesday": "Woensdag",
    "Thursday": "Donderdag",
    "Friday": "Vrijdag",
    "Saturday": "Zaterdag",
    "Sunday": "Zondag"
}

holidays = {
'Kerstvakantie' : pd.date_range(start="2024-12-21", end="2025-01-05"),
'Meivakantie' : pd.date_range(start="2025-04-26", end="2025-05-04"),
'Zomervakantie' : pd.date_range(start="2025-08-01", end="2025-08-30"),
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



# --- FUNCTIONS ---
@st.dialog("📅 Afspraak bevestigd")
def appointment_dialog(
    membership, date, day, week, time_shift, name, e_mail, number,
    buurt, expertise, type_bike, materiaal, opmerking, membership_number
):
    st.markdown("### ✔ Je afspraak is succesvol geboekt!")

    st.write("Hier zijn de details van je reservering:")

    st.markdown(f"""
    **Naam:** {name}  
    **E-mail:** {e_mail}  
    **Telefoonnummer:** {number}  
    **Datum:** {date}  
    **Dag:** {day}  
    **Weeknummer:** {week}  
    **Tijdsverschuiving:** {time_shift}  
    **Membership:** {membership}  
    **Stadspasnummer:** {membership_number}  
    **Buurt:** {buurt}  
    **Ervaring:** {expertise}  
    **Type fiets:** {type_bike}  
    **Reparatie(s):** {materiaal}  
    **Opmerking:** {opmerking}
    """)

    st.markdown("---")

    st.markdown(
        "🚲 **Controleer je e-mail — daar vind je de link om de betaling te voltooien en je reservering veilig te stellen.**"
    )

    st.success("Bedankt voor je reservering!")

def is_slot_full(day, time_shift, current_count):
    """Return True if the time slot is full based on SCHEDULE."""
    if day not in SCHEDULE:
        return False  # no limits for this day
    
    if time_shift not in SCHEDULE[day]:
        return False  # no limits for this time shift
    
    max_allowed = SCHEDULE[day][time_shift]
    return current_count >= max_allowed

def is_day_available(day):
    return day in SCHEDULE and any(capacity > 0 for capacity in SCHEDULE[day].values())

def is_time_available(day, time_shift):
    return (
        day in SCHEDULE and 
        time_shift in SCHEDULE[day] and 
        SCHEDULE[day][time_shift] > 0
    )
    
def is_slot_full(day, time_shift, current_count):
    if not is_time_available(day, time_shift):
        return True  # treat unavailable as full
    return current_count >= SCHEDULE[day][time_shift]

def get_available_days(schedule):
    """Return list of days that have at least one time shift with capacity > 0."""
    return [day for day, shifts in schedule.items() if any(cap > 0 for cap in shifts.values())]


def get_available_time_shifts(schedule, day):
    """Return list of time shifts for a given day that have capacity > 0."""
    if day not in schedule:
        return []
    return [ts for ts, cap in schedule[day].items() if cap > 0]




def insert_period(membership,date, day, week, time_shift, name, e_mail, number, buurt, expertise, type_bike, materiaal, opmerking,membership_number = None):
    """Returns the user on a successful user creation, otherwise raises and error"""
    data = [{"Membership":membership, "Membership_number":membership_number, "Date": date, "Day":day, "Week":week, "Time shift": time_shift, 
    "Name": name, "e_mail": e_mail, "Phone number": number,
    "Neighborhood": buurt, "Expertise": expertise, "Type of bike": type_bike,
    "Type of reparation":materiaal, "Remarks":opmerking
    }]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="Data",data=df_updated)


def fun(dict_, date):
    for holiday_name, list_date in dict_.items():
        if date in list_date:
            return True, holiday_name
            

#--- SETTINGS ---
page_title = None
page_icon = " :bike: "  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"


#---PAYMENT LINK---
PAYMENT_LINK_STADPASS = "https://payment-links.mollie.com/payment/QRHiqREMEec7PXeByiszR"
PAYMENT_LINK_NO_STADPASS = "https://payment-links.mollie.com/payment/nrxyyvYYhHQP6t84dKynb"
PAYMENT_LINK_open = "https://www.ing.nl/payreq/m/?trxid=fjuDgJyqjT9ZPRryp5pSMunynvCmM6MH"

def mail(email_receiver, name, date, time, link, stadpas):
    subject = "Fietsklieniek appointment"
    body = f"""
    Beste {name},

    U heeft een afspraak met Fietskliniek DIY op {date} om {time} uur.
    (stadpas nummer: {stadpas})
    Het adres is Pieter Nieuwlandstraat 95.
    Mocht U verhindert zijn en niet kunnen komen, vragen we u om de afspraak af te zeggen op onderstaande link:
    https://fietskinik-afspraak.streamlit.app/

    Afspraak dient vooraf betaald te worden op onderstaande {link}

    Met vriendelijke groet,

    Fietskliniek Team
    Pieter Nieuwlandstraat 95
    1093XN Amsterdam (NL)
    Tel +31 (6)127 116 08
    FB: FietsKliniek
    www.nieuwland.cc/fietskliniek
    """

    msg = MIMEText(body)
    msg['From'] = st.secrets["EMAIL"]
    msg['To'] = email_receiver
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(st.secrets["EMAIL"], st.secrets["PASSWORD"])

        # Try sending the email
        server.sendmail(
            st.secrets["EMAIL"],
            [email_receiver, st.secrets["EMAIL"]],
            msg.as_string()
        )

        server.quit()
        return True  # email successfully sent

    except smtplib.SMTPRecipientsRefused:
        server.quit()
        return False

    except smtplib.SMTPDataError:
        server.quit()
        return False

    except smtplib.SMTPResponseException:
        server.quit()
        return False

    except Exception:
        server.quit()
        return False


    

#---POPUP CANCEL---
@st.dialog(" ")
def cancelpop():
    st.success("Uw afspraak is geannuleerd!")

@st.dialog(" ")
def cancelpop_english():
    st.success("Your appointment has been cancelled!")

#---mail English---
def mail_english(email_receiver,name,date,time,link,stadpas):
    subject = "Fietsklieniek appointment"
    body = f"""
    Dear {name},
    
    You have an appointment with Fietskliniek DIY on {date} at {time}.
    (stadpas number: {stadpas})
    The address is Pieter Nieuwlandstraat 95.
    
    Should you be unable to attend, we ask you to cancel the appointment via the link below:
    
    https://fietskinik-afspraak.streamlit.app/
    
    The appointment must be paid for in advance via the {link} below.
    
    Kind regards,
    
    Fietskliniek Team
    Pieter Nieuwlandstraat 95
    1093XN Amsterdam (NL)
    Tel +31 (6)127 116 08
    FB: FietsKliniek
    www.nieuwland.cc/fietskliniek
    """  
    
    msg = MIMEText(body)
    msg['From'] = st.secrets["EMAIL"]
    msg['To'] = email_receiver
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(st.secrets["EMAIL"], st.secrets["PASSWORD"])
    resp = server.rcpt(email_receiver)
    server.sendmail(st.secrets["EMAIL"], [email_receiver,st.secrets["EMAIL"]], msg.as_string())
    server.quit()
    



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
             "Driewieler","Backfiets","E-bike","mijn fiets staat er niet op"]

materiaal_choice = ['Ik weet niet precies', 
'Tire/tube',
'Ketting',
'Remmen',
'Versnellingen' ,
'Wiel recht zetten',
'Wiel vlechten',
]

MEMBERSHIP_CHOICE = [ "ik heb geen Stadspas (€20 per 2 uur)", "ik heb een Stadspas"]



TEXT = """
Fietskliniek is een buurt-, sociaal betrokken fietswerkplaats. In de fietsenwerkplaats vind u alle gereedschappen en onderdelen (nieuw en tweedehands) die u nodig hebt om uw fiets te repareren en u krijgt begeleiding van een ervaren vrijwilliger fietsenmaker daarbij. Hierbij moet je rekening houden met de volgende regels:

- Afspraak duur is max 2uur.
- Eenmalig gebruik van de werkplaats kost €20. Met Stadspas €4,00.
- Als de fiets niet klaar is binnen 2 uur, dan moet er een nieuwe afspraak gemaakt worden.
- Als u meerdere fietsen hebt om te repareren moeten er meerdere afspraken worden gemaakt.
- Klein probleem? Kom gewoon langs, zonder afspraak

Onderdelen
- Onderdelen nodig voor de reparatie moeten apart worden betaald.
- We hebben nieuwe - en 2e hands onderdelen voor de halve prijs van een nieuwe.
- Je mag je eigen onderdelen niet meenemen of gebruiken, tenzij anders afgesprokken
- We begrijpen dat materiaal elders goedkoper zou zijn, maar anders kunnen we dit project niet blijven runnen.
- We kiezen voor de voordeligste prijs-kwaliteit verhouding voor onze onderdelen

Afspraak maken/annuleren
- Vul onderstaand formulier in om te reserveren. Zodra u op Gegevens opslaan klikt, is uw
reservering voltooid! U krijgt een bevestiging per mail
- U kunt niet dezelfde dag reserveren waarop u langs wilt komen.
- Indien u een reservering heeft gemaakt en u kunt niet komen, kunt u deze gewoon annuleren
via de knop hierboven, dit kan de daag ervoor tot 12 uur
- Bij annulering tot 12.00 uur krijgt u uw geld terug minus € 4,- voor administratieve doeleinden. Bij no-show of no-cancelling krijgt u geen geld terug.
- Bij het maken van een afspraak dient u te betalen om uw reservering veilig te stellen.

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

#---LOAD DATASETS---
conn = st.connection("gsheets", type=GSheetsConnection)
df_old = conn.read(ttl=0,worksheet="Data")



# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Maak een afspraak", "Afspraak afzeggen"],
    icons=["bi-journal-check", "bi-x-octagon-fill"],
    orientation="horizontal",
)

"---"
# --- INPUT & SAVE PERIODS ---
if selected == "Maak een afspraak":       

    st.image('292366152_369803905279628_8461882568456452789_n.jpg')
    st.markdown(TEXT)

    # -----------------------------
    # MEMBERSHIP
    # -----------------------------
    membership = st.radio("Betaling", MEMBERSHIP_CHOICE)
    membership_number = (
        st.text_input(" ", "", placeholder="Stadspasnummer overschrijven ...", label_visibility="collapsed")
        if membership == "ik heb een Stadspas" else "-"
    )

    if membership == "ik heb een Stadspas" and not membership_number:
        st.warning("Vul het Stadspasnummer in aub")
        st.stop()

    # -----------------------------
    # DATE SELECTION
    # -----------------------------
    date = st.date_input("Datum")
    day_en = date.strftime("%A")
    day_nl = DUTCH_DAYS[day_en]
    week = date.isocalendar()[1]

    # Holiday check
    res_holiday = fun(hol_dict, str(date))
    if isinstance(res_holiday, (list, tuple)) and res_holiday[0]:
        st.warning(f"Het is {res_holiday[1]}! Excuus, de Fietskliniek is gesloten.")
        st.stop()

    # Day availability
    if day_en not in get_available_days(SCHEDULE):
        st.warning(f"Op {day_nl} is het niet mogelijk een afspraak te maken.")
        st.stop()

    # -----------------------------
    # TIME SHIFT SELECTION
    # -----------------------------
    available_shifts = get_available_time_shifts(SCHEDULE, day_en)
    if not available_shifts:
        st.warning(f"Op {day_nl} zijn geen tijdsverschuivingen beschikbaar.")
        st.stop()

    time_shift = st.radio("Tijdsverschuiving", available_shifts)

    # -----------------------------
    # PERSONAL DATA
    # -----------------------------
    name = st.text_input("Naam*", placeholder="Vul hier uw naam in ...")
    e_mail = st.text_input("E-mail*", placeholder="Voer hier uw e-mailadres in ...")
    email_receiver_test = st.text_input("E-mail-test*", placeholder="Herhaal uw e-mailadres ...")

    if e_mail != email_receiver_test:
        st.write("UW E-MAILADRES KOMT NIET OVEREEN. CONTROLEER HET AUB!")
        st.stop()

    # -----------------------------
    # TYPE OF DAY (APPOINTMENT / FREE DAY)
    # -----------------------------
    type_day = st.selectbox(
        "Dit veld is voor de vrijwilliger. Vul 'afspraak' in als u een reservering wilt maken.",
        ['Afspraak', 'Vrije dag']
    )

    if type_day == 'Afspraak':
        number = st.text_input("Telefoonnummer*", placeholder="Voer hier uw nummer in ...")
        buurt = st.selectbox("Uit welke buurt komt u? (voor statistieken doeleinden)", buurt_choice)
        expertise = st.selectbox("Welke ervaring heeft u met fietsen?", expertise_choice)
        type_bike = st.selectbox("Wat voor fiets wilt u repareren?", type_bikes)
        materiaal = st.multiselect("Reparatie te doen (Meer opties mogelijk)", materiaal_choice)
        opmerking = st.text_input("", placeholder="Stuur een bericht, vraag, enz ...", label_visibility="collapsed")

    else:  # Vrije dag
        placeholder = st.empty()
        password = placeholder.text_input(
            "Password", None, label_visibility='collapsed',
            placeholder="schrijf hier uw wachtwoord ..."
        )

        if password == 'fietskliniek':
            placeholder.empty()
            number = buurt = expertise = type_bike = "-"
            materiaal = "-"
            opmerking = type_day
        else:
            st.error("Verkeerd wachtwoord ...")
            st.stop()

    # -----------------------------
    # FOOTNOTE
    # -----------------------------
    st.markdown("_*Verplichte velden_*")
    st.markdown(":orange-background[_Persoonlijke data wordt niet opgeslagen, alleen gebruikt voor administratieve doeleinden van de gemaakte afspraak_]")

    "---"

    # -----------------------------
    # SUBMIT BUTTON
    # -----------------------------
    submitted = st.button(":red[**Gegevens opslaan**]")

    if submitted:
        df = df_old

        # Existing bookings
        df_filter = df[(df["Date"] == str(date)) & (df["Time shift"] == time_shift)]
        df_control = df[(df["Date"] == str(date)) &
                        (df["Time shift"] == time_shift) &
                        (df["e_mail"] == e_mail)]

        len_1 = len(df_filter)
        len_control = len(df_control)

        # Required fields
        if not name or not e_mail or not number:
            st.warning("Vul de verplichte velden in", icon="⚠️")
            st.stop()

        # Prevent same-day booking
        if (dt.strptime(str(date), "%Y-%m-%d").date() - dt.today().date()).days == 0:
            st.warning("Helaas kunt u geen afspraak op dezelfde dag boeken", icon="⚠️")
            st.stop()

        # Prevent duplicate booking
        if len_control > 0:
            st.warning("Er is al een afspraak op deze datum en tijd met dezelfde email", icon="⚠️")
            st.stop()

        # Availability checks
        if not is_day_available(day_en):
            st.warning(f"Op {day_nl} is het niet mogelijk een afspraak te maken.", icon="⚠️")
            st.stop()

        if not is_time_available(day_en, time_shift):
            st.warning("Deze tijdsverschuiving is niet beschikbaar op deze dag.", icon="⚠️")
            st.stop()

        if is_slot_full(day_en, time_shift, len_1):
            st.warning("Deze tijdsverschuiving is al vol. Kies een andere.", icon="⚠️")
            st.stop()

        # -----------------------------
        # SAVE BOOKING
        # -----------------------------
        try:
            email_sent = False
            
            if membership == "ik heb een Stadspas":
                email_sent = mail(e_mail, name, str(date), time_shift, PAYMENT_LINK_STADPASS, membership_number)
            else:
                email_sent = mail(e_mail, name, str(date), time_shift, PAYMENT_LINK_NO_STADPASS, membership_number)
            
            if not email_sent:
                st.error("Het e-mailadres bestaat niet of kan geen mail ontvangen. Controleer het e-mailadres.")
                st.stop()
            
            # Email was sent → now save the booking
            insert_period(
                membership, str(date), day_en, week, time_shift, name, e_mail, number,
                buurt, expertise, type_bike, materiaal, opmerking,
                membership_number if membership == "ik heb een Stadspas" else None
            )


        except Exception:
            st.error("Er ging iets mis bij het opslaan van de afspraak.")
            st.stop()

        # -----------------------------
        # SUCCESS MESSAGE
        # -----------------------------
        # if type_day == "Vrije dag":
        #     st.success("🏖️🏖️ Je hebt een dag vrij geboekt! 🏖️🏖️")
        # else:
        #     st.success(
        #         "🚲 Je afspraak is ontvangen! "
        #         "Controleer je e-mail — daar vind je de link om de betaling te voltooien en je reservering veilig te stellen. 🚲"
        #     )

        if type_day == "Vrije dag":
            st.success("🏖️🏖️ Je hebt een dag vrij geboekt! 🏖️🏖️")
        else:
            appointment_dialog(
                membership, str(date), day_en, week, time_shift, name, e_mail, number,
                buurt, expertise, type_bike, materiaal, opmerking, membership_number
            )




##### --- drop appointment ---
if selected == "Afspraak afzeggen":
    image = '292366152_369803905279628_8461882568456452789_n.jpg'
    st.image(image)

    with st.form("cancel_form", clear_on_submit=False):

        # Datum + dag
        date_obj = st.date_input("Datum")
        date = str(date_obj)
        day_en = date_obj.strftime("%A")

        # Tijdverschuivingen uit SCHEDULE
        available_shifts = SCHEDULE.get(day_en, {}).keys()
        if not available_shifts:
            st.warning("Op deze dag zijn geen afspraken geregistreerd of beschikbaar.")
            st.stop()

        time_shift = st.selectbox("Tijdsverschuiving", list(available_shifts))
        e_mail = st.text_input("", placeholder="Voer hier uw e-mailadres in ...")

        "---"

        submitted = st.form_submit_button("Afspraak annuleren")
        if submitted:
            if not e_mail:
                st.warning('Schrijf alstublieft uw e-mail', icon="⚠️")
                st.stop()

            df = conn.read(ttl=0, worksheet="Data")
            df_filter = df[
                (df["Date"] == date) &
                (df["Time shift"] == time_shift) &
                (df["e_mail"] == e_mail)
            ]

            if len(df_filter) > 0:
                df_drop = df[~df.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
                conn.update(worksheet='Data', data=df_drop)
                cancelpop()
            else:
                st.warning('Er is geen afspraak op dit e-mailadres voor deze datum en tijd', icon="⚠️")



  
