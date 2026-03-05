import "./App.css";
import { RouterProvider } from "react-router-dom";
import { AppRouter } from "./routes/router";
import { Toaster } from "react-hot-toast";

function App() {
  return (
    <>
      <Toaster position="top-right" reverseOrder={false} />
      <RouterProvider router={AppRouter} />
    </>
  );
}

export default App;
