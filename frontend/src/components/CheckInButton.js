import React from "react";
import { updatePostedAt } from "../api/score";

const CheckInButton = ({ username }) => {
  const handleCheckIn = async () => {
    try {
      const response = await updatePostedAt(username);
      alert(`打卡成功！打卡時間: ${response.posted_at}`);
    } catch (error) {
      console.error("打卡失敗:", error);
      alert(error.error || "打卡失敗，請稍後再試！");
    }
  };

  return (
    <button onClick={handleCheckIn} style={styles.button}>
      打卡
    </button>
  );
};

export default CheckInButton;

const styles = {
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    cursor: "pointer",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "5px",
    marginTop: "20px",
    transition: "background-color 0.3s",
  },
};
