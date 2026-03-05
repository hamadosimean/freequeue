import React from "react";
import { useLang } from "@/context/LanguageContext";
import { FiSmartphone, FiClock, FiCheckCircle, FiMapPin } from "react-icons/fi";

function About() {
  const { t } = useLang();

  return (
    <section className="container mx-auto px-4 py-16 dark:bg-gray-900">
      {/* Page title */}
      <div className="max-w-3xl mx-auto text-center mb-16 dark:text-white">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">
          {t("aboutTitle")}
        </h1>

        <p className="text-lg text-gray-600 dark:text-gray-400">
          {t("aboutIntro")}
        </p>
      </div>

      {/* Mission / Vision */}
      <div className="grid md:grid-cols-2 gap-12 max-w-5xl mx-auto mb-20">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {t("ourMission")}
          </h2>

          <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
            {t("missionText")}
          </p>
        </div>

        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {t("ourVision")}
          </h2>

          <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
            {t("visionText")}
          </p>
        </div>
      </div>

      {/* How it works */}
      <div className="max-w-6xl mx-auto mb-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-12">
          {t("howItWorks")}
        </h2>

        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {/* Step 1 */}
          <div className="flex flex-col items-center p-6 rounded-xl bg-white dark:bg-gray-900 shadow-sm hover:shadow-md hover:bg-gray-50 dark:hover:bg-gray-800 transition">
            <FiSmartphone className="text-5xl text-blue-600 mb-4" />

            <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
              {t("stepOneTitle")}
            </h3>

            <p className="text-gray-600 dark:text-gray-400">
              {t("stepOneText")}
            </p>
          </div>

          {/* Walk-in */}
          <div className="flex flex-col items-center p-6 rounded-xl bg-white dark:bg-gray-900 shadow-sm hover:shadow-md hover:bg-gray-50 dark:hover:bg-gray-800 transition">
            <FiMapPin className="text-5xl text-blue-600 mb-4" />

            <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
              {t("stepWalkInTitle")}
            </h3>

            <p className="text-gray-600 dark:text-gray-400">
              {t("stepWalkInText")}
            </p>
          </div>

          {/* Step 2 */}
          <div className="flex flex-col items-center p-6 rounded-xl bg-white dark:bg-gray-900 shadow-sm hover:shadow-md hover:bg-gray-50 dark:hover:bg-gray-800 transition">
            <FiClock className="text-5xl text-blue-600 mb-4" />

            <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
              {t("stepTwoTitle")}
            </h3>

            <p className="text-gray-600 dark:text-gray-400">
              {t("stepTwoText")}
            </p>
          </div>

          {/* Step 3 */}
          <div className="flex flex-col items-center p-6 rounded-xl bg-white dark:bg-gray-900 shadow-sm hover:shadow-md hover:bg-gray-50 dark:hover:bg-gray-800 transition">
            <FiCheckCircle className="text-5xl text-blue-600 mb-4" />

            <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
              {t("stepThreeTitle")}
            </h3>

            <p className="text-gray-600 dark:text-gray-400">
              {t("stepThreeText")}
            </p>
          </div>
        </div>
      </div>

      {/* Closing */}
      <div className="max-w-3xl mx-auto text-center">
        <p className="text-lg text-gray-600 dark:text-gray-400">
          {t("aboutClosing")}
        </p>
      </div>
    </section>
  );
}

export default About;
