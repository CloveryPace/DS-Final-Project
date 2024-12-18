import React from "react";
import AuthForm from "../components/AuthForm";
import { register } from "../api/auth";

const RegisterPage = () => {
  const handleRegister = async ({ username, email, password }) => {
    try {
      const response = await register(username, email, password);
      alert(response.message);
    } catch (error) {
      alert(error.error || "Registration failed");
    }
  };

  return <AuthForm onSubmit={handleRegister} buttonText="Register" />;
};

export default RegisterPage;
