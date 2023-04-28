import React from "react";
import Image from "next/image";

const CustomSlider = ({ thumbnails }) => {
  return (
    <div className="flex w-full gap-2">
      {thumbnails.map((thumbnail) => (
        <div key={thumbnail.path} className="flex min-w-[230px] min-h-[130px]">
          <Image
            src={`https://raw.githubusercontent.com/mohanvpatta/movie-posters/main/${thumbnail.path}`}
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

export default CustomSlider;
