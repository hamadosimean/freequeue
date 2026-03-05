import React, { useState } from "react";
import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import NavBar from "./NavBar";
import SideBar from "./Sidebar";

function AdminLayout() {
  const { isAuthenticated } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-200">
      <NavBar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex">
        <SideBar />
        <main className="flex-1 p-6 transition-all duration-300">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AdminLayout;
