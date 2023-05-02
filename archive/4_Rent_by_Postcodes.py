import streamlit as st
import requests
import json
import pandas as pd
import numpy as np


st.title("Average Rent (2021) by Suburb")
st.header("")

postcode = st.number_input("Enter Postcode: ", value=2000, min_value=0,max_value=999999)

@st.cache_data
def get_abs_data():
    headers = {'Accept': 'application/vnd.sdmx.data+json'}
    params ={}
    url = "https://api.data.abs.gov.au/data/C21_G40_POA/"
    response = requests.get(url=url, headers=headers, params=params)
    return response

response = get_abs_data()

if response.status_code == 200:
    st.text("Data is ready")
    data = response.json()
    dic = data["data"]["dataSets"]["series"]
    print(dic)
    df = pd.DataFrame.from_dict(dic)
    st.dataframe(df)
    # print(data)
else:
    print(response.status_code)
    st.text("Error in processing data")