import { createBrowserRouter } from "react-router-dom";
import { Home, About, Dashboard, NotFound, Space } from "../pages";
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
