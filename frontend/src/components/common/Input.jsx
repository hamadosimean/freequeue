import React from "react";

export const Input = ({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  error,
  className = "",
  ...props
}) => {
  return (
    <div>
      {label && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {label}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`
          w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500
          ${error ? "border-red-500" : "border-gray-300 dark:border-gray-600"}
          ${className}
        `}
        {...props}
      />
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
};
