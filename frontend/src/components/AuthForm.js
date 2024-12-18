import React, { useState } from "react";

const AuthForm = ({ onSubmit, buttonText }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ username, email, password });
  };

  return (
    <form onSubmit={handleSubmit} style={styles.formContainer}>
      <h2>{buttonText}</h2>

      {/* enter username */}
      {buttonText === "Register" && (
        <div style={styles.inputContainer}>
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
      )}

      {/* enter email */}
      <div style={styles.inputContainer}>
        <label>Email</label>
        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>

      {/* enter password */}
      <div style={styles.inputContainer}>
        <label>Password</label>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>

      {/* submit */}
      <button type="submit" style={styles.button}>
        {buttonText}
      </button>
    </form>
  );
};

export default AuthForm;

const styles = {
  formContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "20px",
    width: "300px",
    margin: "0 auto",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  inputContainer: {
    display: "flex",
    flexDirection: "column",
    width: "100%",
  },
  button: {
    padding: "10px 15px",
    border: "none",
    borderRadius: "4px",
    backgroundColor: "#4CAF50",
    color: "white",
    cursor: "pointer",
    marginTop: "10px",
    fontSize: "16px",
  },
};
