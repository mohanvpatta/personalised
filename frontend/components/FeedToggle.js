import React, { useState } from "react";
import * as ToggleGroup from "@radix-ui/react-toggle-group";
import { HomeIcon, CounterClockwiseClockIcon } from "@radix-ui/react-icons";

const toggleGroupItemClasses =
  "bg-neutral-800 p-2 h-full hover:bg-neutral-600 cursor-pointer rounded data-[state=on]:bg-neutral-600";

const FeedToggle = ({ feed, toggleFeed }) => {
  return (
    <ToggleGroup.Root
      className="flex rounded space-x-px bg-neutral-800 p-1 text-neutral-300"
      type="single"
      value={feed}
      aria-label="Movies Toggle"
      onValueChange={(value) => {
        toggleFeed(value);
      }}
    >
      <ToggleGroup.Item
        className={toggleGroupItemClasses}
        value="recommendations"
        aria-label="recommendations"
      >
        <HomeIcon />
      </ToggleGroup.Item>
      <ToggleGroup.Item
        className={toggleGroupItemClasses}
        value="watched"
        aria-label="watched"
      >
        <CounterClockwiseClockIcon />
      </ToggleGroup.Item>
    </ToggleGroup.Root>
  );
};

export default FeedToggle;
