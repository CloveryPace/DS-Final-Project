import axios from 'axios';

const API_URL = 'https://localhost:5000/teams';

// 獲取所有團隊列表
const getTeams = () => {
    return axios.get(`${API_URL}`);
};

// 創建新團隊
const createTeam = (teamName) => {
    return axios.post(`${API_URL}/create`, { name: teamName });
};

// 加入團隊
const joinTeam = (teamId) => {
    return axios.post(`${API_URL}/join`, { teamId });
};

// 獲取用戶加入的團隊
const getUserTeams = (userId) => {
    return axios.get(`${API_URL}/user/${userId}/teams`);
};

export default {
    getTeams,
    createTeam,
    joinTeam,
    getUserTeams,
};
