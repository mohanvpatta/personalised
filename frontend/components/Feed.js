import React, { useState, useEffect } from "react";
import UserSelect from "@/components/UserSelect";
import FeedToggle from "@/components/FeedToggle";
import Slider from "@/components/Slider";
import CustomToggle from "@/components/CustomToggle";

const Feed = ({
  user,
  userOptions,
  index,
  changeUser,
  changeSelectedMovieId,
}) => {
  const [movies, setMovies] = useState([]);
  const [custom, setCustom] = useState(false);
  const [feed, setFeed] = useState("recommendations");

  useEffect(() => {
    if (feed === "recommendations") {
      fetch(`https://thumbnails.up.railway.app/recommend/${user}`)
        .then((res) => res.json())
        .then((data) => {
          setMovies(data);
          console.log(data);
        });
    } else {
      fetch(`https://thumbnails.up.railway.app/best/${user}`)
        .then((res) => res.json())
        .then((data) => {
          const formatThumbnails = data.map((movie) => {
            return {
              id: movie,
              thumbnail_path: `${movie}.jpg`,
              custom: false,
            };
          });
          setMovies(formatThumbnails);
          console.log(formatThumbnails);
        });
    }
  }, [feed]);

  const toggleCustom = () => {
    console.log(custom);
    setCustom(!custom);
  };

  const toggleFeed = (value) => {
    if (value === "") {
      setFeed("recommendations");
    } else {
      setFeed(value);
    }
  };

  useEffect(() => {
    console.log(feed);
  }, [feed]);

  return (
    <>
      <div className="flex w-full justify-between items-center">
        <UserSelect
          changeUser={changeUser}
          index={index}
          user={user}
          userOptions={userOptions}
        />
        <div className="flex">
          <CustomToggle toggle={custom} toggleCustom={toggleCustom} />
          <FeedToggle feed={feed} toggleFeed={toggleFeed} />
        </div>
      </div>
      <div className="w-full overflow-scroll">
        <Slider
          movies={movies}
          custom={custom}
          changeSelectedMovieId={changeSelectedMovieId}
        />
      </div>
    </>
  );
};

export default Feed;
