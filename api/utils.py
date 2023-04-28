import json
import numpy as np
import pandas as pd
import random

movies_to_ignore = set(
    [
        14,
        20,
        75,
        111,
        115,
        165,
        166,
        244,
        279,
        280,
        296,
        330,
        454,
        515,
        536,
        563,
        569,
        665,
        671,
        683,
        688,
        701,
        718,
        788,
        795,
        815,
        817,
        853,
        863,
        900,
        910,
        916,
        925,
        963,
        969,
        995,
        1021,
        1024,
        1026,
        1043,
        1056,
        1059,
        1062,
        1080,
        1086,
        1110,
        1128,
        1147,
        1148,
        1164,
        1182,
        1187,
        1201,
        1212,
        1223,
        1233,
        1234,
        1235,
        1236,
        1246,
        1256,
        1257,
        1259,
        1278,
        1294,
        1300,
        1307,
        1312,
        1322,
        1323,
        1326,
        1331,
        1339,
        1340,
        1341,
        1343,
        1344,
        1349,
        1351,
        1353,
        1359,
        1365,
        1366,
        1368,
        1379,
        1385,
        1394,
        1402,
        1404,
        1408,
        1419,
        1421,
        1433,
        1448,
        1463,
        1482,
        1487,
        1493,
        1499,
        1503,
        1505,
        1515,
        1516,
        1518,
        1529,
        1539,
        1541,
        1559,
        1561,
        1565,
        1568,
        1570,
        1578,
        1580,
        1588,
        1601,
        1619,
        1622,
        1628,
        1634,
        1641,
        1652,
        1654,
        1660,
        1667,
        1668,
        1676,
    ]
)


def get_matrix(df, rows, cols):
    user_item_matrix = np.zeros((rows, cols))
    for row in df.itertuples():
        if row.rating != 0:
            user_item_matrix[row.user_id - 1, row.movie_id - 1] = row.rating

    user_item_matrix = np.insert(user_item_matrix, 0, 0, axis=0)
    user_item_matrix = np.insert(user_item_matrix, 0, 0, axis=1)

    return user_item_matrix


def load_user_preferences(user):
    user_item_matrix = get_matrix(
        pd.read_csv(
            f"data/u.data",
            sep="	",
            header=None,
            names=["user_id", "movie_id", "rating", "timestamp"],
            engine="python",
        ),
        943,
        1682,
    )

    with open("data/movies.json", encoding="utf8") as f:
        movies = json.load(f)
        movies_actors = {}
        for movie in movies:
            movies_actors[movie["id"]] = movie["actors"]

    user_ratings = user_item_matrix[user, :]
    rated_movies = np.where(user_ratings != 0)[0]
    user_actor_preferences = {}

    for movie in rated_movies:
        if movie in movies_actors:
            for actor in movies_actors[movie]:
                actor_id = actor["id"]
                if actor_id in user_actor_preferences:
                    user_actor_preferences[actor_id].append(
                        int(user_item_matrix[user, movie])
                    )
                else:
                    user_actor_preferences[actor_id] = [
                        int(user_item_matrix[user, movie])
                    ]

    return user_actor_preferences


def load_popular_actors():
    with open("data/popular_actors.txt") as f:
        popular_actors = f.read().splitlines()
        popular_actors = [int(actor) for actor in popular_actors]
        popular_actors = set(popular_actors)

    return popular_actors


def load_recommendations(user):
    with open("data/recommendations.json") as f:
        recommendations = json.load(f)

    recommendations = {int(k): v for k, v in recommendations.items()}
    recommendations = recommendations[user]

    recommendations = [
        {"id": recommendation[0], "rating": recommendation[1]}
        for recommendation in recommendations
    ]

    return recommendations


def load_thumbnails():
    with open("data/thumbnails.json") as f:
        thumbnails = json.load(f)

    thumbnails = {int(k): v for k, v in thumbnails.items()}

    return thumbnails


def get_positive_actors(user_preferences):
    positive_actors = set()
    for actor in user_preferences:
        if not (
            np.mean(user_preferences[actor]) < 2.5 and len(user_preferences[actor]) >= 5
        ):
            positive_actors.add(actor)

    return positive_actors


def get_actors_in_more_than_1_movie(user_preferences):
    user_actor_frequency = {}

    for actor in user_preferences:
        if len(user_preferences[actor]) > 1:
            user_actor_frequency[actor] = len(user_preferences[actor])

    return user_actor_frequency


def get_random_thumbnail(thumbnails):
    weights = [thumbnail["weight"] for thumbnail in thumbnails]
    selected_thumbnail = random.choices(thumbnails, weights=weights)[0]

    return selected_thumbnail


def get_thumbnail(
    thumbnails,
    popular_actors,
    positive_actors,
    acted_in_more_than_1_movie,
):
    POPULARITY_WEIGHT = 1
    POSITIVE_EXPOSURE_WEIGHT = 2

    for thumbnail in thumbnails:
        weights = []
        for actor in thumbnail["actors"]:
            actor_weight = 0
            if actor in popular_actors:
                actor_weight += POPULARITY_WEIGHT
            if actor in positive_actors:
                actor_weight += POSITIVE_EXPOSURE_WEIGHT
            if actor in acted_in_more_than_1_movie:
                actor_weight += 0.1 * acted_in_more_than_1_movie[actor] - 1
            else:
                actor_weight += 0.25
            weights.append(actor_weight)

        weights.sort(reverse=True)

        adjusted_weights = 0
        for i in range(len(weights)):
            adjusted_weights += weights[i] / (i + 1)

        thumbnail["weight"] = adjusted_weights

    return get_random_thumbnail(thumbnails)["path"]


def recommend(user):
    recommendations = load_recommendations(user)
    thumbnails = load_thumbnails()
    popular_actors = load_popular_actors()
    user_preferences = load_user_preferences(user)
    positive_actors = get_positive_actors(user_preferences)
    acted_in_more_than_1_movie = get_actors_in_more_than_1_movie(user_preferences)

    for recommendation in recommendations:
        movie_id = recommendation["id"]
        if recommendation["id"] in thumbnails:
            recommendation["thumbnail_path"] = get_thumbnail(
                thumbnails[movie_id],
                popular_actors,
                positive_actors,
                acted_in_more_than_1_movie,
            )
            recommendation["custom"] = True
        else:
            recommendation["thumbnail_path"] = f"{movie_id}.jpg"
            recommendation["custom"] = False

    return recommendations


def tmdb_id(movie_id):
    with open("data/movies.json", encoding="utf8") as f:
        movies = json.load(f)
        for movie in movies:
            if movie["id"] == movie_id:
                return int(movie["tmdb_id"])


def custom_thumbnails(movie_id):
    thumbnails = load_thumbnails()

    if movie_id in thumbnails:
        return thumbnails[movie_id]
    else:
        return []


def best_rated_movies(user_id):
    user_item_matrix = get_matrix(
        pd.read_csv(
            f"data/u.data",
            sep="	",
            header=None,
            names=["user_id", "movie_id", "rating", "timestamp"],
            engine="python",
        ),
        943,
        1682,
    )

    user_ratings = user_item_matrix[user_id, :]

    best_rated_movies = np.argsort(user_ratings)[::-1]

    best_movies = []

    for movie in best_rated_movies:
        if movie not in movies_to_ignore:
            best_movies.append(int(movie))

    return best_movies[:20]


print(best_rated_movies(1))
