import streamlit as st
import requests

# Set up the API URLs and your API key
LISTINGS_API_URL = "https://api.domain.com.au/v1/listings/residential/_search"
ME_API_URL = "https://api.domain.com.au/v1/me"
API_KEY = "key_7bfd0069496455b7970e777462b54e1c"

# Define the Streamlit app
def app():
    # Set the page title
    st.set_page_config(page_title="New Property Listings")

    # Test the connection to the /v1/me API endpoint
    headers = {"X-API-Key": f"{API_KEY}"}
    me_response = requests.get(ME_API_URL, headers=headers)
    if me_response.status_code != 200:
        st.error("Error: Unable to connect to the Domain.com.au API.")
        return

    # Define the API request payload
    payload = {
        "listingType": "Sale",
        "propertyTypes": [
            "House",
            "ApartmentUnitFlat",
            "Townhouse",
            "VacantLand",
            "NewApartments",
        ],
        "locations": [
            {"state": "NSW"},
            {"state": "VIC"},
            {"state": "QLD"},
            {"state": "SA"},
            {"state": "WA"},
            {"state": "TAS"},
            {"state": "ACT"},
            {"state": "NT"},
        ],
        "pageSize": 20,
        "pageNumber": 1,
    }

    # Make the API request to retrieve new property listings
    listings_response = requests.post(
        LISTINGS_API_URL, headers=headers, json=payload
    )

    # Check if the API request was successful
    if listings_response.status_code != 200:
        st.error("Error: Unable to retrieve new property listings.")
    else:
        # Parse the API response
        data = listings_response.json()

        st.write(data)
        # Display the new property listings in a table
        # st.write("## New Property Listings")
        # st.write(
        #     data["totalResults"],
        #     "new property listings found in Australia.",
        # )
        # listings = data.get("listings")
        # if listings:
        #     for listing in listings:
        #         st.write(
        #             f"{listing.get('propertyDetails', {}).get('address', {}).get('displayAddress')}: "
        #             f"${listing.get('priceDetails', {}).get('displayPrice')}"
        #         )

# Run the Streamlit app
if __name__ == "__main__":
    app()
