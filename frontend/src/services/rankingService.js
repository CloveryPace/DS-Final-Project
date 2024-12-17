import axios from 'axios';

const API_URL = 'localhost:5002';

// 獲取團隊積分排名
const getRanking = () => {
	return axios.get(`${API_URL}/ranking`);
};

const rankingService = { getRanking };

export default rankingService;
