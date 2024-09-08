# 🎬 MovieMatch-CF

A personalized movie recommendation system using collaborative filtering. This app allows users to rate movies and get recommendations based on similar movies, genres, and preferences. Built with Streamlit, it provides an interactive and user-friendly experience.

## Features

- 🛠 **Collaborative Filtering**: Recommends movies based on users' ratings and similar movie preferences.
- 🎥 **Personalized Suggestions**: Users receive movie recommendations tailored to their taste.
- 📊 **Genre Filtering**: Allows filtering by movie genres to refine recommendations.
- 🌑 **Dark Mode Support**: Switch between light and dark mode for a better user experience.
- ✨ **Responsive Interface**: A clean, intuitive UI designed for easy navigation.
- ❤️ **Custom Footer**: Developed with love and a personal touch.

## Tech Stack

- **Streamlit**: For the web interface.
- **Pandas & Numpy**: For data handling and processing.
- **CSV Files**: Used to store movies and ratings data.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Adekunle-Habeeb/CF-MovieMatcher.git
    cd MovieMatch-CF
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:

    ```bash
    streamlit run app.py
    ```

## How to Use

1. **Rate Movies**: Select and rate a few movies from the provided list.
2. **Get Recommendations**: Click on "Get Recommendations" to receive a list of suggested movies tailored to your preferences.
3. **Filter by Genre**: Use the sidebar to filter your recommendations by genre.
4. **Dark Mode**: Toggle dark mode in the sidebar for a night-friendly experience.

## Data

The recommendation system uses two CSV files:
- **movies.csv**: Contains movie metadata such as title, genres, etc.
- **ratings.csv**: Contains user ratings for different movies.

## Example Output

After rating a few movies, the system will output a list of movie recommendations like:

```
1. The Shawshank Redemption
   Why you might like it: This movie is in the Drama genre(s), similar to your preferences.
   Recommendation Score: 4.85
---
2. Inception
   Why you might like it: This movie is in the Action|Sci-Fi genre(s), similar to your preferences.
   Recommendation Score: 4.75
---
```

## Future Features

- 🔍 **Search Functionality**: Allow users to search for specific movies.
- 📊 **More Data Sources**: Integrating additional data sources for better recommendations.
- ⭐ **Advanced Filtering**: Add filters for release year, director, and more.

## Contributing

Feel free to open an issue or pull request for any enhancements, bug fixes, or new features!
