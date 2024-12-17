import React, { useEffect, useState } from 'react';
import rankingService from '../services/rankingService';
import { socket } from '../socket';

const RankingBoard = () => {
	const [isConnected, setIsConnected] = useState(socket.connected);
	const [ranking, setRanking] = useState([]); // 團隊排名數據
	const [error, setError] = useState(null); // 錯誤訊息

	useEffect(() => {
		// const fetchRanking = async () => {
		// 	try {
		// 		const response = await rankingService.getRanking();
		// 		console.log(response);
		// 		setRanking(response.data);
		// 	} catch (err) {
		// 		console.error(err); // Log the error object
		// 		setError('Failed to fetch ranking data');
		// 	}
		// };

		// fetchRanking();

		const onConnect = () => {
			setIsConnected(true);
		};

		const onDisconnect = () => {
			setIsConnected(false);
		};

		const onUpdateLeaderboard = (data) => {
			console.log(data);
			setRanking(data);
		};

		socket.on('connect', onConnect);
		socket.on('disconnect', onDisconnect);
		socket.on('update_leaderboard', onUpdateLeaderboard);

		return () => {
			socket.off('connect', onConnect);
			socket.off('disconnect', onDisconnect);
			socket.off('update_leaderboard', onUpdateLeaderboard);
		};
	}, []);

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
								<tr key={team.name}>
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
