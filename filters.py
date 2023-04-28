import pandas as pd
import numpy as np
import numpy.ma as ma
from datetime import datetime
import warnings
from pprint import pprint
import json


u_data = np.loadtxt("100k/u.data", dtype=int)

num_users = np.max(u_data[:, 0])
num_items = np.max(u_data[:, 1])


def get_matrix_from_txt(path):
    matrix = np.loadtxt(path)
    matrix = np.insert(matrix, 0, 0, axis=0)
    matrix = np.insert(matrix, 0, 0, axis=1)

    return matrix


def get_matrix(df, rows, cols):
    user_item_matrix = np.zeros((rows, cols))
    for row in df.itertuples():
        if row.rating != 0:
            user_item_matrix[row.user_id - 1, row.movie_id - 1] = row.rating

    user_item_matrix = np.insert(user_item_matrix, 0, 0, axis=0)
    user_item_matrix = np.insert(user_item_matrix, 0, 0, axis=1)

    return user_item_matrix


def predict_ratings_colab(user_id, user_item_matrix, user_similarity_matrix):
    top_n_users = 400

    predicted_ratings = np.zeros(user_item_matrix.shape[1])
    for item in range(1, user_item_matrix.shape[1]):
        ratings = user_item_matrix[:, item]

        similarities = user_similarity_matrix[user_id, :]
        similar_users = np.argsort(similarities)[::-1][1:top_n_users]

        masked_ratings = ma.masked_array(ratings, mask=(ratings == 0))
        masked_similarities = ma.masked_array(
            similarities[similar_users], mask=(ratings[similar_users] == 0)
        )

        weighted_ratings = ma.dot(masked_similarities, masked_ratings[similar_users])
        similarity_weights = np.sum(masked_similarities)

        if similarity_weights > 0:
            predicted_rating = weighted_ratings / similarity_weights
        else:
            predicted_rating = 0
        predicted_ratings[item] = predicted_rating

    return predicted_ratings


def predict_ratings_content(user_id, user_item_matrix, item_item_similarity_matrix):
    movies_rated_by_user = user_item_matrix[user_id, :].nonzero()[0]
    movie_ratings = user_item_matrix[user_id, movies_rated_by_user]

    predicted_ratings = np.zeros(user_item_matrix.shape[1])
    for item in range(1, user_item_matrix.shape[1]):
        similarities = item_item_similarity_matrix[item, movies_rated_by_user]
        if np.sum(similarities) == 0:
            predicted_ratings[item] = 0
        else:
            predicted_ratings[item] = np.dot(similarities, movie_ratings) / np.sum(
                similarities
            )

    return predicted_ratings


def triangle_similarity(ratings_m, ratings_n):
    nz_indices_m = ratings_m.nonzero()
    nz_indices_n = ratings_n.nonzero()
    nz_indices = np.intersect1d(nz_indices_m, nz_indices_n)

    if len(nz_indices) < 0:
        return 0
    ratings_m = ratings_m[nz_indices]
    ratings_n = ratings_n[nz_indices]

    numerator = np.sum(np.subtract(ratings_m, ratings_n) ** 2) ** 0.5
    denominator = np.sum((ratings_m) ** 2) ** 0.5 + np.sum((ratings_n) ** 2) ** 0.5

    if denominator == 0:
        return 0

    return 1 - (numerator / denominator)


def calculate_user_similarity_matrix(user_item_matrix, index):
    user_similarity_matrix = np.zeros(
        (user_item_matrix.shape[0], user_item_matrix.shape[0])
    )

    row_means = user_item_matrix.mean(axis=1)
    row_stdevs = user_item_matrix.std(axis=1, ddof=1)
    row_stdevs[row_stdevs == 0] = 1
    user_item_matrix_centered = user_item_matrix - row_means.reshape(-1, 1)
    user_item_matrix_normalized = user_item_matrix_centered / row_stdevs.reshape(-1, 1)

    x_min = np.min(user_item_matrix_normalized)
    x_max = np.max(user_item_matrix_normalized)

    user_item_matrix = (user_item_matrix_normalized - x_min) / (x_max - x_min)

    for i in range(1, user_item_matrix.shape[0]):
        for j in range(i + 1, user_item_matrix.shape[0]):
            user_similarity_matrix[i, j] = triangle_similarity(
                user_item_matrix[i], user_item_matrix[j]
            )
            user_similarity_matrix[j, i] = user_similarity_matrix[i, j]

    return user_similarity_matrix


def get_eval(predicted, actual):
    nz_indices = actual.nonzero()
    nz_actual = actual[nz_indices]
    nz_predicted = predicted[nz_indices]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        mse = np.mean((nz_predicted - nz_actual) ** 2)
        rmse = np.sqrt(mse)

        mae = np.mean(np.abs(nz_predicted - nz_actual))

        return {
            "rmse": rmse,
            "mae": mae,
        }


def get_avg_eval(results):
    dict = {
        "combined_25": [],
        "combined_50": [],
        "combined_75": [],
        "content": [],
        "colab": [],
    }
    for result in results:
        rmse = np.mean(
            [results[result][i]["rmse"] for i in range(len(results[result]))]
        )
        mae = np.mean([results[result][i]["mae"] for i in range(len(results[result]))])
        print(result)
        print(rmse, mae)

        dict[result].extend([rmse, mae])

    return dict


def final_avg(final):
    dict = {
        "combined_25": [],
        "combined_50": [],
        "combined_75": [],
        "content": [],
        "colab": [],
    }

    for item in final:
        for key in item:
            dict[key].extend(item[key])

    import json

    with open("final.json", "w") as f:
        json.dump(dict, f)

    for key in dict:
        avg_rmse = []
        avg_mae = []
        for i in range(0, len(dict[key]), 2):
            avg_rmse.append(dict[key][i])
            avg_mae.append(dict[key][i + 1])
        print(key)
        print(np.mean(avg_rmse), np.mean(avg_mae))

    return dict


def run_benchmark():
    final = []
    for index in range(1, 6):
        [base, test] = [
            pd.read_csv(
                f"100k/u{index}.base",
                sep="	",
                header=None,
                names=["user_id", "movie_id", "rating", "timestamp"],
                engine="python",
            ),
            pd.read_csv(
                f"100k/u{index}.test",
                sep="	",
                header=None,
                names=["user_id", "movie_id", "rating", "timestamp"],
                engine="python",
            ),
        ]

        item_similarity_matrix = get_matrix_from_txt("data/item_similarity_matrix.txt")

        user_similarity_matrix = calculate_user_similarity_matrix(
            get_matrix(
                base,
                num_users,
                num_items,
            ),
            index,
        )

        user_item_matrix_train = get_matrix(
            base,
            num_users,
            num_items,
        )

        user_item_matrix_test = get_matrix(
            test,
            num_users,
            num_items,
        )

        results = {
            "combined_25": [],
            "combined_50": [],
            "combined_75": [],
            "content": [],
            "colab": [],
        }

        for user in range(1, user_item_matrix_test.shape[0]):
            predicted_ratings_colab = predict_ratings_colab(
                user, user_item_matrix_train, user_similarity_matrix
            )
            predicted_ratings_content = predict_ratings_content(
                user, user_item_matrix_train, item_similarity_matrix
            )
            predicted_ratings_25 = (
                0.25 * predicted_ratings_colab + 0.75 * predicted_ratings_content
            )
            predicted_ratings_50 = (
                0.50 * predicted_ratings_colab + 0.50 * predicted_ratings_content
            )
            predicted_ratings_75 = (
                0.75 * predicted_ratings_colab + 0.25 * predicted_ratings_content
            )

            results_combined_25 = get_eval(
                predicted_ratings_25, user_item_matrix_test[user]
            )
            results_combined_50 = get_eval(
                predicted_ratings_50, user_item_matrix_test[user]
            )
            results_combined_75 = get_eval(
                predicted_ratings_75, user_item_matrix_test[user]
            )
            results_content = get_eval(
                predicted_ratings_content, user_item_matrix_test[user]
            )
            results_colab = get_eval(
                predicted_ratings_colab, user_item_matrix_test[user]
            )

            if not np.isnan(results_combined_25["rmse"]) and not np.isnan(
                results_combined_25["mae"]
            ):
                results["combined_25"].append(results_combined_25)

            if not np.isnan(results_combined_50["rmse"]) and not np.isnan(
                results_combined_50["mae"]
            ):
                results["combined_50"].append(results_combined_50)

            if not np.isnan(results_combined_75["rmse"]) and not np.isnan(
                results_combined_75["mae"]
            ):
                results["combined_75"].append(results_combined_75)

            if not np.isnan(results_content["rmse"]) and not np.isnan(
                results_content["mae"]
            ):
                results["content"].append(results_content)

            if not np.isnan(results_colab["rmse"]) and not np.isnan(
                results_colab["mae"]
            ):
                results["colab"].append(results_colab)

        eval = get_avg_eval(results)
        final.append(eval)
    final_avg(final)


def calculate_user_similarity_matrix_data(user_item_matrix):
    user_similarity_matrix = np.zeros(
        (user_item_matrix.shape[0], user_item_matrix.shape[0])
    )

    row_means = user_item_matrix.mean(axis=1)
    row_stdevs = user_item_matrix.std(axis=1, ddof=1)
    row_stdevs[row_stdevs == 0] = 1
    user_item_matrix_centered = user_item_matrix - row_means.reshape(-1, 1)
    user_item_matrix_normalized = user_item_matrix_centered / row_stdevs.reshape(-1, 1)

    x_min = np.min(user_item_matrix_normalized)
    x_max = np.max(user_item_matrix_normalized)

    user_item_matrix = (user_item_matrix_normalized - x_min) / (x_max - x_min)

    for i in range(1, user_item_matrix.shape[0]):
        for j in range(i + 1, user_item_matrix.shape[0]):
            user_similarity_matrix[i, j] = triangle_similarity(
                user_item_matrix[i], user_item_matrix[j]
            )
            user_similarity_matrix[j, i] = user_similarity_matrix[i, j]

    print(f"Completed calculating similarity matrix for u")

    return user_similarity_matrix


def main():
    run_benchmark()


if __name__ == "__main__":
    main()
