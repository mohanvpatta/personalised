import React from "react";
import * as Toggle from "@radix-ui/react-toggle";
import { StarIcon } from "@radix-ui/react-icons";

const CustomToggle = ({ toggle, toggleCustom }) => {
  return (
    <div className="rounded space-x-px bg-neutral-800 p-1 mr-3 text-neutral-300">
      <Toggle.Root
        pressed={toggle}
        onPressedChange={() => {
          toggleCustom();
        }}
        aria-label="Toggle Custom Thumbnails"
        className="bg-neutral-800 p-2 h-full hover:bg-neutral-600 cursor-pointer rounded data-[state=on]:bg-neutral-600"
      >
        <StarIcon />
      </Toggle.Root>
    </div>
  );
};

export default CustomToggle;
