import streamlit as st
import requests
import json


st.title("Checking Crime Rates by Suburb")
st.header("")

postcode = st.number_input("Enter Postcode: ", value=2000, min_value=0,max_value=999999)

@st.cache_data
def get_abs_data(postcode):
    base_url = "https://api.data.abs.gov.au"
    url = base_url + "/"
    headers = {}
    params ={}


    response = requests.get(url=url, headers=headers, params=params)
