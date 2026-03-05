import React from "react";
import CustomModal from "../component/common/Modal";
function Space() {
  const [isOpen, setIsOpen] = React.useState(false);
  return (
    <div>
      <CustomModal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        label="Modal"
      >
        <p>Modal</p>
      </CustomModal>
      <button onClick={() => setIsOpen((prev) => !prev)}>Open Modal</button>
    </div>
  );
}

export default Space;
