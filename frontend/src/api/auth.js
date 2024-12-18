import axios from 'axios';

const API_URL = 'login: "https://checkinservice-126965479140.asia-east1.run.app/api/';

export const register = (username, email, password) => {
    return axios.post(`${API_URL}/register`, { username, email, password });
};

export const login = (email, password) => {
    return axios.post(`${API_URL}/login`, { email, password });
};

export default {
    register,
    login,
};
