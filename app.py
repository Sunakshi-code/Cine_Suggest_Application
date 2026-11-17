
import streamlit as st

from movie_api import (
    get_movie_genres,
    get_popular_movies,
    discover_movies,
    search_movies,
    get_movie_details,
    get_movie_trailer
)

from recommender import recommend_movies
from database import create_tables, register_user, login_user

from user_preferences import (
    initialize_preferences,
    save_genres,
    like_movie,
    dislike_movie,
    rate_movie
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CineSuggest | Movie Discovery",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)




# ==========================================
# USER AUTHENTICATION
# ==========================================

create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None


if not st.session_state.logged_in:

    st.title("🎬 Welcome to CineSuggest")
    st.write("Login or create an account to discover movies.")

    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )

    with login_tab:

        st.subheader("Login to Your Account")

        with st.form("login_form"):

            username = st.text_input("Username")
            password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if login_button:

                user_id = login_user(username, password)

                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()
                    st.session_state.user_id = user_id

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

    with register_tab:

        st.subheader("Create Your Account")

        with st.form("register_form"):

            new_username = st.text_input("Choose Username")

            new_password = st.text_input(
                "Choose Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            register_button = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if register_button:

                if new_password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    success, message = register_user(
                        new_username,
                        new_password
                    )

                    if success:
                        st.success(message)
                        st.info("Now login using your new account.")
                    else:
                        st.error(message)

    st.stop()


# Initialize preferences only after login
initialize_preferences()


# ==========================================
# 2. SESSION STATE
# ==========================================

defaults = {
    "discovered_movies": [],
    "recommendations": [],
    "popular_movies": [],
    "search_results": [],
    "popular_loaded": False,
    "last_industry": "All Industries",
    "selected_movie_id": None,
    "page_navigation": "Home"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 3. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #101019;
    color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background-color: #181824;
}

.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #FFFFFF;
}

.subtitle {
    font-size: 16px;
    color: #A5A5B5;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 20px;
}

.movie-name {
    font-size: 17px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 8px;
}

.stButton button {
    border-radius: 8px;
    font-weight: 600;
}

/* Like button - Green */
div[class*="st-key-liked_active"] button {
    background-color: #16A34A !important;
    color: white !important;
    border: 1px solid #16A34A !important;
}

/* Dislike button - Red */
div[class*="st-key-disliked_active"] button {
    background-color: #DC2626 !important;
    color: white !important;
    border: 1px solid #DC2626 !important;
}

/* Saved rating - Blue */
div[class*="st-key-rating_saved"] button {
    background-color: #2563EB !important;
    color: white !important;
    border: 1px solid #2563EB !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. LOAD MOVIE GENRES
# ==========================================

try:
    genres = get_movie_genres()

    genre_map = {
        genre["id"]: genre["name"]
        for genre in genres
    }

except Exception as error:
    st.error(f"Unable to load movie genres: {error}")
    genres = []
    genre_map = {}


# ==========================================
# 5. NAVIGATION CALLBACKS
# ==========================================

def open_movie_details(movie_id):
    st.session_state.selected_movie_id = movie_id
    st.session_state.page_navigation = "Movie Details"


def go_to_page(page_name):
    st.session_state.page_navigation = page_name


# ==========================================
# 6. HELPER FUNCTIONS
# ==========================================

def prepare_movies(movies):

    prepared = []

    for movie in movies:

        movie = movie.copy()

        movie["genres"] = [
            genre_map[genre_id]
            for genre_id in movie.get("genre_ids", [])
            if genre_id in genre_map
        ]

        prepared.append(movie)

    return prepared


def show_movie_cards(movies, section_name):

    if not movies:
        st.info("No movies available.")
        return

    columns = st.columns(4)

    for index, movie in enumerate(movies):

        with columns[index % 4]:

            poster = movie.get("poster_path")

            if poster:

                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster
                )

                st.image(
                    poster_url,
                    use_container_width=True
                )

            else:
                st.info("Poster unavailable")

            title = movie.get("title", "Unknown Movie")

            st.markdown(
                f'<div class="movie-name">{title}</div>',
                unsafe_allow_html=True
            )

            release_date = movie.get("release_date") or "N/A"

            year = (
                release_date[:4]
                if release_date != "N/A"
                else "N/A"
            )

            rating = movie.get("vote_average", 0) or 0

            st.caption(
                f"📅 {year}  |  ⭐ {rating:.1f}/10"
            )

            if movie.get("genres"):
                st.caption(
                    " | ".join(movie["genres"])
                )

            with st.expander("Quick Overview"):
                st.write(
                    movie.get("overview")
                    or "Description unavailable."
                )

                if "recommendation_score" in movie:
                    st.write(
                        f"Match Score: "
                        f"{movie['recommendation_score']}%"
                    )

            movie_id = movie.get("id")

            if movie_id is None:
                continue

            # NEW: Movie Details Button
            st.button(
                "🎬 View Details",
                key=f"{section_name}_details_{movie_id}",
                use_container_width=True,
                on_click=open_movie_details,
                args=(movie_id,)
            )

            
            # Check existing feedback
            is_liked = title in st.session_state.liked_movies
            is_disliked = title in st.session_state.disliked_movies

            # LIKE BUTTON
            with st.container(
                key=(
                    f"liked_active_{section_name}_{movie_id}"
                    if is_liked else
                    f"liked_inactive_{section_name}_{movie_id}"
                )
            ):
                st.button(
                    "❤️ Liked" if is_liked else "❤️ Like",
                    key=f"{section_name}_like_{movie_id}",
                    use_container_width=True,
                    on_click=like_movie,
                    args=(title,),
                    type="primary" if is_liked else "secondary"
                )

            # DISLIKE BUTTON
            with st.container(
                key=(
                    f"disliked_active_{section_name}_{movie_id}"
                    if is_disliked else
                    f"disliked_inactive_{section_name}_{movie_id}"
                )
            ):
                st.button(
                    "👎 Disliked" if is_disliked else "👎 Dislike",
                    key=f"{section_name}_dislike_{movie_id}",
                    use_container_width=True,
                    on_click=dislike_movie,
                    args=(title,),
                    type="primary" if is_disliked else "secondary"
                )

            # RATING SELECTOR
            rating_value = st.selectbox(
                "Your Rating",
                [1, 2, 3, 4, 5],
                key=f"{section_name}_rating_{movie_id}"
            )

            is_rating_saved = (
                st.session_state.movie_ratings.get(title)
                == rating_value
            )

            # SAVE RATING BUTTON
            with st.container(
                key=(
                    f"rating_saved_{section_name}_{movie_id}"
                    if is_rating_saved else
                    f"rating_unsaved_{section_name}_{movie_id}"
                )
            ):
                st.button(
                    "✓ Rating Saved" if is_rating_saved
                    else "⭐ Save Rating",
                    key=f"{section_name}_save_{movie_id}",
                    use_container_width=True,
                    on_click=rate_movie,
                    args=(title, rating_value),
                    type="primary" if is_rating_saved else "secondary"
                )



def update_recommendations():

    movies = st.session_state.discovered_movies

    if not movies:
        st.session_state.recommendations = []
        return

    st.session_state.recommendations = recommend_movies(
        movies=movies,
        preferred_genres=st.session_state.preferred_genres,
        liked_movies=st.session_state.liked_movies,
        disliked_movies=st.session_state.disliked_movies,
        ratings=st.session_state.movie_ratings,
        top_n=12
    )


# ==========================================
# 7. MOVIE DETAILS PAGE
# ==========================================

def show_movie_details(movie_id):
    """Display complete details, trailer, and feedback for one movie."""
    try:
        with st.spinner("Loading movie details..."):
            movie = get_movie_details(movie_id)

        st.title(movie.get("title", "Movie Details"))
        st.divider()

        col1, col2 = st.columns([1, 2])

        with col1:
            poster_path = movie.get("poster_path")
            if poster_path:
                poster_url = (
                    "https://image.tmdb.org/t/p/w500" + poster_path
                )
                st.image(poster_url, use_container_width=True)
            else:
                st.info("Poster not available.")

        with col2:
            st.subheader("Movie Information")
            st.write("**Original Title:**", movie.get("original_title", "N/A"))
            st.write("**Release Date:**", movie.get("release_date") or "N/A")
            st.write(
                "**TMDB Rating:** ⭐",
                f"{movie.get('vote_average', 0):.1f}/10"
            )
            st.write(
                "**Runtime:**",
                f"{movie.get('runtime')} minutes"
                if movie.get("runtime") else "N/A"
            )

            movie_genres = [
                genre.get("name", "")
                for genre in movie.get("genres", [])
                if genre.get("name")
            ]
            st.write(
                "**Genres:**",
                ", ".join(movie_genres) if movie_genres else "N/A"
            )
            st.write(
                "**Original Language:**",
                movie.get("original_language", "N/A").upper()
            )
            st.write("**Status:**", movie.get("status", "N/A"))

        st.divider()
        st.subheader("📖 Movie Overview")
        st.write(movie.get("overview") or "No overview available.")

        # Trailer lookup must stay inside this function because movie_id
        # is passed into show_movie_details(movie_id).
        st.divider()
        st.subheader("▶️ Watch Movie Trailer")
        try:
            with st.spinner("Finding movie trailer..."):
                trailer_url = get_movie_trailer(movie_id)

            if trailer_url:
                st.video(trailer_url)
            else:
                st.info(
                    "Sorry! No YouTube trailer is available for this movie."
                )
        except Exception as trailer_error:
            st.warning(f"Unable to load trailer: {trailer_error}")

        # Movie feedback
        st.divider()
        st.subheader("Your Feedback")

        title = movie.get("title", "Unknown Movie")

        is_liked = title in st.session_state.liked_movies
        is_disliked = title in st.session_state.disliked_movies

        feedback_col1, feedback_col2 = st.columns(2)

        with feedback_col1:
            with st.container(
                key=(
                    f"liked_active_details_{movie_id}"
                    if is_liked else f"liked_inactive_details_{movie_id}"
                )
            ):
                st.button(
                    "❤️ Liked" if is_liked else "❤️ Like Movie",
                    key=f"details_like_{movie_id}",
                    use_container_width=True,
                    on_click=like_movie,
                    args=(title,),
                    type="primary" if is_liked else "secondary"
                )

        with feedback_col2:
            with st.container(
                key=(
                    f"disliked_active_details_{movie_id}"
                    if is_disliked else f"disliked_inactive_details_{movie_id}"
                )
            ):
                st.button(
                    "👎 Disliked" if is_disliked else "👎 Dislike Movie",
                    key=f"details_dislike_{movie_id}",
                    use_container_width=True,
                    on_click=dislike_movie,
                    args=(title,),
                    type="primary" if is_disliked else "secondary"
                )

        rating_value = st.selectbox(
            "Rate this movie",
            [1, 2, 3, 4, 5],
            key=f"details_rating_{movie_id}"
        )

        is_rating_saved = (
            st.session_state.movie_ratings.get(title)
            == rating_value
        )

        with st.container(
            key=(
                f"rating_saved_details_{movie_id}"
                if is_rating_saved else f"rating_unsaved_details_{movie_id}"
            )
        ):
            st.button(
                "✓ Rating Saved" if is_rating_saved
                else "⭐ Save My Rating",
                key=f"details_save_rating_{movie_id}",
                use_container_width=True,
                on_click=rate_movie,
                args=(title, rating_value),
                type="primary" if is_rating_saved else "secondary"
            )
    except Exception as error:
        st.error(f"Unable to load movie details: {error}")

# ==========================================
# 8. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🎬 CineSuggest")

st.sidebar.success(
    f"Welcome, {st.session_state.username}!"
)

if st.sidebar.button("Logout", use_container_width=True):

    st.session_state.clear()
    st.rerun()

st.sidebar.caption(
    "Your Personal Movie Companion"
)

navigation_options = [
    "Home",
    "Discover Movies",
    "For You",
    "Search Movies",
    "My Favorites",
    "Movie Details"
]

page = st.sidebar.radio(
    "Navigation",
    navigation_options,
    key="page_navigation"
)

st.sidebar.divider()

st.sidebar.subheader("Your Activity")

st.sidebar.metric(
    "Liked Movies",
    len(st.session_state.liked_movies)
)

st.sidebar.metric(
    "Rated Movies",
    len(st.session_state.movie_ratings)
)


# ==========================================
# 9. HOME PAGE
# ==========================================

if page == "Home":

    st.markdown(
        '<div class="main-title">'
        'Welcome to CineSuggest 🍿'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Discover movies that match your interests.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader(
        "✨ Discover Your Next Favourite Movie"
    )

    st.write(
        "Explore Hollywood, Bollywood and South Indian cinema."
    )

    st.button(
        "Explore Movies",
        type="primary",
        on_click=go_to_page,
        args=("Discover Movies",)
    )

    st.markdown(
        '<div class="section-title">'
        '🔥 Popular Movies'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.popular_loaded:

        try:

            with st.spinner("Loading popular movies..."):

                popular = get_popular_movies()

                st.session_state.popular_movies = (
                    prepare_movies(popular)
                )

                st.session_state.popular_loaded = True

        except Exception as error:

            st.warning(
                f"Popular movies unavailable: {error}"
            )

    show_movie_cards(
        st.session_state.popular_movies,
        "home"
    )


# ==========================================
# 10. DISCOVER MOVIES
# ==========================================


elif page == "Discover Movies":

    st.title("🔎 Discover Movies")

    st.write(
        "Find movies using advanced search filters."
    )

    # Industry selection
    industry = st.selectbox(
        "Select Movie Industry",
        [
            "All Industries",
            "Hollywood",
            "Bollywood",
            "South Indian"
        ]
    )

    # Genre selection
    genre_options = {
        genre["name"]: genre["id"]
        for genre in genres
    }

    selected_genres = st.multiselect(
        "Select Genres",
        list(genre_options.keys()),
        default=[
            genre for genre in st.session_state.preferred_genres
            if genre in genre_options
        ]
    )

    # Release year
    current_year = 2026

    release_year = st.selectbox(
        "Release Year",
        ["Any Year"] + list(
            range(current_year, 1979, -1)
        )
    )

    if release_year == "Any Year":
        release_year = None

    # Minimum rating
    min_rating = st.slider(
        "Minimum TMDB Rating",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5
    )

    if min_rating == 0:
        min_rating = None

    # Sorting
    sort_options = {
        "Popularity": "popularity.desc",
        "Highest Rating": "vote_average.desc",
        "Latest Releases": "primary_release_date.desc"
    }

    selected_sort = st.selectbox(
        "Sort Movies By",
        list(sort_options.keys())
    )

    if st.button(
        "🍿 Discover Movies",
        type="primary",
        use_container_width=True
    ):

        genre_ids = [
            genre_options[genre]
            for genre in selected_genres
        ]

        try:

            with st.spinner("Finding movies for you..."):

                movies = discover_movies(
                    industry=industry,
                    genre_ids=genre_ids,
                    release_year=release_year,
                    min_rating=min_rating,
                    sort_by=sort_options[selected_sort]
                )

                movies = prepare_movies(movies)

                st.session_state.discovered_movies = movies

                st.session_state.last_industry = industry

                save_genres(selected_genres)

                update_recommendations()

        except Exception as error:

            st.error(
                f"Unable to discover movies: {error}"
            )

    st.divider()

    st.subheader("🎥 Movie Results")

    show_movie_cards(
        st.session_state.discovered_movies,
        "discover"
    )


# ==========================================
# 11. PERSONALIZED RECOMMENDATIONS
# ==========================================

elif page == "For You":

    st.title("❤️ Movies Picked For You")

    st.write(
        "Recommendations based on your preferences "
        "and movie feedback."
    )

    update_recommendations()

    recommendations = st.session_state.recommendations

    if recommendations:

        show_movie_cards(
            recommendations,
            "recommend"
        )

    else:

        st.info(
            "Discover movies first and share your feedback "
            "to generate personalized recommendations."
        )


# ==========================================
# 12. SEARCH MOVIES
# ==========================================

elif page == "Search Movies":

    st.title("🔍 Search Movies")

    query = st.text_input(
        "Search by movie name",
        placeholder="Example: Inception, Titanic, Dangal..."
    )

    if st.button(
        "Search",
        type="primary"
    ):

        if query.strip():

            try:

                with st.spinner("Searching movies..."):

                    results = search_movies(
                        query.strip()
                    )

                    st.session_state.search_results = (
                        prepare_movies(results)
                    )

            except Exception as error:

                st.error(
                    f"Search failed: {error}"
                )

        else:

            st.warning(
                "Please enter a movie name."
            )

    show_movie_cards(
        st.session_state.search_results,
        "search"
    )


# ==========================================
# 13. MY FAVORITES
# ==========================================

elif page == "My Favorites":

    st.title("❤️ My Favourite Movies")

    st.write(
        "Your liked movies and saved ratings."
    )

    favorite_titles = st.session_state.liked_movies

    all_movies = (
        st.session_state.popular_movies
        + st.session_state.discovered_movies
        + st.session_state.search_results
    )

    favorite_movies = []

    seen_ids = set()

    for movie in all_movies:

        if (
            movie.get("title") in favorite_titles
            and movie.get("id") not in seen_ids
        ):

            favorite_movies.append(movie)
            seen_ids.add(movie.get("id"))

    if favorite_movies:

        show_movie_cards(
            favorite_movies,
            "favorites"
        )

    elif favorite_titles:

        st.write(
            "Your liked movie titles:"
        )

        for title in favorite_titles:
            st.write(f"❤️ {title}")

    else:

        st.info(
            "You haven't liked any movies yet."
        )

    st.divider()

    st.subheader("⭐ Your Movie Ratings")

    if st.session_state.movie_ratings:

        for title, rating in (
            st.session_state.movie_ratings.items()
        ):

            st.write(
                f"**{title}** — {rating}/5 ⭐"
            )

    else:

        st.info(
            "You haven't rated any movies yet."
        )


# ==========================================
# 14. MOVIE DETAILS
# ==========================================

elif page == "Movie Details":

    st.title("🎬 Movie Details")

    st.button(
        "← Back to Discover Movies",
        on_click=go_to_page,
        args=("Discover Movies",)
    )

    selected_movie_id = st.session_state.selected_movie_id

    if selected_movie_id:

        show_movie_details(selected_movie_id)

    else:

        st.info(
            "Please select a movie using View Details."
        )


# ==========================================
# 15. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#999999;">
        <h4>CineSuggest 🎬</h4>
        Your Personal Movie Discovery Platform
        <br><br>
        Movie data provided by TMDB.
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "This product uses the TMDB API but is not endorsed "
    "or certified by TMDB."
)
