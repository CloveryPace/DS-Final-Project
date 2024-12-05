import React, { useEffect, useState } from 'react';

function App() {
	const [rankings, setRankings] = useState([]); // 保存排名數據

	useEffect(() => {
		// 創建 WebSocket 連接
		const socket = new WebSocket('ws://websocket_server:6789'); // 使用 WebSocket 服務名稱

		socket.onopen = () => {
			console.log('WebSocket connection established.');
		};

		socket.onmessage = (event) => {
			// 假設 WebSocket 發送的數據是 JSON 格式的積分排名
			const data = JSON.parse(event.data);
			setRankings(data); // 更新積分排名數據
		};

		socket.onerror = (error) => {
			console.error('WebSocket error:', error);
		};

		socket.onclose = () => {
			console.log('WebSocket connection closed.');
		};

		// 清理 WebSocket 連接
		return () => {
			socket.close();
		};
	}, []); // 空依賴陣列表示這個 effect 只會在組件掛載時執行一次

	return (
		<div className="App">
			<h1>團隊積分排名</h1>
			{rankings.length === 0 ? (
				<p>等待積分排名更新...</p>
			) : (
				<ul>
					{rankings.map((team, index) => (
						<li key={index}>
							{team.team_id}: {team.score} 分
						</li>
					))}
				</ul>
			)}
		</div>
	);
}

export default App;
