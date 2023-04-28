import os
import json
import shutil


def clean_thumbnails():
    path = "thumbnails-processed"

    for file in os.listdir(path):
        if file.endswith(".png"):
            os.remove(os.path.join(path, file))
        if file.endswith(".jpg"):
            if "_" in file:
                os.remove(os.path.join(path, file))


def generate_thumbnails(thumbnails_dir, thumbnails_processed_dir):

    for movie_id in os.listdir(thumbnails_dir):
        movie_dir = os.path.join(thumbnails_dir, movie_id)

        for thumbnail_filename in os.listdir(movie_dir):
            thumbnail_path = os.path.join(movie_dir, thumbnail_filename)

            filename, ext = os.path.splitext(thumbnail_filename)

            new_filename = f"{movie_id}_{filename}{ext}"

            shutil.copy(
                thumbnail_path, os.path.join(thumbnails_processed_dir, new_filename)
            )


def generate_thumbnail_data(thumbnails_dir, json_dir):
    json_path = os.path.join(json_dir, "thumbnails.json")

    movie_data = {}

    for movie_id in os.listdir(thumbnails_dir):
        movie_dir = os.path.join(thumbnails_dir, movie_id)
        thumbnails = []

        for thumbnail_filename in os.listdir(movie_dir):
            actor_ids_str, ext = os.path.splitext(thumbnail_filename)
            actor_ids = [int(actor_id) for actor_id in actor_ids_str.split(",")]

            new_filename = f"{movie_id}_{thumbnail_filename}"

            thumbnail_path = os.path.join(movie_id, thumbnail_filename)
            new_thumbnail_path = new_filename

            thumbnails.append({"path": new_thumbnail_path, "actors": actor_ids})

        movie_data[movie_id] = thumbnails

    with open(json_path, "w") as f:
        json.dump(movie_data, f, indent=2)


def process_thumbnails():
    thumbnails_dir = "thumbnails"
    thumbnails_processed_dir = "thumbnails-processed"

    json_dir = "api/data"

    clean_thumbnails()
    generate_thumbnails(thumbnails_dir, thumbnails_processed_dir)
    generate_thumbnail_data(thumbnails_dir, json_dir)


if __name__ == "__main__":
    process_thumbnails()
