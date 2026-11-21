
import streamlit as st
import pandas as pd
import requests

from recommendation import recommend_movies


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #111827;
    color: white;
}

h1, h2, h3, p, label {
    color: #F9FAFB !important;
}

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #A78BFA;
}

.subtitle {
    text-align: center;
    color: #D1D5DB;
    font-size: 18px;
}

.stButton button {
    background-color: #7C3AED;
    color: white;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    padding: 10px;
}

.stButton button:hover {
    background-color: #6D28D9;
    color: white;
}

.movie-card {
    background-color: #1F2937;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. TMDB API CONFIGURATION
# ==========================================

token = st.secrets["TMDB_ACCESS_TOKEN"]

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + token
}


# ==========================================
# 4. FUNCTION TO FETCH MOVIE POSTERS
# ==========================================

@st.cache_data(ttl=86400, show_spinner=False)
def get_movie_poster(movie_id, movie_title, access_token):

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + access_token
    }

    try:

        # First search using TMDB movie ID
        url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}"

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code == 200:

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:

                return "https://image.tmdb.org/t/p/w500" + poster_path

        # If poster is unavailable, search using movie title
        search_url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "query": movie_title
        }

        response = requests.get(
            search_url,
            headers=headers,
            params=params,
            timeout=15
        )

        if response.status_code == 200:

            results = response.json().get("results", [])
            for movie in results:
                poster_path = movie.get("poster_path")

                if poster_path:

                    return "https://image.tmdb.org/t/p/w500" + poster_path

    except (requests.RequestException, ValueError, TypeError):

        return None

    return None


# ==========================================
# 5. LOAD MOVIE DATASET
# ==========================================

movies = pd.read_csv("C:\\Users\\ASUS\\OneDrive\\Desktop\\Ai project\\data\\cleaned_movies.csv")


# ==========================================
# 6. APPLICATION HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🎬 Movie Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover movies similar to your favourites!'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 7. MOVIE SELECTION
# ==========================================

st.subheader("🍿 Choose Your Favourite Movie")

movie_names = movies["title"].dropna().tolist()

selected_movie = st.selectbox(
    "Select a movie:",
    movie_names
)


# ==========================================
# 8. RECOMMENDATION BUTTON
# ==========================================

if st.button("✨ Recommend Movies", use_container_width=True):

    with st.spinner("Finding the best movies for you..."):

        result = recommend_movies(selected_movie)

    if len(result) > 0:

        st.success("Here are your recommended movies!")

        st.subheader("🎥 Top 5 Recommended Movies")

        # Display recommendations in five columns
        columns = st.columns(5)

        for index, (column, (row_index, movie)) in enumerate(
            zip(columns, result.iterrows())
        ):

            with column:

                # Fetch movie poster
                poster_url = get_movie_poster(
                    movie["id"],
                    movie["title"],
                    token
                )

                # Display poster
                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info("Poster not available")

                # Movie title
                st.markdown(
                    f"**{movie['title']}**"
                )

                # Movie genres
                st.caption(
                    str(movie["genres"])
                )

                # Movie rating
                st.metric(
                    "⭐ Rating",
                    round(float(movie["rating"]), 1)
                )

                # Matching score
                st.metric(
                    "Matching Score",
                    int(movie["matching_score"])
                )

                # Release year
                if pd.notna(movie["year"]):

                    st.write(
                        "📅 Year:",
                        int(movie["year"])
                    )

    else:

        st.warning(
            "No similar movies found. Please select another movie."
        )


# ==========================================
# 9. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#9CA3AF;">
        🎬 Movie Recommendation System
        <br>
        Developed using Python, Pandas, Streamlit and TMDB API
        <br>
        Educational College Project
    </div>
    """,
    unsafe_allow_html=True
)
