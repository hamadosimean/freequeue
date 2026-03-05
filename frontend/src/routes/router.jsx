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
  Activate,
  ActivateMessage,
  ResendActivationEmail,
  ConfirmedPasswordReset,
  Contact,
  TrustCenter,
  Privacy,
  Abuse,
  Cookies,
} from "../pages";
import { MainLayout, AuthLayout } from "@/component/layout";
import { AppRoutes } from "./routes";
export const AppRouter = createBrowserRouter([
  {
    path: AppRoutes.home,
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: AppRoutes.contact,
        element: <Contact />,
      },
      {
        path: AppRoutes.trustCenter,
        element: <TrustCenter />,
      },
      {
        path: AppRoutes.privacy,
        element: <Privacy />,
      },
      {
        path: AppRoutes.abuse,
        element: <Abuse />,
      },
      {
        path: AppRoutes.cookies,
        element: <Cookies />,
      },
      {
        index: true,
        element: <Login />,
      },
      {
        path: AppRoutes.login,
        element: <Login />,
      },
      {
        path: AppRoutes.register,
        element: <Register />,
      },
      {
        path: AppRoutes.activate,
        element: <Activate />,
      },
      {
        path: AppRoutes.activateMessage,
        element: <ActivateMessage />,
      },
      {
        path: AppRoutes.resendActivationEmail,
        element: <ResendActivationEmail />,
      },
      {
        path: AppRoutes.resetPassword,
        element: <ResetPassword />,
      },
      {
        path: AppRoutes.confirmResetPassword,
        element: <ConfirmedPasswordReset />,
      },
      {
        path: AppRoutes.forgetPassword,
        element: <ForgetPassword />,
      },

      {
        path: AppRoutes.about,
        element: <About />,
      },
      {
        path: AppRoutes.dashboard,
        element: <Dashboard />,
      },
      {
        path: AppRoutes.space,
        element: <Space />,
      },
    ],
  },
  {
    path: AppRoutes.notFound,
    element: <NotFound />,
  },
]);
