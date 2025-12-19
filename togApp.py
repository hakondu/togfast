import streamlit as st
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import time

st.set_page_config(page_title="Train Delay Cost Calculator", layout="centered")

# Large dynamic number (dummy: current Unix time seconds)
current_unix = int(time.time())
st.markdown(
    f"<h1 style='text-align:center;font-size:72px;margin-top:-10px;'>{current_unix:,}</h1>",
    unsafe_allow_html=True
)
st.caption("Running total (dummy: current Unix timestamp)")

# Inputs
delay_minutes = st.number_input("How delayed is my train (minutes)", min_value=0, step=1, value=0)
fullness = st.selectbox("How full is the train", ["Not very", "Medium", "Full"])


# Map fullness to approximate passenger counts
fullness_map = {
    "Not very": 80,
    "Medium": 200,
    "Full": 400
}
COST_PER_PERSON_MINUTE_NOK = 5

passengers = fullness_map[fullness]
person_minutes = delay_minutes * passengers
cost = person_minutes * COST_PER_PERSON_MINUTE_NOK

st.subheader("Result")
st.write(f"My train is {delay_minutes} minutes delayed.")
st.write(
    f"This costs the society {cost:,.0f} NOK, and so far this year train delays has cost the society {current_unix:,.0f} NOK."
)

st.markdown("### Send til Samferdselsdepartementet (standard e-postklient)")
to_email = "hd@multiconsult.no"
subject = "Samfunnskostnad forsinket tog"
message_body = (
    f"Forsinkelsesrapport\n\n"
    f"Forsinkelse (min): {delay_minutes}\n"
    f"Antatt passasjerer: {passengers}\n"
    f"Person-minutter tapt: {person_minutes:,}\n"
    f"Kostnad (NOK): {cost:,.0f}\n"
    f"Akkumulert (dummy): {current_unix:,.0f} NOK\n"
    f"Generert: {datetime.now().isoformat(sep=' ', timespec='seconds')}\n"
)

edited_body = st.text_area("E-postinnhold (kan redigeres før sending)", message_body, height=220)

import urllib.parse
encoded_subject = urllib.parse.quote(subject)
encoded_body = urllib.parse.quote(edited_body)

mailto_link = f"mailto:{to_email}?subject={encoded_subject}&body={encoded_body}"
st.markdown(f"[Åpne e-postklient med tekst klar til sending]({mailto_link})")
st.caption("Klikk lenken for å åpne din standard e-postklient.")
