import React from "react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/login");
  };

  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <div style={styles.container}>
      <h1>Group Like Marketing Campaign</h1>
      <p>Please select sign in / sign up:</p>
      <div style={styles.buttonContainer}>
        <button onClick={handleLogin} style={styles.button}>
          Login
        </button>
        <button onClick={handleRegister} style={styles.button}>
          Register
        </button>
      </div>
    </div>
  );
};

export default LandingPage;

const styles = {
  container: {
    textAlign: "center",
    marginTop: "50px",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    gap: "10px",
    marginTop: "20px",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    cursor: "pointer",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "4px",
  },
};
