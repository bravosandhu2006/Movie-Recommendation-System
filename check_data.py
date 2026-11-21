import pandas as pd

#load movie dataset
movies =pd.read_csv("C:\\Users\\ASUS\\Downloads\\movies data set\\tmdb_5000_movies.csv")

# Display First Five Records
print("First Five Movies:")
print(movies.head())

#Display total rows and columns
print("\nDataset Shape:")
print(movies.shape)

#Display column names
print("\nColumn Names:")
print(movies.columns)

#check Missing Values
print("\nMissing Values:")
print(movies.isnull().sum())

#Check duplicate records
print("\nDuplicate Records:")
print(movies.duplicated().sum())

#Display Important movie Details
print("\nMovies Details:")
print(movies[["title","genres","release_date","vote_average"]].head())
