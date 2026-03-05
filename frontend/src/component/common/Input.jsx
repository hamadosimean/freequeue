import React, { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
export default function Input({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  error,
  className = "",
  ...props
}) {
  const [showPassword, setShowPassword] = useState(false);
  const isPasswordType = type === "password";

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div>
      {label && (
        <label
          htmlFor={label.toLowerCase().replace(" ", "-")}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
        >
          {label}
        </label>
      )}
      <div className="relative">
        <input
          type={isPasswordType ? (showPassword ? "text" : "password") : type}
          value={value}
          onChange={onChange}
          id={label?.toLowerCase().replace(" ", "-")}
          placeholder={placeholder}
          className={`
            w-full px-4 text-gray-700 dark:text-gray-300 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500
            ${error ? "border-red-500 focus:ring-red-500" : "border-gray-300 dark:border-gray-600"}
            ${isPasswordType ? "pr-10" : ""}
            ${className}
          `}
          {...props}
        />
        {isPasswordType && (
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none"
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? <FaEyeSlash size={18} /> : <FaEye size={18} />}
          </button>
        )}
      </div>
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
}
