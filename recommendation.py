import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
try:
     movies = pd.read_csv('imdbmovies.csv')
except FileNotFoundError:
    raise FileNotFoundError("The dataset 'imdbmovies.xlsx' was not found. Ensure the file is in the correct location.")
except Exception as e:
    raise Exception(f"An error occurred while loading the dataset: {e}")

# Combine relevant features into a single column
def combine_features(row):
    return f"{row.get('Movie_Genre', '')} {row.get('Movie_Cast', '')} {row.get('All_Movie_Info', '')}"

# Preprocess data
required_columns = ['Movie_Name', 'Movie_Genre', 'Movie_Cast', 'All_Movie_Info']
for feature in required_columns[1:]:  # Exclude 'Movie_Name'
    if feature in movies.columns:
        movies[feature] = movies[feature].fillna('')  # Handle missing values
    else:
        movies[feature] = ''  # Add missing columns with empty values

if 'Movie_Name' not in movies.columns:
    raise KeyError("'Movie_Name' column is missing in the dataset. Ensure the dataset has a 'Movie_Name' column.")

movies['combined_features'] = movies.apply(combine_features, axis=1)

# Vectorize the combined features
cv = CountVectorizer()
feature_vectors = cv.fit_transform(movies['combined_features'])

# Compute similarity matrix
similarity_matrix = cosine_similarity(feature_vectors)

# Recommendation function
def recommend(movie_title):
    try:
        # Find the movie index
        idx = movies[movies['Movie_Name'].str.contains(movie_title, case=False, na=False)].index[0]
        similarity_scores = list(enumerate(similarity_matrix[idx]))
        sorted_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommendations = [movies.iloc[i[0]]['Movie_Name'] for i in sorted_movies[1:6]]  # Top 5 recommendations
        return recommendations
    except IndexError:
        return ["Movie not found in the dataset."]
    except Exception as e:
        return [f"An error occurred: {e}"]
