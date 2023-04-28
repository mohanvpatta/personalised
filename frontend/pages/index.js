import React, { useState, useEffect } from "react";
import Feed from "@/components/Feed";
import CustomSlider from "@/components/CustomSlider";
import Image from "next/image";

export default function Home() {
  const [users, setUsers] = useState([26, 53, 252, 227]);
  const [selectedMovieId, setSelectedMovieId] = useState(64);
  const [selectedMovieThumbnails, setSelectedMovieThumbnails] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const userOptions = [
    26, 37, 49, 53, 74, 120, 136, 139, 154, 157, 159, 171, 176, 192, 217, 227,
    252, 265,
  ];

  const changeUser = (user, index) => {
    const newUsers = [...users];
    newUsers[index] = user;
    setUsers(newUsers);
  };

  const changeSelectedMovie = (movie) => {
    setSelectedMovie(movie);
  };

  useEffect(() => {
    fetch(`https://thumbnails.up.railway.app/tmdb/${selectedMovieId}`)
      .then((res) => res.json())
      .then((data) => {
        fetch(
          `https://api.themoviedb.org/3/movie/${data}?api_key=7a1009b4e49581207130211394ef3d89`
        )
          .then((res) => res.json())
          .then((data) => {
            console.log(data);
            setSelectedMovie(data);
          });
      });
  }, [selectedMovieId]);

  useEffect(() => {
    fetch(`https://thumbnails.up.railway.app/custom/${selectedMovieId}`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedMovieThumbnails(data);
        console.log(data);
      });
  }, [selectedMovieId]);

  const changeSelectedMovieId = (id) => {
    setSelectedMovieId(id);
  };

  return (
    <div className="flex max-w-fit mx-auto my-16 gap-16">
      <div className="max-w-[800px]">
        {users.map((user, index) => (
          <div className="flex gap-4 flex-col items-center p-4" key={user}>
            <Feed
              user={user}
              index={index}
              changeUser={changeUser}
              changeSelectedMovieId={changeSelectedMovieId}
              userOptions={userOptions}
            />
          </div>
        ))}
      </div>
      {selectedMovie && (
        <div className="max-w-[320px] basis-full py-4">
          <div className="flex justify-between py-2 mb-4 font-medium">
            <div className="text-neutral-200">{selectedMovie.title}</div>
            <div className="text-neutral-500">
              {selectedMovie.release_date.split("-")[0]}
            </div>
          </div>
          <div>
            <Image
              src={`https://raw.githubusercontent.com/mohanvpatta/movie-posters/main/${selectedMovieId}.jpg`}
              alt="id"
              width={800}
              height={800}
              style={{
                width: "100%",
                height: "auto",
              }}
            />
          </div>
          <div>
            <div className="my-4 mb-6 ">
              <div className="my-4 font-medium text-neutral-500">Overview</div>
              <div className="text-neutral-300">
                {`${selectedMovie.overview.substring(0, 200)}... `}
                <a
                  href={`https://www.themoviedb.org/movie/${selectedMovie.id}`}
                  target="_blank"
                  rel="noreferrer"
                  className="underline text-neutral-500"
                >
                  {"Read more"}
                </a>
              </div>
            </div>
            <div className="my-4 mb-6 ">
              <div className="my-4 font-medium text-neutral-500">Genres</div>
              <div className="text-neutral-300">
                {selectedMovie.genres.map((genre) => genre.name).join(", ")}
              </div>
            </div>
            {selectedMovieThumbnails.length > 0 && (
              <div className="my-4 mb-6 ">
                <div className="my-4 font-medium text-neutral-500">
                  Custom Thumbnails
                </div>
                <div className="w-full overflow-scroll">
                  <CustomSlider thumbnails={selectedMovieThumbnails} />
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
