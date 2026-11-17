
import os
import requests
from dotenv import load_dotenv

# ==========================================
# 1. API CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


# ==========================================
# 2. COMMON API REQUEST FUNCTION
# ==========================================

def make_api_request(endpoint, params=None):
    """Send a request to the TMDB API."""

    if not API_KEY:
        raise ValueError(
            "TMDB API key not found. Check your .env file."
        )

    url = f"{BASE_URL}/{endpoint}"

    request_params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    if params:
        request_params.update(params)

    response = requests.get(
        url,
        params=request_params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ==========================================
# 3. GET MOVIE GENRES
# ==========================================

def get_movie_genres():
    """Get all available movie genres."""

    data = make_api_request("genre/movie/list")

    return data.get("genres", [])


# ==========================================
# 4. GET POPULAR MOVIES
# ==========================================

def get_popular_movies(page=1):
    """Get popular movies from TMDB."""

    data = make_api_request(
        "movie/popular",
        {"page": page}
    )

    return data.get("results", [])


# ==========================================
# 5. INDUSTRY FILTERS
# ==========================================

def get_industry_filters(industry):
    """Return language and country filters."""

    filters = {
        "Hollywood": {
            "with_original_language": "en",
            "with_origin_country": "US"
        },

        "Bollywood": {
            "with_original_language": "hi",
            "with_origin_country": "IN"
        },

        "South Indian": {
            "with_original_language": "ta|te|ml|kn",
            "with_origin_country": "IN"
        },

        "All Industries": {}
    }

    return filters.get(industry, {})


# ==========================================
# 6. DISCOVER MOVIES
# ==========================================

def discover_movies(
    industry="All Industries",
    genre_ids=None,
    page=1,
    release_year=None,
    min_rating=None,
    sort_by="popularity.desc"
):
    """Discover movies using advanced filters."""

    params = {
        "sort_by": sort_by,
        "include_adult": "false",
        "page": page
    }

    # Industry filter
    params.update(get_industry_filters(industry))

    # Genre filter
    if genre_ids:
        params["with_genres"] = "|".join(
            str(genre_id)
            for genre_id in genre_ids
        )

    # Release year filter
    if release_year:
        params["primary_release_date.gte"] = (
            f"{release_year}-01-01"
        )
        params["primary_release_date.lte"] = (
            f"{release_year}-12-31"
        )

    # Minimum TMDB rating
    if min_rating is not None:
        params["vote_average.gte"] = min_rating

    data = make_api_request(
        "discover/movie",
        params
    )

    return data.get("results", [])


# ==========================================
# 7. GET MOVIE DETAILS
# ==========================================

def get_movie_details(movie_id):
    """Get complete details of a movie."""

    if not movie_id:
        raise ValueError("Movie ID is required.")

    return make_api_request(
        f"movie/{movie_id}"
    )


# ==========================================
# 8. CONVERT GENRE IDs INTO NAMES
# ==========================================

def get_movie_genre_names(genre_ids):
    """Convert genre IDs into genre names."""

    if not genre_ids:
        return []

    genres = get_movie_genres()

    genre_map = {
        genre["id"]: genre["name"]
        for genre in genres
    }

    return [
        genre_map[genre_id]
        for genre_id in genre_ids
        if genre_id in genre_map
    ]


# ==========================================
# 9. SEARCH MOVIES
# ==========================================

def search_movies(query, page=1):
    """Search movies by title."""

    if not query or not query.strip():
        return []

    params = {
        "query": query.strip(),
        "include_adult": "false",
        "page": page
    }

    data = make_api_request(
        "search/movie",
        params
    )

    return data.get("results", [])


# ==========================================
# 10. GET MOVIE VIDEOS
# ==========================================

def get_movie_videos(movie_id):
    """Get trailers and other videos for a movie."""

    if not movie_id:
        raise ValueError("Movie ID is required.")

    data = make_api_request(
        f"movie/{movie_id}/videos"
    )

    return data.get("results", [])


# ==========================================
# 11. GET YOUTUBE TRAILER
# ==========================================

def get_movie_trailer(movie_id):
    """Find an official YouTube trailer for a movie."""

    videos = get_movie_videos(movie_id)

    youtube_videos = [
        video for video in videos
        if video.get("site") == "YouTube"
        and video.get("key")
    ]

    trailers = [
        video for video in youtube_videos
        if video.get("type") == "Trailer"
    ]

    official_trailers = [
        video for video in trailers
        if video.get("official") is True
    ]

    # First preference: Official trailer
    if official_trailers:
        selected = official_trailers[0]

    # Second preference: Other YouTube trailer
    elif trailers:
        selected = trailers[0]

    else:
        # Third preference: YouTube teaser
        teasers = [
            video for video in youtube_videos
            if video.get("type") == "Teaser"
        ]

        if not teasers:
            return None

        selected = teasers[0]

    return (
        "https://www.youtube.com/watch?v="
        + selected["key"]
    )
