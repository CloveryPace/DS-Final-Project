import axios from 'axios';

const API_URL = 'http://backend:5001/api/team';

export const createTeam = async (teamName) => {
    return await axios.post(`${API_URL}/create`, { team_name: teamName });
  };

export const joinTeam = (teamName, username) => {
    return axios.post(`${API_URL}/${teamName}/add_member`, { username });
};

export default {
  createTeam,
  joinTeam,
};