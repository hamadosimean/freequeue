import React from "react";
import { useLang } from "@/context/LanguageContext";
function Pricing() {
  const { t } = useLang();
  return (
    <section className="container mx-auto px-4 py-20">
      {/* Title */}
      <div className="max-w-3xl mx-auto text-center mb-16">
        <h2 className="text-xl md:text-6xl font-extrabold text-gray-900 ">
          {t("pricingTitle")}
        </h2>

        <p className="text-lg text-gray-600 dark:text-gray-400">
          {t("pricingSubtitle")}
        </p>
      </div>
    </section>
  );
}

export default Pricing;
