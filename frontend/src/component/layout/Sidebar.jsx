import React, { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { useLang } from "@/context/LanguageContext";
import { FaBars, FaTimes } from "react-icons/fa";

function SideBar({ routes = [] }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const { t } = useLang();

  const navStyle = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-2 transition duration-300 border-b border-gray-200 dark:border-gray-800 ${
      isActive
        ? "bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400"
        : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
    }`;

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Mobile overlay */}
      {menuOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-30 lg:hidden"
          onClick={() => setMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static z-40 top-0 left-0 h-screen w-64 bg-white dark:bg-gray-900 transform transition-transform duration-300 ring-1 ring-gray-300 dark:ring-gray-800
        ${menuOpen ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0`}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          {menuOpen && (
            <div className="flex items-center justify-between px-5 py-4 border-b dark:border-gray-800">
              <h1 className="text-xl font-bold text-gray-800 dark:text-white">
                FreeQueues
              </h1>

              <button
                className="lg:hidden text-gray-600 dark:text-gray-300"
                onClick={() => setMenuOpen(false)}
              >
                <FaTimes size={20} />
              </button>
            </div>
          )}

          {/* Navigation */}
          <nav className="flex-1 px-3 py-6 space-y-2">
            {routes.map((route) => (
              <NavLink key={route.to} to={route.to} className={navStyle}>
                <span className="text-lg">{route.icon}</span>
                <span>{t(route.label)}</span>
              </NavLink>
            ))}
          </nav>

          {/* Footer */}
          <div className="px-5 py-4 border-t text-sm text-gray-500 dark:border-gray-800">
            © {new Date().getFullYear()} FreeQueues
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Mobile Top Bar */}
        <header className="flex items-center justify-between px-4 py-3 bg-white dark:bg-gray-950 border-b border-gray-300 dark:border-gray-800 lg:hidden">
          <button
            onClick={() => setMenuOpen(true)}
            className="text-gray-700 dark:text-gray-200"
          >
            <FaBars size={22} />
          </button>
        </header>

        {/* Page content */}
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default SideBar;
