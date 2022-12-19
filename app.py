import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from deta import Deta
import pandas as pd
import altair as alt

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])

# Create a new database "example-db"
db = deta.Base("project_fietsklinik")
# # Define the drive to store the files.
# drive = deta.Drive("project_2_drive_1")

# -------------- FUNCTIONS --------------

def insert_period(date, species, n_specimens, comment, lat, lon, image_name=None):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"date": date, "time_shift": time_shift, "name": name, "e_mail": e_mail, "buurt": buurt, 
                   "werkzaamheedeb": werkzaamheedeb, "materiaal":materiaal, "opmerking":opmerking})


# -------------- SETTINGS --------------
page_title = "Fietsklinik"
page_icon = ":bike:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
time_shift_choice = ["14-16", "16-18", "18-20"]
buurt_choice = ["Centrum", "Oost", "West"]

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
    menu_title=None,
    options=["Make an appointment", "Cancel an appointment"],
    icons=["bi-journal-check", "bi-x-octagon-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS ---
if selected == "Make an appointment":
    with st.form("entry_form", clear_on_submit=True):

        date = st.date_input("Date")
        st.write(date)
        
        time_shift = st.selectbox("Time shift", time_shift, key="time_shift")
        name = st.text_input("", placeholder="Enter your name here ...")
        e_mail = st.text_input("", placeholder="Enter your e-mail here ...")
        buurt = st.selectbox("Buurt", buurt_choice, key="buurt_choice")
        materiaal = st.selectbox("Matiriaal", materiaal_choice, key="buurt_choice")
        opmerking = st.text_input("Opmerking", placeholder="Opmerking ...")
               
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            insert_period(period, sp, n, comment, lat, lon)
            st.success("You booked an appointment!")
            
# # --- PLOT PERIODS ---
# if selected == "Data Visualization":
#      with st.form("plot_form"):
    
#         # ---FILTER THE DATASET---
#         db_content = db.fetch().items
#         df = pd.DataFrame(db_content)
#         filter_multiselect = st.multiselect("Select a species", df["species"].unique().tolist(), default=df["species"].unique().tolist())

#         df_2 = df[df.species.isin(filter_multiselect)][["lat", "lon", "date", "species", "n_specimens", "comment"]]


#         # ---CREATE TABS ---
#         tab1, tab2 = st.tabs(["🗃 Data","📈 Chart & 🗺️ Map"])

#         with tab1:
#             # ---show dataframe---
#             st.dataframe(df_2,use_container_width=True)    

#             # ---CREATE A DOWNLOAD BOTTON ---
#             csv = df_2.to_csv().encode('utf-8')
#             st.download_button(
#                 label="Download data as CSV",
#                 data=csv,
#                 file_name='df.csv',
#                 mime='text/csv',
#             )


#         with tab2:
#         # ---CREATE THE PLOT---
#             source = df_2.groupby("species", as_index=False)['n_specimens'].sum()
#             plot_ = alt.Chart(source).mark_bar().encode(y='species', x='n_specimens',
#                                                     tooltip=['species', 'n_specimens'])
#             st.altair_chart(plot_, use_container_width=True)

#             # ---CREATE A DOWNLOAD BOTTON ---
#             fig = plot_.save("fig.html")     
#             with open("fig.html", "rb") as file:
#                 btn = st.download_button(
#                         label="Download image",
#                         data=file,
#                         file_name="fig.html",
#                       )

#             left, right = st.columns(2)

#             with left:
#                 m = folium.Map(location=[df_2["lat"].mean(),df_2["lon"].mean()])
#                 for row, columns in df_2.iterrows():
#                     folium.Marker(location=[columns["lat"],columns["lon"]]).add_to(m)
#                 output = st_folium(m)
#                 output


#             with right:
#                 img_name = df_2[(df_2.lat==output["last_object_clicked"]["lat"]) & (df_2.lon==output["last_object_clicked"]["lng"])]["image_name"].values[0]
#                 caption = df_2[(df_2.lat==output["last_object_clicked"]["lat"]) & (df_2.lon==output["last_object_clicked"]["lng"])]["comment"].values[0]
#                 img = drive.get(img_name).read()
#                 st.image(img, caption=caption)
        
        
     


         
