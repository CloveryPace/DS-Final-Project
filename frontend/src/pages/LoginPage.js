import React from "react";
import AuthForm from "../components/AuthForm";
import { login } from "../api/auth";

const LoginPage = () => {
  const handleLogin = async ({ email, password }) => {
    try {
      const response = await login(email, password);
      alert(response.message);
    } catch (error) {
      alert(error.error || "Login failed");
    }
  };

  return <AuthForm onSubmit={handleLogin} buttonText="Login" />;
};

export default LoginPage;
