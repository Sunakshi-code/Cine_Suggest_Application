
import streamlit as st

from database import (
    load_user_preferences,
    save_user_preferences
)


def save_preferences():
    user_id = st.session_state.get("user_id")

    if not user_id:
        return

    preferences = {
        "preferred_genres": st.session_state.preferred_genres,
        "liked_movies": st.session_state.liked_movies,
        "disliked_movies": st.session_state.disliked_movies,
        "movie_ratings": st.session_state.movie_ratings
    }

    save_user_preferences(user_id, preferences)


def initialize_preferences():
    user_id = st.session_state.get("user_id")

    if not user_id:
        return

    if st.session_state.get("preferences_user_id") == user_id:
        return

    saved = load_user_preferences(user_id)

    st.session_state.preferred_genres = saved["preferred_genres"]
    st.session_state.liked_movies = saved["liked_movies"]
    st.session_state.disliked_movies = saved["disliked_movies"]
    st.session_state.movie_ratings = saved["movie_ratings"]

    st.session_state.preferences_user_id = user_id


def save_genres(genres):
    st.session_state.preferred_genres = genres
    save_preferences()


def like_movie(title):
    if title not in st.session_state.liked_movies:
        st.session_state.liked_movies.append(title)

    if title in st.session_state.disliked_movies:
        st.session_state.disliked_movies.remove(title)

    save_preferences()


def dislike_movie(title):
    if title not in st.session_state.disliked_movies:
        st.session_state.disliked_movies.append(title)

    if title in st.session_state.liked_movies:
        st.session_state.liked_movies.remove(title)

    save_preferences()


def rate_movie(title, rating):
    st.session_state.movie_ratings[title] = rating
    save_preferences()
