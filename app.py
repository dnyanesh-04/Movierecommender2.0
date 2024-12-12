import streamlit as st
from recommendation import recommend
import pandas as pd
# Load dataset
try:
    movies = pd.read_excel('imdbmovies.xlsx', engine='openpyxl')
except FileNotFoundError:
    st.error("Dataset file not found. Please ensure 'imdbmovies.xlsx' is in the correct location.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")
    st.stop()

# Check for required columns
required_columns = ['Movie_Name', 'Movie_Poster_HD']
if not all(column in movies.columns for column in required_columns):
    st.error(f"The dataset must contain the following columns: {', '.join(required_columns)}")
    st.stop()

# Ensure all entries in 'Movie_Name' are strings
movies['Movie_Name'] = movies['Movie_Name'].astype(str)

# Remove specific movie from the dropdown list
if 'Movie_Name' in movies.columns:
    movies = movies[movies['Movie_Name'] != "(500) Days of Summer"]

# Get unique movie titles for the dropdown
movie_titles = movies['Movie_Name'].dropna().sort_values().unique()

# Styling for the UI
st.markdown("""
<style>
    .title {
        text-align: center;
        font-size: 2.5em;
        color:white;
        margin-top:-50px; /* Adds space below the title */
        margin-bottom:11px;
    }

    .subtitle {
        text-align: center;
        font-size: 1.4em;
        color:white;
        margin-bottom: 16px; /* Adds space below the subtitle */
    }

    .stButton button {
        background-color: purple !important;
        color: white!important;
        border-radius: 5px;
        margin-top: 24px;
    }

    .label {
        margin-bottom: 16px; /* Space below "Select a movie" text */
        color: white !important;
    }

    /* Movie card styles */
    .movie-card {
        width: 140px;
        margin: 10px;
        display: inline-block;
        text-align: center;
        border: 2px solid #1A237E; /* Border color */
        border-radius: 10px;
        overflow: hidden;
        background-color: gold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .movie-card:hover {
        transform: scale(1.05); /* Slightly enlarge the card */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* More intense shadow */
    }

    .movie-poster {
        width: 100%;
        height: auto;
        border-bottom: 2px solid #1A237E; /* Border between poster and text */
    }

    .movie-title {
        font-size: 1.2em;
        color:white;
        margin-top: 04px;
    }

   img.movie-poster {
    width: 150px;
    height: 230px;
    object-fit: cover;
    border-radius: 5px;
}

 @media (max-width: 768px) {
    .movie-card {
        width: 100%;
        margin-bottom: 20px; /* Adds space between rows */
    }
    img.movie-poster {
        width: 100%; /* Stretch image to card width */
    }
}

</style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown('<div class="title">🎥 Movie Recommendation System 🎥</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get personalized movie recommendations based on your favorite movies!</div>', unsafe_allow_html=True)

# Layout for input and button
col1, col2 = st.columns([8, 12])  # Adjust proportions as needed

with col1:
    selected_movie = st.selectbox("Select a movie:", options=["-- Select a movie --"] + list(movie_titles))

with col2:
    recommend_button = st.button("Recommend")

# Recommendation display logic
if recommend_button:
    if selected_movie and selected_movie != "-- Select a movie --":
        st.write(f"Selected Movie : {selected_movie}")  # Debugging output
        recommendations = recommend(selected_movie)
        if isinstance(recommendations, str):  # If recommend() returns an error message
            st.error(recommendations)
        elif not recommendations:  # If no recommendations are returned
            st.error(f"Sorry, no recommendations could be generated for **{selected_movie}**.")
        else:
            st.write(f"### Recommendations based on **{selected_movie}**:")

            # Create columns for displaying recommended movies side-by-side
            cols = st.columns(len(recommendations))
            for idx, movie in enumerate(recommendations):
                # Fetch movie details
                movie_details = movies[movies['Movie_Name'].str.contains(movie, case=False, na=False)]
                poster_url = (
                    movie_details.iloc[0].get('Movie_Poster_HD', 'https://dummyimage.com/150x230/000/fff&text=No+Image')
                    if not movie_details.empty else 'https://dummyimage.com/150x230/000/fff&text=No+Image'
                )
                
                # Display movie poster and title in respective column
                with cols[idx]:
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{poster_url}" alt="{movie}" class="movie-poster"/>
                            <div class="movie-title">{movie}</div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("Please select a valid movie from the dropdown.")

