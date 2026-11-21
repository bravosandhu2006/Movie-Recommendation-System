
import streamlit as st
import requests

# Application heading
st.title("TMDB API Connection Test")

# Get API token from secrets.toml
token = st.secrets["TMDB_ACCESS_TOKEN"]

# TMDB movie details URL
url = "https://api.themoviedb.org/3/movie/19995"

# Request headers
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + token
}

# Send API request
response = requests.get(url, headers=headers, timeout=20)

# Check API response
if response.status_code == 200:

    data = response.json()

    st.success("TMDB API Connected Successfully!")

    st.subheader(data["title"])

    st.write("Movie Rating:", data["vote_average"])

    st.write("Release Date:", data["release_date"])

    # Get movie poster
    poster = data.get("poster_path")

    if poster:

        image_url = "https://image.tmdb.org/t/p/w500" + poster

        st.image(image_url, width=250)

else:

    st.error("API connection failed.")

    st.write("Status Code:", response.status_code)
