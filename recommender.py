
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_movies(
    movies,
    preferred_genres=None,
    liked_movies=None,
    disliked_movies=None,
    ratings=None,
    top_n=12
):
    preferred_genres = preferred_genres or []
    liked_movies = liked_movies or []
    disliked_movies = disliked_movies or []
    ratings = ratings or {}

    if not movies:
        return []

    excluded = set(liked_movies + disliked_movies)

    candidates = [
        movie for movie in movies
        if movie.get("title") not in excluded
    ]

    if not candidates:
        return []

    def movie_text(movie):
        genres = " ".join(movie.get("genres", []))
        overview = movie.get("overview", "")
        return genres + " " + overview

    all_texts = [
        movie_text(movie) for movie in movies
    ]

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english"
        )
        matrix = vectorizer.fit_transform(all_texts)
    except ValueError:
        matrix = None

    title_to_index = {
        movie.get("title"): index
        for index, movie in enumerate(movies)
    }

    liked_indices = [
        title_to_index[title]
        for title in liked_movies
        if title in title_to_index
    ]

    rated_indices = [
        (title_to_index[title], rating)
        for title, rating in ratings.items()
        if title in title_to_index and rating >= 4
    ]

    disliked_indices = [
        title_to_index[title]
        for title in disliked_movies
        if title in title_to_index
    ]

    results = []

    for movie in candidates:

        original_index = title_to_index.get(
            movie.get("title")
        )

        if original_index is None:
            continue

        genre_score = 0
        movie_genres = set(movie.get("genres", []))

        for genre in preferred_genres:
            if genre in movie_genres:
                genre_score += 1

        if preferred_genres:
            genre_score /= len(preferred_genres)

        like_similarity = 0
        rating_similarity = 0
        dislike_similarity = 0

        if matrix is not None:

            candidate_vector = matrix[original_index]

            if liked_indices:
                similarities = cosine_similarity(
                    candidate_vector,
                    matrix[liked_indices]
                )[0]

                like_similarity = float(
                    similarities.max()
                )

            if rated_indices:
                weighted_scores = []

                for index, rating in rated_indices:
                    similarity = cosine_similarity(
                        candidate_vector,
                        matrix[index]
                    )[0][0]

                    weighted_scores.append(
                        similarity * (rating / 5)
                    )

                rating_similarity = max(
                    weighted_scores
                )

            if disliked_indices:
                similarities = cosine_similarity(
                    candidate_vector,
                    matrix[disliked_indices]
                )[0]

                dislike_similarity = float(
                    similarities.max()
                )

        tmdb_rating = (
            movie.get("vote_average", 0) or 0
        ) / 10

        final_score = (
            0.25 * genre_score
            + 0.35 * like_similarity
            + 0.20 * rating_similarity
            + 0.20 * tmdb_rating
            - 0.20 * dislike_similarity
        )

        final_score = max(0, min(1, final_score))

        results.append({
            **movie,
            "recommendation_score": round(
                final_score * 100, 2
            )
        })

    results.sort(
        key=lambda item: item["recommendation_score"],
        reverse=True
    )

    return results[:top_n]
