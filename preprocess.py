
import pandas as pd
import ast
import os

# Load original Kaggle dataset
movies =pd.read_csv("C:\\Users\\ASUS\\Downloads\\movies data set\\tmdb_5000_movies.csv")

print("Original Dataset Loaded Successfully!")
print("Original Dataset Shape:", movies.shape)


# Select required columns
movies = movies[[
    "id",
    "title",
    "genres",
    "overview",
    "release_date",
    "vote_average",
    "vote_count",
    "popularity"
]]


# Remove rows with missing movie names or genres
movies = movies.dropna(subset=["title", "genres"])


# Function to extract genre names
def get_genres(value):

    genre_list = ast.literal_eval(value)

    names = []

    for genre in genre_list:
        names.append(genre["name"])

    return ", ".join(names)


# Convert genres into readable format
movies["genres"] = movies["genres"].apply(get_genres)


# Fill missing movie descriptions
movies["overview"] = movies["overview"].fillna("")


# Extract release year
movies["release_year"] = pd.to_datetime(
    movies["release_date"],
    errors="coerce"
).dt.year


# Remove original release date column
movies = movies.drop(columns=["release_date"])


# Create data folder if it does not exist
os.makedirs("data", exist_ok=True)


# Save cleaned dataset
movies.to_csv("data/cleaned_movies.csv", index=False)


# Display final results
print("\nData Preprocessing Completed!")

print("\nCleaned Dataset:")
print(movies.head())

print("\nCleaned Dataset Shape:")
print(movies.shape)

print("\nMissing Values:")
print(movies.isnull().sum())

print("\nDuplicate Records:")
print(movies.duplicated().sum())

print("\nCleaned Dataset Saved Successfully!")
