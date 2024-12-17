import axios from 'axios';


const API_URL = 'http://localhost:5001/api/score';

// 上傳打卡照片
const uploadPost = (formData) => {
    return axios.post(`${API_URL}/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

// 獲取團隊積分排名
const getRanking = () => {
    return axios.get(`${API_URL}/ranking`);
};

// 獲取單個團隊的積分詳情
const getTeamScore = (teamId) => {
    return axios.get(`${API_URL}/${teamId}/score`);
};

export default {
    uploadPost,
    getRanking,
    getTeamScore,
};
