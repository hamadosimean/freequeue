import "./App.css";
import { RouterProvider } from "react-router-dom";
import { AppRoutes } from "./routes/router";
function App() {
  return <RouterProvider router={AppRoutes} />;
}

export default App;
