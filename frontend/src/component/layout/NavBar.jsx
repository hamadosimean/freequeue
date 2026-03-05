import React, { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { useLang } from "@/context/LanguageContext";
import { AppRoutes } from "@/routes/routes";

function NavBar() {
  const { t, changeLang } = useLang();
  const [menuOpen, setMenuOpen] = useState(false);

  const navStyle = ({ isActive }) =>
    `text-base font-medium transition ${
      isActive
        ? "text-blue-600"
        : "text-gray-600 dark:text-gray-300 hover:text-blue-500"
    }`;

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm ring">
      <nav className="container mx-auto px-4 h-20 flex items-center justify-between">
        {/* Logo */}
        <Link
          to="/"
          className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white"
        >
          FreeQueue
        </Link>

        {/* Desktop Menu */}
        <ul className="hidden md:flex items-center space-x-10">
          <li>
            <NavLink to="/" className={navStyle}>
              {t("home")}
            </NavLink>
          </li>

          <li>
            <NavLink to={AppRoutes.about} className={navStyle}>
              {t("about")}
            </NavLink>
          </li>

          <li>
            <NavLink to={AppRoutes.contact} className={navStyle}>
              {t("contact")}
            </NavLink>
          </li>
        </ul>

        {/* Right section */}
        <div className="hidden md:flex items-center space-x-6">
          {/* Auth */}
          <NavLink to={AppRoutes.login} className={navStyle}>
            {t("login")}
          </NavLink>

          <NavLink
            to={AppRoutes.register}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            {t("register")}
          </NavLink>

          {/* Language chooser */}
          <select
            onChange={(e) => changeLang(e.target.value)}
            className="border rounded-md px-2 py-1 text-sm bg-white dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
          >
            <option value="en">EN</option>
            <option value="fr">FR</option>
            <option value="ar">AR</option>
          </select>
        </div>

        {/* Mobile Button */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden text-gray-700 dark:text-white"
        >
          {menuOpen ? (
            <span className="text-2xl">✕</span>
          ) : (
            <span className="text-2xl">☰</span>
          )}
        </button>
      </nav>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-white dark:bg-gray-800 border-t">
          <ul className="flex flex-col items-center space-y-6 py-6">
            <li>
              <NavLink
                to="/"
                className={navStyle}
                onClick={() => setMenuOpen(false)}
              >
                {t("home")}
              </NavLink>
            </li>

            <li>
              <NavLink
                to={AppRoutes.about}
                className={navStyle}
                onClick={() => setMenuOpen(false)}
              >
                {t("about")}
              </NavLink>
            </li>

            <li>
              <NavLink
                to={AppRoutes.contact}
                className={navStyle}
                onClick={() => setMenuOpen(false)}
              >
                {t("contact")}
              </NavLink>
            </li>

            <div className="border-t w-2/3 pt-4 flex flex-col items-center space-y-4">
              <NavLink
                to={AppRoutes.login}
                className={navStyle}
                onClick={() => setMenuOpen(false)}
              >
                {t("login")}
              </NavLink>

              <NavLink
                to={AppRoutes.register}
                className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700"
                onClick={() => setMenuOpen(false)}
              >
                {t("register")}
              </NavLink>

              {/* Language chooser mobile */}
              <li>
                <select
                  onChange={(e) => changeLang(e.target.value)}
                  className="border rounded-md px-3 py-2 text-sm bg-white dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600"
                >
                  <option value="fr">FR</option>
                  <option value="ar">AR</option>
                </select>
              </li>
            </div>
          </ul>
        </div>
      )}
    </header>
  );
}

export default NavBar;
