import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Load data
@st.cache_data
def load_data():
    movies = pd.read_csv('movies.csv')
    ratings = pd.read_csv('ratings.csv')
    return movies, ratings

movies, ratings = load_data()

# Data preprocessing
@st.cache_data
def preprocess_data(movies, ratings):
    merged_df = pd.merge(ratings, movies, left_on='movieId', right_on='id', how='inner')
    
    merged_df = merged_df.drop(['index', 'budget', 'homepage', 'id', 'keywords',
                                'original_language', 'original_title', 'overview', 
                                'popularity', 'production_companies', 'production_countries', 
                                'release_date', 'revenue', 'runtime', 'spoken_languages', 
                                'status', 'tagline', 'vote_average', 'vote_count', 'cast', 
                                'crew', 'director', 'timestamp'], axis=1)

    user_ratings = merged_df.pivot_table(index='userId', columns='title', values='rating')
    movie_genres = merged_df.groupby('title')['genres'].first().reset_index()
    
    user_ratings = user_ratings.dropna(thresh=2, axis=1).fillna(0)
    
    return user_ratings, movie_genres

user_ratings, movie_genres = preprocess_data(movies, ratings)

# Calculate item similarity
@st.cache_data
def calculate_similarity(user_ratings):
    return user_ratings.corr(method='pearson')

item_similarity_df = calculate_similarity(user_ratings)

# Function to get similar movies
def get_similar_movies(movie_name, user_rating):
    if movie_name not in item_similarity_df.index:
        st.warning(f"Movie '{movie_name}' not found in the similarity matrix.")
        return pd.Series()
    similar_score = item_similarity_df.loc[movie_name] * user_rating  
    return similar_score.sort_values(ascending=False)

# Sidebar
st.sidebar.title('Movie Recommender Settings')

# Dark mode
if st.sidebar.checkbox('Dark Mode'):
    st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Number of movies to rate
num_movies = st.sidebar.number_input('How many movies would you like to rate?', min_value=1, max_value=5, value=3)

# Genre filter
all_genres = set()
for genres in movie_genres['genres']:
    all_genres.update(genres.split('|'))
selected_genres = st.sidebar.multiselect('Filter recommendations by genre', list(all_genres))

# Exclude rated movies
exclude_rated = st.sidebar.checkbox('Exclude rated movies from recommendations', value=True)

# Main app
st.title('🎥 Movie Recommendation System 🍿')

# User input
st.header('✨ Enter Your Movie Preferences ✨')

user_preferences = []
for i in range(num_movies):
    col1, col2 = st.columns([3, 1])
    with col1:
        movie = st.selectbox(f'Select Movie {i+1}', options=movie_genres['title'].tolist(), key=f'movie_{i}')
    with col2:
        rating = st.slider(f'Rating ⭐', min_value=1, max_value=5, value=3, key=f'rating_{i}')
    user_preferences.append((movie, rating))

if st.button('🎬 Get Recommendations'):
    similar_movies = pd.DataFrame()
    input_genres = set()

    for movie, rating in user_preferences:
        similar = get_similar_movies(movie, rating)
        similar = similar.to_frame(name='score')
        similar['title'] = similar.index
        similar_movies = pd.concat([similar_movies, similar], ignore_index=True)
        
        movie_genre = movie_genres[movie_genres['title'] == movie]['genres'].iloc[0] if not movie_genres[movie_genres['title'] == movie].empty else ''
        input_genres.update(movie_genre.split('|'))

    recommended_movies = similar_movies.groupby('title')['score'].sum().sort_values(ascending=False)
    recommended_movies = recommended_movies.to_frame().reset_index()

    # Merge with movie_genres to get the genres
    recommended_movies_with_genres = recommended_movies.merge(movie_genres, on='title', how='left')

    # Filter by selected genres
    if selected_genres:
        recommended_movies_with_genres = recommended_movies_with_genres[
            recommended_movies_with_genres['genres'].apply(lambda x: any(genre in x for genre in selected_genres))
        ]

    # Exclude rated movies if option is selected
    if exclude_rated:
        rated_movies = [movie for movie, _ in user_preferences]
        recommended_movies_with_genres = recommended_movies_with_genres[~recommended_movies_with_genres['title'].isin(rated_movies)]

    # Reorder and format
    recommended_movies_with_genres = recommended_movies_with_genres[['title', 'genres', 'score']]
    recommended_movies_with_genres['score'] = recommended_movies_with_genres['score'].round(2)

    st.subheader('🎥 Your Personalized Movie Recommendations 🎬')
    st.write("Based on your preferences, here are some similar movies you might enjoy:")

    # Display recommendations with reasons
    for i, (_, row) in enumerate(recommended_movies_with_genres.head(10).iterrows()):
        st.write(f"🎬 **{i+1}. {row['title']}**")
        st.write(f"   **Why you might like it:** This movie belongs to the **{row['genres']}** genre(s), which is similar to your preferences.")
        st.write(f"   **Recommendation Score:** {row['score']}")
        st.write("---")

    st.write("We hope you find your next favorite movie in this list! 🍿 Enjoy watching!")

st.info('Note: This recommendation system uses collaborative filtering based on user ratings and genre matching to suggest movies similar to your preferences.')

# Custom footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #F0F2F6;  /* Light background color */
    color: #333333;  /* Dark text color */
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #DDDDDD; /* Light border to separate it from the content */
}
</style>
<div class="footer">
    <p>Developed with ❤️ by Habeeb</p>
</div>
""", unsafe_allow_html=True)
