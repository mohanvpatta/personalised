import React from "react";
import Image from "next/image";

const Slider = ({ movies, custom, changeSelectedMovieId }) => {
  if (custom) {
    movies = movies.filter((movie) => movie.custom === true);
  }

  return (
    <div className="flex w-full gap-2">
      {movies.map((movie) => (
        <div
          key={movie.id}
          className="flex min-w-[230px] min-h-[130px] hover:cursor-pointer"
          onClick={() => changeSelectedMovieId(movie.id)}
        >
          <Image
            src={`https://raw.githubusercontent.com/mohanvpatta/movie-posters/main/${movie.thumbnail_path}`}
            alt="id"
            width={200}
            height={200}
            style={{
              width: 230,
              height: 130,
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default Slider;
