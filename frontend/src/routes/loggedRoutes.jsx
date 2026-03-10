import { AppRoutes } from "@/routes/routes";
import { FaUser } from "react-icons/fa";
import { FaBuilding, FaHome, FaCog } from "react-icons/fa";

export const loggedRoutes = [
  {
    to: AppRoutes.company,
    label: "Company",
    icon: <FaHome />,
  },
  {
    to: AppRoutes.agency,
    label: "Agency",
    icon: <FaBuilding />,
  },
  {
    to: AppRoutes.dashboard,
    label: "Dashboard",
    icon: <FaUser />,
  },
  {
    to: AppRoutes.settings,
    label: "Settings",
    icon: <FaCog />,
  },
];
