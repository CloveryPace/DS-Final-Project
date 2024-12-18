import React, { useState } from "react";
import TeamForm from "../components/TeamForm";
import CheckInButton from "../components/CheckInButton";
import { useNavigate } from "react-router-dom";

const HomePage = ({ username }) => {
  const [formType, setFormType] = useState("create");
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>歡迎, {username || "用戶"}</h1>

      {/* 創建/加入團隊切換按鈕 */}
      <div style={styles.buttonContainer}>
        <button
          onClick={() => setFormType("create")}
          style={formType === "create" ? styles.activeButton : styles.button}
        >
          創建團隊
        </button>
        <button
          onClick={() => setFormType("join")}
          style={formType === "join" ? styles.activeButton : styles.button}
        >
          加入團隊
        </button>
      </div>

      {/* 創建/加入團隊表單 */}
      <div style={styles.formContainer}>
        <TeamForm formType={formType} username={username} />
      </div>

      {/* 打卡按鈕 */}
      <div style={styles.checkInContainer}>
        <h3>進行每日打卡</h3>
        <CheckInButton username={username} />
      </div>

      {/* 查看即時排名按鈕 */}
      <div style={styles.rankingContainer}>
        <button onClick={() => navigate("/ranking")} style={styles.button}>
          查看即時排名
        </button>
      </div>
    </div>
  );
};

export default HomePage;

const styles = {
  container: {
    textAlign: "center",
    marginTop: "50px",
    fontFamily: "Arial, sans-serif",
  },
  heading: {
    marginBottom: "20px",
    color: "#333",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    gap: "10px",
    marginBottom: "20px",
  },
  button: {
    padding: "10px 20px",
    backgroundColor: "#ddd",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  activeButton: {
    padding: "10px 20px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  formContainer: {
    marginBottom: "30px",
  },
  checkInContainer: {
    marginTop: "30px",
  },
  rankingContainer: {
    marginTop: "20px",
  },
};
