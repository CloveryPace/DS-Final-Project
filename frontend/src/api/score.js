import axios from 'axios';

const API_URL = 'http://backend:5001/api/score';

export const updatePostedAt = async (username) => {
    try {
        const response = await axios.post(`${API_URL}/update`, { username });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : { error: "Network error" };
    }
};

export const calculateTeamScore = async (teamName) => {
    try {
        const response = await axios.post(`${API_URL}/calculate_score`, { team_name: teamName });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : { error: "Network error" };
    }
};

export default {
    updatePostedAt,
    calculateTeamScore,
};
