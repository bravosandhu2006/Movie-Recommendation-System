
import pandas as pd

# Load cleaned movie dataset
movies = pd.read_csv("data/cleaned_movies.csv")


# Function to recommend similar movies
def recommend_movies(selected_movie):

    # Find the selected movie
    selected = movies[
        movies["title"].str.lower() == selected_movie.lower()
    ]

    # Check whether movie exists
    if len(selected) == 0:
        return pd.DataFrame()

    # Get genres of selected movie
    selected_genre = selected.iloc[0]["genres"]

    # Check if selected movie has genres
    if pd.isna(selected_genre) or selected_genre == "":
        return pd.DataFrame()

    selected_genres = selected_genre.split(", ")

    recommendations = []

    # Compare with all other movies
    for index, movie in movies.iterrows():

        # Do not recommend the same movie
        if index != selected.index[0]:

            # Skip movies with missing genres
            if pd.isna(movie["genres"]) or movie["genres"] == "":
                continue

            movie_genres = movie["genres"].split(", ")

            score = 0

            # Compare genres
            for genre in movie_genres:

                if genre in selected_genres:
                    score = score + 1

            # Store movies with matching genres
            if score > 0:
                recommendations.append({
    "id": movie["id"],
    "title": movie["title"],
    "genres": movie["genres"],
    "rating": movie["vote_average"],
    "year": movie["release_year"],
    "matching_score": score
})
                  
    # Convert recommendations into DataFrame
    result = pd.DataFrame(recommendations)

    # Sort recommendations
    if len(result) > 0:

        result = result.sort_values(
            by=["matching_score", "rating"],
            ascending=[False, False]
        )

    # Return top 5 movies
    return result.head(5)


# Test recommendation system
if __name__ == "__main__":

    selected_movie = input("Enter a movie name: ")

    result = recommend_movies(selected_movie)

    if len(result) > 0:

        print("\nRecommended Movies:")

        print(result.to_string(index=False))

    else:

        print("Movie not found or no similar movies available.")
