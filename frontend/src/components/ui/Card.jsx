import React from "react";

export const Card = ({
  children,
  className = "",
  padding = true,
  ...props
}) => {
  return (
    <div
      className={`
        bg-white rounded-xl shadow-md
        ${padding ? "p-6" : ""}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
};
