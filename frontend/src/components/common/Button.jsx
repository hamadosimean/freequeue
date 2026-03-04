import React from "react";
export const Button = ({
  children,
  variant = "primary",
  size = "md",
  onClick,
  disabled = false,
  fullWidth = false,
  className = "",
  ...props
}) => {
  const baseClasses =
    "font-medium rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2";

  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
    secondary:
      "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500",
    danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
    outline: "border-2 border-blue-600 text-blue-600 hover:bg-blue-50",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  const classes = `
    ${baseClasses}
    ${variants[variant]}
    ${sizes[size]}
    ${fullWidth ? "w-full" : ""}
    ${disabled ? "opacity-50 cursor-not-allowed" : ""}
    ${className}
  `;

  return (
    <button
      className={classes}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
