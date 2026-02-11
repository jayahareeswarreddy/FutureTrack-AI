import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCareers = async () => {
  try {
    const response = await api.get('/careers');
    console.log('API Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching careers:', error);
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      throw new Error('Backend server is not running. Please start it on port 8000.');
    }
    throw error;
  }
};

export const getCareerById = async (id) => {
  try {
    const response = await api.get(`/careers/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching career:', error);
    throw error;
  }
};

export const searchCareers = async (query) => {
  try {
    const response = await api.get('/careers/search', { params: { q: query } });
    return response.data;
  } catch (error) {
    console.error('Error searching careers:', error);
    throw error;
  }
};

export const getRecommendations = async (profile) => {
  try {
    const response = await api.post('/recommendations', profile);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    // Return fallback recommendations if API fails
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      throw new Error('Backend server is not running. Please start the backend server on port 8000.');
    }
    throw error;
  }
};

export const getLearningRoadmap = async (careerId) => {
  try {
    const response = await api.get(`/careers/${careerId}/roadmap`);
    return response.data;
  } catch (error) {
    console.error('Error fetching roadmap:', error);
    throw error;
  }
};

export default api;
