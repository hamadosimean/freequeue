import React from "react";
import { PropagateLoader } from "react-spinners";
import { useLang } from "@/context/LanguageContext";
function LoadingSpinner({
  size = 15,
  color = "#2b66e4",
  label = "Loading...",
}) {
  const { t } = useLang();
  return (
    <div className="flex flex-col items-center justify-center gap-4 h-screen">
      <PropagateLoader color={color} size={size} />
      <p className="text-gray-500 dark:text-gray-400">{t(label)}</p>
    </div>
  );
}

export default LoadingSpinner;
