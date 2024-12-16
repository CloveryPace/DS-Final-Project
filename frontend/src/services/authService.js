import axios from 'axios';

const API_URL = 'https://localhost:5000/auth';

// 登入 API
const login = (email, password) => {
    return axios.post(`${API_URL}/login`, { email, password });
};

// 註冊 API
const register = (email, password) => {
    return axios.post(`${API_URL}/register`, { email, password });
};

// 登出 API
const logout = () => {
    localStorage.removeItem('user'); // 清除本地儲存的登入資訊
};

const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem('user')); // 獲取當前用戶資訊
};

export default {
    login,
    register,
    logout,
    getCurrentUser,
};
