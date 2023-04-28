import React from "react";
import * as Select from "@radix-ui/react-select";
import {
  CheckIcon,
  ChevronDownIcon,
  ChevronUpIcon,
} from "@radix-ui/react-icons";

const SelectItem = React.forwardRef(({ children, ...props }, forwardedRef) => {
  return (
    <Select.Item {...props} ref={forwardedRef}>
      <Select.ItemText>{children}</Select.ItemText>
      <Select.ItemIndicator className="SelectItemIndicator">
        <CheckIcon className="text-neutral-300" />
      </Select.ItemIndicator>
    </Select.Item>
  );
});

SelectItem.displayName = "SelectItem";

const UserSelect = ({ changeUser, index, userOptions, user }) => {
  const [selectedUser, setSelectedUser] = React.useState(user);

  const handleChangeUser = (value) => {
    setSelectedUser(value);
    changeUser(value, index);
  };

  return (
    <Select.Root
      aria-label="User"
      onValueChange={(value) => {
        handleChangeUser(value);
      }}
      value={selectedUser}
    >
      <Select.Trigger
        aria-label="User Select"
        className="flex items-center justify-between gap-3 bg-neutral-800 py-2 px-4 rounded-sm w-44 text-neutral-300"
      >
        <Select.Value placeholder="Select a user" />
        <Select.Icon>
          <ChevronDownIcon />
        </Select.Icon>
      </Select.Trigger>
      <Select.Portal>
        <Select.Content className="bg-neutral-800">
          <Select.ScrollUpButton className="flex items-center justify-center h-[25px] bg-neutral-800 text-violet11 cursor-default">
            <ChevronUpIcon />
          </Select.ScrollUpButton>
          <Select.Viewport>
            <Select.Group>
              {userOptions.map((option) => {
                return (
                  <SelectItem
                    value={option}
                    key={option}
                    className="flex items-center justify-between gap-3 w-44 text-neutral-300 bg-neutral-800 py-2 px-4 cursor-pointer rounded-sm hover:bg-neutral-900"
                  >
                    User {option}
                  </SelectItem>
                );
              })}
            </Select.Group>
          </Select.Viewport>
          <Select.ScrollDownButton>
            <ChevronDownIcon />
          </Select.ScrollDownButton>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
};

export default UserSelect;
