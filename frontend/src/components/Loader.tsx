import React from "react";

const Loader: React.FC = () => (
  <div className="flex justify-center items-center py-8">
    <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-500 border-b-4 border-cyan-400"></div>
    <span className="ml-4 text-blue-500 font-semibold text-lg">Loading...</span>
  </div>
);

export default Loader; 