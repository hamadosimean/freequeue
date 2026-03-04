import { createBrowserRouter } from "react-router-dom";
import {
  Home,
  About,
  Dashboard,
  NotFound,
  Space,
  Login,
  Register,
  ResetPassword,
  ForgetPassword,
} from "../pages";
import { MainLayout, AuthLayout } from "@/components/layout";
export const AppRoutes = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "auth",
        element: <AuthLayout />,
        children: [
          {
            index: true,
            element: <Login />,
          },
          {
            path: "login",
            element: <Login />,
          },
          {
            path: "register",
            element: <Register />,
          },
          {
            path: "reset-password",
            element: <ResetPassword />,
          },
          {
            path: "forget-password",
            element: <ForgetPassword />,
          },
        ],
      },
      {
        path: "about",
        element: <About />,
      },
      {
        path: "dashboard",
        element: <Dashboard />,
      },
      {
        path: "space",
        element: <Space />,
      },
    ],
  },
  {
    path: "*",
    element: <NotFound />,
  },
]);
