import streamlit as st
import requests
import json



# Set up Streamlit page layout
st.set_page_config(
    page_title="PropertyTech",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define API endpoint and headers
API_ENDPOINT = "https://api.domain.com.au/v1/listings/residential/_search"
HEADERS = {
    "X-API-Key": "key_7bfd0069496455b7970e777462b54e1c",
    "Content-Type": "application/json",
}

# Define request payload
PAYLOAD = {
        # Sale, Rent, Share, Sold, NewHomes
        # "listingType": "Rent",
        "propertyTypes": [
            "House",
            "ApartmentUnitFlat",
            "Townhouse",
        ],
        "locations": [
            {
                "state": "NSW",
                "postCode": "2020",
                },
            # {"state": "VIC"},
            # {"state": "QLD"},
            # {"state": "SA"},
            # {"state": "WA"},
            # {"state": "TAS"},
            # {"state": "ACT"},
            # {"state": "NT"},
        ],
        "pageSize": 100,
    }

# Make API request
@st.cache_data
def get_data():
    response = requests.post(API_ENDPOINT, headers=HEADERS, json=PAYLOAD)
    return response

import re
def get_price(string):
    pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|\b\d+(?:\.\d+)?\b'
    numbers = re.findall(pattern, string)
    return [int(float(n.replace(',', ''))) for n in numbers]

response = get_data()
listings = []
if response.status_code == 200:
    # Extract listings from API response
    data = response.json()
    #print(len(data))
    for i in range(0,len(data)):
        try:
            if data[i]['type'] == "Project":
                listings += data[i]["listings"]
            elif data[i]['type'] == "PropertyListing":
                listings.append(data[i]["listing"])
        except Exception as e:
            print(e)
    # listings = response.json()[0]["listings"]

    
# Define Streamlit sidebar
st.sidebar.title("Property Filters")

property_types = [
    "Apartment",
    "Townhouse",
    "House",
    #"Land",
]

listing_type = st.sidebar.radio("Listing Type",options=('Buy','Rent','Sold'), label_visibility="collapsed")
property_type_filter = st.sidebar.multiselect("Property Type", property_types, default=property_types)
min_bedrooms = st.sidebar.slider("Minimum number of bedrooms", 0, 5, 0)
max_bedrooms = st.sidebar.slider("Maximum number of bedrooms", 0, 5, 5)
min_bathrooms = st.sidebar.slider("Minimum number of bathrooms", 0, 5, 0)
max_bathrooms = st.sidebar.slider("Maximum number of bathrooms", 0, 5, 5)






if listing_type == "Buy":
    listing_type = "Sale"
    st.title("Sydney Apartments for Sale")
    min_price = st.sidebar.slider("Minimum price ($)", 0, 3000000, 0, 100000)
    max_price = st.sidebar.slider("Maximum price ($)", 0, 3000000, 1000000, 100000)
elif listing_type == "Rent":
    st.title("Sydney Apartments for Rent")
    min_price = st.sidebar.slider("Minimum price ($)", 0, 5000, 0, 50)
    max_price = st.sidebar.slider("Maximum price ($)", 0, 5000, 1000, 50)
elif listing_type == "Sold":
    st.title("Sydney Apartments Sold")
    min_price = st.sidebar.slider("Minimum price ($)", 0, 3000000, 0, 100000)
    max_price = st.sidebar.slider("Maximum price ($)", 0, 3000000, 1000000, 100000)





# Filter listings based on user inputs
filtered_listings = []
# print(listings)
for listing in listings:
    try:
        bedrooms = int(listing["propertyDetails"]["bedrooms"])
        bathrooms = int(listing["propertyDetails"]["bathrooms"])
        price_range = get_price(listing['priceDetails']['displayPrice'])
        propertyType = listing["propertyDetails"]["propertyType"]
        listingType = listing["listingType"]
        if propertyType in "ApartmentUnitFlat":
            propertyType = "Apartment"

        if len(price_range) > 0:
            price_flag = True
            min_guided_price = price_range[0]
            max_guided_price = min_guided_price
            if len(price_range) > 1:
                max_guided_price = price_range[1]
        else:
            price_flag = False

        # Filter the listings based on the input provided by user
        if (
            (min_bedrooms <= bedrooms <= max_bedrooms)
            and (min_bathrooms <= bathrooms <= max_bathrooms)
            and (propertyType in property_type_filter)
            and (listingType == listing_type)
        ):
            if price_flag and (min_price <= min_guided_price) and (max_guided_price <= max_price): 
                filtered_listings.append(listing)
            elif not price_flag:
                filtered_listings.append(listing)

    except:
        json.dumps(listing, indent=2)
    

# Display filtered listings in Streamlit app
    
# function to grab data here, change based on tab. May need to be moved within each tab

st.write(f"Showing {len(filtered_listings)} of {len(listings)} listings.")
for listing in filtered_listings:
    st.write(f"## {listing['headline']}")
    st.write(f"**Type:** {listing['propertyDetails']['propertyType']}")
    st.write(f"**Address:** {listing['propertyDetails']['displayableAddress']}")
    st.write(f"**Bedrooms:** {listing['propertyDetails']['bedrooms']}")
    st.write(f"**Bathrooms:** {listing['propertyDetails']['bathrooms']}")
    st.write(f"**Price:** {listing['priceDetails'].get('displayPrice', 'Contact agent')}")
    propType = listing['propertyDetails']['propertyType']
    suburb = listing['propertyDetails']['suburb']
    state = listing['propertyDetails']['state']
    postcode = listing['propertyDetails']['postcode']
    id = listing['id']
    st.write("**URL:**",f"https://www.domain.com.au/{propType}-{suburb}-{state}-{postcode}-{id}".replace(" ","%20"))
    st.image(listing["media"][0]["url"], use_column_width=True)
    st.write("______________________________________________________________________")
