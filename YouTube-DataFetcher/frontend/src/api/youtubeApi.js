import axios from 'axios';

const API_BASE = 'http://localhost:8000/youtube/';

export const fetchYouTubeData = (channelUrl) => {
  return axios.post(`${API_BASE}fetch-data/`, { channel_url: channelUrl });
};

export const exportExcelFile = () => {
  return axios.get(`${API_BASE}export-excel/`, { responseType: 'blob' });
};
