import streamlit as st
import json
import pandas as pd

# Load data
with open("data/station.json", "r") as f:
    stations_data = json.load(f)

with open("data/tourist_places.json", "r") as f:
    tourist_data = json.load(f)

stations = pd.DataFrame(stations_data["stations"])

# Custom styles
st.markdown(
    """
    <link rel="stylesheet" href="assets/style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .css-1aumxhk {
            background-color: #f7f9fc !important;
        }
        .stTitle {
            color: #0078D7;
        }
        .stSidebar {
            background-color: #ebf5ff !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("🚇 Delhi Metro Navigation App")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Choose an option:",
    ["Stations", "Nearby Tourist Places", "Calculate Fare", "Nearby Places"]
)

if option == "Stations":
    st.header("🔍 Search Metro Stations")
    st.dataframe(stations)

elif option == "Nearby Tourist Places":
    st.header("🌟 Tourist Places Near Metro Stations")
    station = st.selectbox("Select a station:", [s["station"] for s in tourist_data["places"]])
    places = next(item["places"] for item in tourist_data["places"] if item["station"] == station)
    st.write(f"Tourist places near **{station}**:")
    st.markdown(", ".join(f"**{place}**" for place in places))

elif option == "Calculate Fare":
    st.header("💸 Calculate Fare")
    start_station = st.selectbox("Start Station:", stations["name"])
    end_station = st.selectbox("End Station:", stations["name"])

    # Example: Using distance between stations as a simple calculation for fare
    start_index = stations[stations["name"] == start_station].index[0]
    end_index = stations[stations["name"] == end_station].index[0]
    distance = abs(start_index - end_index)
    fare = 10 + (distance * 5)  # Base fare + fare per station

    st.write(f"Estimated Fare from **{start_station}** to **{end_station}**: ₹{fare}")

elif option == "Nearby Places":
    st.header("📍 Find Nearby Places")
    selected_station = st.selectbox("Select a station to explore nearby:", stations["name"])
    # Example data for nearby places
    nearby_places = {
        "Rajiv Chowk": ["Connaught Place", "Palika Bazaar", "Janpath Market"],
        "Chandni Chowk": ["Red Fort", "Jama Masjid", "Paranthe Wali Gali"],
        "Saket": ["Select City Walk", "Qutub Minar", "Garden of Five Senses"],
        "Dwarka": ["Dada Dev Mandir", "Dwarka Sector 9 Market", "Pacific Mall Dwarka"],
        "New Delhi": ["Gurudwara Bangla Sahib", "Jantar Mantar", "Connaught Place"],
        "Karol Bagh": ["Ajmal Khan Road Market", "Karol Bagh Gaffar Market", "Jhandewalan Mandir"],
        "Hauz Khas": ["Hauz Khas Village", "Deer Park", "Hauz Khas Fort"],
        "AIIMS": ["Safdarjung Hospital", "Dilli Haat", "Lodhi Garden"]
    }

    if selected_station in nearby_places:
        st.write(f"Nearby places near **{selected_station}**:")
        st.markdown(", ".join(f"**{place}**" for place in nearby_places[selected_station]))
    else:
        st.write(f"No information available for **{selected_station}**.")
