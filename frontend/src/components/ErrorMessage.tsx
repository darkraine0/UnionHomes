import React from "react";

const ErrorMessage: React.FC<{ message: string }> = ({ message }) => (
  <div className="text-center text-red-500 font-semibold text-lg py-6">{message}</div>
);

export default ErrorMessage; 