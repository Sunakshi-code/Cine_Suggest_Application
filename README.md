
# 🎬 CineSuggest – Personalized Movie Recommendation System

### Discover Movies. Explore Your Interests. Find Your Next Favorite.

CineSuggest is an interactive and personalized movie recommendation web application developed using **Python and Streamlit**. It allows users to explore movies across different film industries, discover content based on their interests, and receive personalized recommendations based on their preferences and feedback.

Powered by the **TMDB API**, CineSuggest dynamically retrieves movie information, including titles, posters, genres, ratings, release dates, descriptions, and available trailers.

The application combines **Content-Based Filtering, TF-IDF Vectorization, and Cosine Similarity** with user preference tracking to deliver a personalized movie discovery experience.

---

## 📌 Project Overview

Finding movies that match personal interests can be challenging when thousands of movies are available across different genres and industries.

CineSuggest solves this problem by providing a centralized movie discovery platform where users can:

- Explore movies from multiple film industries.
- Discover movies based on genres and personal interests.
- Search for specific movies.
- Apply advanced filters to refine movie results.
- View detailed movie information and trailers.
- Like or dislike movies.
- Rate movies based on their preferences.
- Receive personalized movie recommendations.
- Maintain individual user profiles and preferences.

Unlike traditional recommendation projects that depend entirely on static datasets, CineSuggest retrieves movie information dynamically from TMDB.

---

## ✨ Key Features

### 1. Live Movie Discovery
- Fetches live movie information through the TMDB API.
- Displays movie posters, titles, release years, ratings, and genres.
- Supports Hollywood, Bollywood, and South Indian movie discovery.
- Provides an interactive movie browsing experience.

### 2. Personalized Movie Recommendations
- Generates recommendations based on individual user preferences.
- Uses content-based filtering techniques.
- Analyzes similarities between movie information.
- Considers liked and highly rated movies.
- Reduces recommendations for movies similar to disliked content.
- Ranks suitable movies using recommendation scoring.

### 3. Advanced Movie Search & Filters
- Search movies by title.
- Explore movies by industry.
- Filter movies by genre.
- Filter movies by release year.
- Set minimum movie ratings.
- Sort results according to selected preferences.

### 4. Movie Details
Each movie has a dedicated details view containing:
- Movie title and poster.
- Release date and release year.
- Movie rating.
- Genre information.
- Movie overview and description.
- Additional movie information retrieved from TMDB.

### 5. Watch Movie Trailers
- Retrieves available movie trailers.
- Provides trailer access from the movie details section.
- Helps users preview movies before deciding what to watch.

### 6. Like & Dislike System
- Users can like movies they enjoy.
- Users can dislike movies that do not match their interests.
- Feedback is stored in individual user profiles.
- Liked and disliked preferences contribute to personalized recommendations.
- Interactive button states provide visual feedback.

### 7. Movie Rating System
- Allows users to rate movies on a scale of 1–5.
- Saves ratings to individual user profiles.
- Uses highly rated movies as positive preference signals.
- Helps improve recommendation relevance.

### 8. User Authentication
- Individual user registration.
- Login and logout functionality.
- Duplicate username prevention.
- Password confirmation during registration.
- Separate user profiles.

### 9. Persistent User Preferences
- Stores user preferences using SQLite.
- Maintains liked movies and disliked movies.
- Saves movie ratings.
- Stores preferred genres.
- Retains individual preferences between login sessions.

### 10. My Favorites
- Displays movies liked by the user.
- Provides quick access to saved movie preferences.
- Makes it easier to revisit favorite movies.

---

## 🧠 Recommendation System – How It Works

CineSuggest uses a **Content-Based Filtering** approach to generate personalized movie recommendations.

The recommendation engine analyzes movie information and user feedback to identify movies that are similar to the user's interests.

### Recommendation Workflow

**1. Movie Data Collection**

Movie information is retrieved dynamically from the TMDB API.

**2. Feature Preparation**

Movie information is transformed into textual features that can be compared by the recommendation engine.

**3. TF-IDF Vectorization**

TF-IDF (Term Frequency–Inverse Document Frequency) converts textual movie information into numerical vectors.

**4. Cosine Similarity**

Cosine similarity measures how closely two movie feature vectors are related.

**5. User Preference Analysis**

The system considers:
- Liked movies.
- Highly rated movies.
- Disliked movies.
- Similarity between movie content and user preferences.

**6. Recommendation Generation**

Movies are scored using similarity and preference signals. Suitable candidates are ranked and displayed as personalized recommendations.

### Recommendation Flow

```text
             TMDB API
                 |
                 v
             Movie Data
                 |
                 v
          Feature Preparation
                 |
                 v
           TF-IDF Vectorizer
                 |
                 v
          Cosine Similarity
                 |
                 v
         User Preferences
          /      |       \
       Liked   Highly   Disliked
       Movies   Rated    Movies
                Movies
                 |
                 v
       Recommendation Scoring
                 |
                 v
      Personalized Movie Results
```

---

## 🖥️ Application Modules

| Module | Functionality |
|---|---|
| Home | Displays the main movie discovery interface and popular movies |
| Discover Movies | Explore movies by industry, genre, year, rating, and sorting |
| For You | Displays personalized movie recommendations |
| Search Movies | Search for movies by title |
| My Favorites | Displays the user's liked movies |
| Movie Details | Shows detailed movie information and available trailers |
| User Authentication | Handles registration, login, and logout |
| User Preferences | Maintains individual genres, likes, dislikes, and ratings |

---

## 🔄 Application Workflow

1. A user registers or logs into CineSuggest.
2. The user explores movies from different industries.
3. Movie information is fetched from TMDB.
4. The user searches, filters, and views movie details.
5. The user likes, dislikes, or rates movies.
6. Individual preferences are saved in SQLite.
7. The recommendation engine analyzes movie similarities and feedback.
8. Personalized recommendations are generated.
9. The user can revisit favorite movies and continue discovering content.

---

## 🛠️ Technologies & Libraries

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web application interface |
| TMDB API | Live movie information and media data |
| SQLite | User profiles and preference storage |
| Pandas | Structured data handling |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and similarity calculations |
| TF-IDF | Text feature vectorization |
| Cosine Similarity | Movie similarity calculation |
| Requests | API communication |
| Python-dotenv | Environment variable management |

---

## 🗄️ Database Functionality

CineSuggest uses **SQLite** to maintain user-specific information.

The database contains two main tables:

### Users

Maintains account information such as:
- User ID
- Username
- Password hash
- Password salt
- Account creation information

### User Preferences

Maintains individual movie preferences such as:
- User ID
- Preferred genres
- Liked movies
- Disliked movies
- Movie ratings

This structure allows multiple users to maintain separate recommendation profiles.

---

## 🌟 What Makes CineSuggest Different?

- Uses live movie information instead of relying only on a static movie dataset.
- Supports movie discovery across multiple film industries.
- Combines movie similarity with individual user feedback.
- Maintains separate profiles for multiple users.
- Stores preferences and ratings persistently.
- Provides an integrated experience for searching, exploring, rating, and discovering movies.

---

## 🚀 Future Enhancements

Potential improvements for future versions include:

- Hybrid recommendation system combining content-based and collaborative filtering.
- More advanced recommendation algorithms.
- Watchlist functionality.
- Movie comparison feature.
- Advanced recommendation analytics.
- Improved recommendation explanations.
- Additional movie discovery categories.
- More interactive dashboard visualizations.

---

## 🎯 Project Objectives

- Develop a personalized movie recommendation application.
- Integrate external APIs for dynamic movie information.
- Implement content-based filtering using machine learning techniques.
- Understand TF-IDF and cosine similarity through practical implementation.
- Implement user authentication and persistent data storage.
- Build an interactive and user-friendly web application.
- Apply Python, API integration, machine learning, and database concepts in a real-world project.

---

## 👩‍💻 Project Information

| Details | Description |
|---|---|
| Project Name | CineSuggest – Movie Recommendation System |
| Project Type | Python-Based Web Application |
| Domain | Machine Learning, Recommendation Systems & Web Development |
| Framework | Streamlit |
| Data Source | TMDB API |
| Recommendation Technique | Content-Based Filtering |
| Database | SQLite |
| Language | Python |

---

### 🎬 CineSuggest

**Discover movies that match your interests and make every movie discovery more personal!** 🍿
