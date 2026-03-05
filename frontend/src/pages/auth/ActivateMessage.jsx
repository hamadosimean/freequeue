import React from "react";
import { useLang } from "@/context/LanguageContext";

function ActivateMessage() {
  const { t } = useLang();
  return (
    <div className="flex items-center justify-center min-h-[80vh] px-4">
      <div className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700">
        <div className="text-center space-y-2">
          <p className="text-base font-bold text-gray-900 dark:text-gray-200">
            {t("checkYourEmail")}
          </p>
        </div>
      </div>
    </div>
  );
}

export default ActivateMessage;
