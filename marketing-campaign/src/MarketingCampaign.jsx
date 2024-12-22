import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { UserCircle, Upload, Trophy, Users } from 'lucide-react';
import { socket } from './socket';

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const MarketingCampaign = () => {
	const [currentPage, setCurrentPage] = useState('home');
	const [user, setUser] = useState(null);
	const [teams, setTeams] = useState([]);
	const [topTeams, setTopTeams] = useState([]);
	const [formData, setFormData] = useState({
		username: '',
		email: '',
		password: '',
		teamName: '',
	});
	const [isConnected, setIsConnected] = useState(socket.connected);

	useEffect(() => {
		// 載入所有團隊
		fetchTeams();
		// 初次載入排行榜
		// fetchLeaderboard();

		// 設置定期更新排行榜(每5秒)
		// const intervalId = setInterval(fetchLeaderboard, 5000);

		// Cleanup interval on component unmount
		// return () => clearInterval(intervalId);
		// Establish WebSocket connection
		function onConnect() {
			setIsConnected(true);
		}

		function onDisconnect() {
			setIsConnected(false);
		}

		function onUpdateLeaderboard(value) {
			setTopTeams(value);
		}

		socket.on('connect', onConnect);
		socket.on('disconnect', onDisconnect);
		socket.on('update_leaderboard', onUpdateLeaderboard);

		return () => {
			socket.off('connect', onConnect);
			socket.off('disconnect', onDisconnect);
			socket.off('update_leaderboard', onUpdateLeaderboard);
		};

		// const socket = new WebSocket('http://localhost:5000');

		// // Handle WebSocket message event
		// socket.onmessage = (event) => {
		// 	const data = JSON.parse(event.data);
		// 	if (data.type === 'update_leaderboard') {
		// 		setTopTeams(data.topTeams); // Assuming the server sends updated leaderboard data
		// 	}
		// };

		// // Cleanup WebSocket on component unmount
		// return () => {
		// 	socket.close();
		// };
	}, []);

	// const fetchLeaderboard = async () => {
	// 	try {
	// 		const response = await fetch(`${BASE_URL}/api/leaderboard`, {
	// 			method: 'GET',
	// 		});
	// 		if (response.ok) {
	// 			const data = await response.json();
	// 			setTopTeams(data);
	// 		}
	// 	} catch (error) {
	// 		console.error('Error fetching leaderboard:', error);
	// 	}
	// };

	const fetchTeams = async () => {
		try {
			const response = await fetch(`${BASE_URL}/api/team/`);
			console.log(response);
			const data = await response.json();
			setTeams(data.teams);
		} catch (error) {
			console.error('Error fetching teams:', error);
		}
	};

	const handleRegister = async (e) => {
		e.preventDefault();
		try {
			const response = await fetch(`${BASE_URL}/api/auth/register`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					username: formData.username,
					email: formData.email,
					password: formData.password,
				}),
			});

			if (response.ok) {
				const data = await response.json();
				alert('註冊成功！');
				setUser(data);
				setCurrentPage('home');
			} else {
				const error = await response.json();
				alert(error.error);
			}
		} catch (error) {
			console.error('Registration error:', error);
		}
	};

	const handleLogin = async (e) => {
		e.preventDefault();
		try {
			const response = await fetch(`${BASE_URL}/api/auth/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					email: formData.email,
					password: formData.password,
				}),
			});

			if (response.ok) {
				const data = await response.json();
				setUser(data.user);
				setCurrentPage('home');
			} else {
				const error = await response.json();
				alert(error.error);
			}
		} catch (error) {
			console.error('Login error:', error);
		}
	};

	const handleCreateTeam = async (e) => {
		e.preventDefault();
		try {
			const response = await fetch(`${BASE_URL}/api/team/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					team_name: formData.teamName,
				}),
			});

			if (response.ok) {
				alert('團隊建立成功！');
				fetchTeams();
				setFormData({ ...formData, teamName: '' });
			} else {
				const error = await response.json();
				alert(error.error);
			}
		} catch (error) {
			console.error('Team creation error:', error);
		}
	};

	const handleJoinTeam = async (teamName) => {
		if (!user) {
			alert('請先登入');
			return;
		}

		try {
			const response = await fetch(`${BASE_URL}/api/team/${teamName}/members`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					username: user.username,
				}),
			});

			if (response.ok) {
				alert(`成功加入團隊 ${teamName}！`);
			} else {
				const error = await response.json();
				alert(error.error);
			}
		} catch (error) {
			console.error('Team joining error:', error);
		}
	};

	const handlePost = async () => {
		if (!user) {
			alert('請先登入');
			return;
		}

		try {
			const response = await fetch(`${BASE_URL}/api/auth/post`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					username: user.username,
				}),
			});

			if (response.ok) {
				alert('打卡成功！');
				// 立即更新排行榜
				// await fetchLeaderboard();
			} else {
				const error = await response.json();
				alert(error.error);
			}
		} catch (error) {
			console.error('Posting error:', error);
		}
	};

	return (
		<div className="min-h-screen bg-gray-50">
			<nav className="bg-white shadow-sm">
				<div className="max-w-7xl mx-auto px-4">
					<div className="flex justify-between h-16">
						<div className="flex space-x-8">
							<Button
								variant="ghost"
								className="inline-flex items-center"
								onClick={() => setCurrentPage('home')}>
								<Trophy className="h-5 w-5 mr-2" />
								揪團按讚活動
							</Button>

							<div className="flex space-x-4">
								{!user ? (
									<Button
										variant="ghost"
										onClick={() => setCurrentPage('register')}>
										<UserCircle className="h-5 w-5 mr-2" />
										會員註冊/登入
									</Button>
								) : (
									<span className="flex items-center">
										歡迎, {user.username}
									</span>
								)}
								<Button variant="ghost" onClick={() => setCurrentPage('team')}>
									<Users className="h-5 w-5 mr-2" />
									團隊管理
								</Button>
								<Button
									variant="ghost"
									onClick={() => setCurrentPage('upload')}>
									<Upload className="h-5 w-5 mr-2" />
									上傳打卡
								</Button>
							</div>
						</div>
					</div>
				</div>
			</nav>

			<main className="max-w-7xl mx-auto py-6 px-4">
				<Card className="mb-6">
					<CardHeader>
						<CardTitle>即時排行榜 (Top 20)</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-2">
							{topTeams.map((team, index) => (
								<div
									key={index}
									className="flex justify-between items-center p-2 bg-gray-50 rounded">
									<span className="font-medium">{index + 1}.</span>
									<span className="font-medium flex-grow text-left">
										{` ${team.team_name}`}
									</span>
									<span className="text-gray-600">{team.score}</span>
								</div>
							))}
						</div>
					</CardContent>
				</Card>

				<div className="mt-6">
					{currentPage === 'register' && (
						<Card>
							<CardHeader>
								<CardTitle>會員註冊/登入</CardTitle>
							</CardHeader>
							<CardContent className="space-y-4">
								<Input
									placeholder="使用者名稱"
									value={formData.username}
									onChange={(e) =>
										setFormData({ ...formData, username: e.target.value })
									}
								/>
								<Input
									placeholder="電子郵件"
									type="email"
									value={formData.email}
									onChange={(e) =>
										setFormData({ ...formData, email: e.target.value })
									}
								/>
								<Input
									placeholder="密碼"
									type="password"
									value={formData.password}
									onChange={(e) =>
										setFormData({ ...formData, password: e.target.value })
									}
								/>
								<Button className="w-full" onClick={handleLogin}>
									登入
								</Button>
								<Button
									variant="outline"
									className="w-full"
									onClick={handleRegister}>
									註冊新帳號
								</Button>
							</CardContent>
						</Card>
					)}

					{currentPage === 'team' && (
						<Card>
							<CardHeader>
								<CardTitle>團隊管理</CardTitle>
							</CardHeader>
							<CardContent className="space-y-4">
								<div className="space-y-4">
									<Input
										placeholder="團隊名稱"
										value={formData.teamName}
										onChange={(e) =>
											setFormData({ ...formData, teamName: e.target.value })
										}
									/>
									<Button className="w-full" onClick={handleCreateTeam}>
										建立新團隊
									</Button>
								</div>
								<div className="mt-6">
									<h3 className="text-lg font-medium mb-4">現有團隊</h3>
									<div className="space-y-2">
										{teams.map((team, index) => (
											<div
												key={index}
												className="flex justify-between items-center p-2 bg-gray-50 rounded">
												<span>{team.team_name}</span>
												<Button onClick={() => handleJoinTeam(team.team_name)}>
													加入團隊
												</Button>
											</div>
										))}
									</div>
								</div>
							</CardContent>
						</Card>
					)}

					{currentPage === 'upload' && (
						<Card>
							<CardHeader>
								<CardTitle>上傳打卡照片</CardTitle>
							</CardHeader>
							<CardContent className="space-y-4">
								<div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
									<Upload className="mx-auto h-12 w-12 text-gray-400" />
									<p className="mt-2">點擊或拖曳檔案至此處上傳</p>
								</div>
								<Button className="w-full" onClick={handlePost}>
									確認打卡
								</Button>
							</CardContent>
						</Card>
					)}
				</div>
			</main>
		</div>
	);
};

export default MarketingCampaign;
