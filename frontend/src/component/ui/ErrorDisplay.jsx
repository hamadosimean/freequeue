import React from "react";

function ErrorDisplay({ error }) {
  return (
    <div className="p-3 text-sm text-red-500 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
      {error}
    </div>
  );
}

export default ErrorDisplay;
