import React from "react";
import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";
import Footer from "./Footer";
function MainLayout() {
  return (
    <div>
      <NavBar />
      <Outlet />
      <Footer />
    </div>
  );
}

export default MainLayout;
