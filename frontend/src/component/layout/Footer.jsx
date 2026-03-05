import React from "react";
import { Link } from "react-router-dom";
import { useLang } from "@/context/LanguageContext";
import { AppRoutes } from "@/routes/routes";
function Footer() {
  const { t } = useLang();

  return (
    <footer className="bg-gray-100 dark:bg-gray-900 pt-16 pb-10">
      <div className="container mx-auto px-4">
        {/* Top footer content */}
        <div className="grid md:grid-cols-3 gap-10 mb-16 md:text-center">
          {/* Product */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
              {t("product")}
            </h3>

            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>
                <Link to={AppRoutes.home}>{t("home")}</Link>
              </li>
              <li>
                <Link to={AppRoutes.about}>{t("about")}</Link>
              </li>
              <li>
                <Link to={AppRoutes.contact}>{t("contact")}</Link>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
              {t("company")}
            </h3>

            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>
                <Link to={AppRoutes.about}>{t("about")}</Link>
              </li>
              <li>
                <Link to={AppRoutes.contact}>{t("contact")}</Link>
              </li>
            </ul>
          </div>

          {/* Account */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
              {t("account")}
            </h3>

            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>
                <Link to={AppRoutes.login}>{t("login")}</Link>
              </li>
              <li>
                <Link to={AppRoutes.register}>{t("register")}</Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider section */}
        <div className="border-t border-gray-300 dark:border-gray-700 pt-10 text-center">
          {/* Copyright */}
          <p className="text-gray-500 dark:text-gray-400 mb-4">
            © {new Date().getFullYear()} FreeQueues. {t("all_rights_reserved")}
          </p>

          {/* Trust / Legal links */}
          <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm text-gray-500 dark:text-gray-400 mb-8">
            <Link
              to={AppRoutes.trustCenter}
              className="hover:text-gray-900 dark:hover:text-white"
            >
              {t("trust_center")}
            </Link>

            <Link
              to={AppRoutes.privacy}
              className="hover:text-gray-900 dark:hover:text-white"
            >
              {t("privacy")}
            </Link>

            <Link
              to={AppRoutes.abuse}
              className="hover:text-gray-900 dark:hover:text-white"
            >
              {t("abuse")}
            </Link>

            <Link
              to={AppRoutes.cookies}
              className="hover:text-gray-900 dark:hover:text-white"
            >
              {t("cookie_settings")}
            </Link>
          </div>

          {/* Big brand signature */}
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold tracking-tight text-gray-900 dark:text-white opacity-90">
            FreeQueues
          </h1>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
