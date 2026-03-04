import React from "react";
import { PropagateLoader } from "react-spinners";

function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center h-screen">
      <PropagateLoader color="#36d7b7" size={15} />
    </div>
  );
}

export default LoadingSpinner;
