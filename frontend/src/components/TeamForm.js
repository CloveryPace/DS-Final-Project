import React, { useState } from "react";
import { createTeam, joinTeam } from "../api/team";

const TeamForm = ({ formType, username }) => {
  const [teamName, setTeamName] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      if (formType === "create") {
        const response = await createTeam(teamName);
        setMessage(response.message);
      } else if (formType === "join") {
        if (!username) {
          setMessage("Username is required to join a team");
          return;
        }
        const response = await joinTeam(teamName, username);
        setMessage(response.message);
      }
      setTeamName("");
    } catch (error) {
      setMessage(error.response?.data?.error || "Something went wrong!");
    }
  };

  return (
    <div style={styles.container}>
      <h2>{formType === "create" ? "創建團隊" : "加入團隊"}</h2>
      <form onSubmit={handleSubmit}>
        <div style={styles.inputContainer}>
          <label>Team name：</label>
          <input
            type="text"
            value={teamName}
            onChange={(e) => setTeamName(e.target.value)}
            placeholder="Enter team name"
            required
            style={styles.input}
          />
        </div>
        <button type="submit" style={styles.button}>
          {formType === "create" ? "創建" : "加入"}
        </button>
      </form>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

export default TeamForm;

// 樣式設置
const styles = {
  container: {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "20px",
    width: "300px",
    margin: "0 auto",
    textAlign: "center",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
  },
  inputContainer: {
    marginBottom: "15px",
    textAlign: "left",
  },
  input: {
    width: "100%",
    padding: "8px",
    marginTop: "5px",
    borderRadius: "4px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 15px",
    fontSize: "16px",
    cursor: "pointer",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "4px",
    marginTop: "10px",
  },
  message: {
    marginTop: "15px",
    color: "green",
  },
};
