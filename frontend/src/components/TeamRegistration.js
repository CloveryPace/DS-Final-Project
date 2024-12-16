import React, { useState, useEffect } from 'react';
import teamService from '../services/teamService';

const TeamRegistration = () => {
    const [teams, setTeams] = useState([]); // 所有團隊
    const [newTeamName, setNewTeamName] = useState(''); // 新團隊名稱
    const [selectedTeam, setSelectedTeam] = useState(''); // 已選擇加入的團隊ID
    const [joinedTeams, setJoinedTeams] = useState([]); // 會員已加入的團隊

    // 初始化時獲取所有團隊列表
    useEffect(() => {
        fetchTeams();
    }, []);

    const fetchTeams = async () => {
        try {
            const response = await teamService.getTeams();
            setTeams(response.data);
        } catch (error) {
            console.error('Failed to fetch teams:', error);
        }
    };

    // 處理創建新團隊
    const handleCreateTeam = async () => {
        if (!newTeamName) return alert('Team name cannot be empty!');
        try {
            const response = await teamService.createTeam(newTeamName);
            setJoinedTeams([...joinedTeams, response.data]); // 添加到已加入團隊
            setTeams([...teams, response.data]); // 更新團隊列表
            setNewTeamName(''); // 清空輸入框
        } catch (error) {
            console.error('Failed to create team:', error);
        }
    };

    // 處理加入團隊
    const handleJoinTeam = async () => {
        if (!selectedTeam) return alert('Please select a team to join.');
        try {
            const response = await teamService.joinTeam(selectedTeam);
            setJoinedTeams([...joinedTeams, response.data]); // 添加到已加入團隊
        } catch (error) {
            console.error('Failed to join team:', error);
        }
    };

    return (
        <div className="team-registration-container">
            <h2>Team Registration</h2>

            {/* 創建新團隊 */}
            <div className="create-team">
                <h3>Create a New Team</h3>
                <input
                    type="text"
                    placeholder="Enter team name"
                    value={newTeamName}
                    onChange={(e) => setNewTeamName(e.target.value)}
                />
                <button onClick={handleCreateTeam}>Create Team</button>
            </div>

            {/* 加入已存在的團隊 */}
            <div className="join-team">
                <h3>Join an Existing Team</h3>
                <select
                    value={selectedTeam}
                    onChange={(e) => setSelectedTeam(e.target.value)}
                >
                    <option value="">Select a team</option>
                    {teams.map((team) => (
                        <option key={team.id} value={team.id}>
                            {team.name}
                        </option>
                    ))}
                </select>
                <button onClick={handleJoinTeam}>Join Team</button>
            </div>

            {/* 顯示已加入的團隊 */}
            <div className="joined-teams">
                <h3>Your Teams</h3>
                <ul>
                    {joinedTeams.map((team) => (
                        <li key={team.id}>{team.name}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default TeamRegistration;
