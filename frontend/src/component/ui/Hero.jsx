import React from "react";
import { Link } from "react-router-dom";
import { useLang } from "@/context/LanguageContext";
import { FiClock, FiSmartphone, FiUsers } from "react-icons/fi";
import { womanHoldingPhone } from "@/assets/images";
import { AppRoutes } from "@/routes/routes";
function Hero() {
  const { t } = useLang();

  return (
    <section className="bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-950 py-20">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* LEFT CONTENT */}
          <div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold mb-6 text-gray-900 dark:text-white">
              {t("heroTitle")}
            </h1>

            <p className="text-lg mb-8 text-gray-600 dark:text-gray-300">
              {t("heroSubtitle")}
            </p>

            {/* CTA */}
            <div className="flex flex-col sm:flex-row gap-4 mb-10">
              <Link
                to={AppRoutes.register}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition text-center"
              >
                {t("getStarted")}
              </Link>

              <Link
                to={AppRoutes.about}
                className="border border-gray-300 dark:border-gray-700 px-6 py-3 rounded-lg text-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition text-center"
              >
                {t("learnMore")}
              </Link>
            </div>

            {/* FEATURES */}
            <div className="grid grid-cols-3 gap-6 text-center">
              <div>
                <FiSmartphone className="text-3xl text-blue-600 mx-auto mb-2" />
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t("heroFeatureOneTitle")}
                </p>
              </div>

              <div>
                <FiClock className="text-3xl text-blue-600 mx-auto mb-2" />
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t("heroFeatureTwoTitle")}
                </p>
              </div>

              <div>
                <FiUsers className="text-3xl text-blue-600 mx-auto mb-2" />
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t("heroFeatureThreeTitle")}
                </p>
              </div>
            </div>
          </div>

          {/* Right IMAGE */}
          <div className="flex justify-center">
            <img
              src={womanHoldingPhone}
              alt="Woman joining queue with phone"
              className="rounded-2xl shadow-xl w-full max-w-md object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
