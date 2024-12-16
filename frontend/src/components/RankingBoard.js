import React, { useEffect, useState } from 'react';
import scoreService from '../services/scoreService';

const RankingBoard = () => {
    const [ranking, setRanking] = useState([]); // 團隊排名數據
    const [error, setError] = useState(null);   // 錯誤訊息

    useEffect(() => {
        fetchRanking(); // 初始獲取排名

        // 設置定時刷新 (每 10 秒更新一次)
        const interval = setInterval(() => {
            fetchRanking();
        }, 10000);

        // 清除定時器
        return () => clearInterval(interval);
    }, []);

    // 從後端獲取團隊排名
    const fetchRanking = async () => {
        try {
            const response = await scoreService.getRanking();
            setRanking(response.data.ranking); // 假設後端回傳 { ranking: [...] }
            setError(null); // 清除錯誤訊息
        } catch (err) {
            console.error('Failed to fetch ranking:', err);
            setError('Failed to load ranking. Please try again later.');
        }
    };

    return (
        <div className="ranking-board-container">
            <h2>Team Ranking Board</h2>

            {error ? (
                <p className="error-message">{error}</p>
            ) : (
                <table className="ranking-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Team Name</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ranking.length > 0 ? (
                            ranking.map((team, index) => (
                                <tr key={team.teamId}>
                                    <td>{index + 1}</td>
                                    <td>{team.name}</td>
                                    <td>{team.score}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="3">No ranking data available</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default RankingBoard;
