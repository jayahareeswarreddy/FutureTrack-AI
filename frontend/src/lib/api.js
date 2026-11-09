import axios from 'axios';

// Set REACT_APP_API_URL at build time to point the UI at a deployed backend.
// The default suits `uvicorn server:app --port 8010` from the backend folder.
const API_BASE_URL =
  process.env.REACT_APP_API_URL || 'http://localhost:8010';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
  headers: { 'Content-Type': 'application/json' },
});

export { API_BASE_URL };

/**
 * Turn an axios failure into one sentence a user can act on.
 *
 * Axios reports an unreachable host as a generic "Network Error", which tells
 * a visitor nothing, so the three cases worth distinguishing are named here:
 * backend down, backend slow, and backend answered with an error.
 */
function describe(error, fallback) {
  if (error.response) {
    const detail = error.response.data?.detail;
    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg;
    return `${fallback} (HTTP ${error.response.status})`;
  }
  if (error.code === 'ECONNABORTED') {
    return 'The backend took too long to respond. It may be waking from sleep — try again in a moment.';
  }
  return `Cannot reach the backend at ${API_BASE_URL}. Start it with "uvicorn server:app --port 8010" from the backend folder.`;
}

async function request(promise, fallback) {
  try {
    const { data } = await promise;
    return data;
  } catch (error) {
    throw new Error(describe(error, fallback));
  }
}

/* ----------------------------- careers ----------------------------- */

export const getCareers = () =>
  request(api.get('/careers'), 'Could not load careers');

export const getCareerById = (id) =>
  request(api.get(`/careers/${encodeURIComponent(id)}`), 'Could not load that career');

export const searchCareers = (query) =>
  request(api.get('/careers/search', { params: { q: query } }), 'Search failed');

export const getLearningRoadmap = (careerId) =>
  request(
    api.get(`/careers/${encodeURIComponent(careerId)}/roadmap`),
    'Could not load the roadmap'
  );

/* -------------------------- recommendations ------------------------- */

export const getRecommendations = (profile) =>
  request(api.post('/recommendations', profile), 'Could not generate recommendations');

/* ------------------------- taxonomy & health ------------------------ */

export const getHealth = () =>
  request(api.get('/health'), 'Health check failed');

export const getCategories = () =>
  request(api.get('/categories'), 'Could not load categories');

export const getSkills = (limit = 100) =>
  request(api.get('/skills', { params: { limit } }), 'Could not load the skill list');

/* --------------------------- skill gap ------------------------------ */

export const getSkillGap = ({ careerId, skills, experienceYears = 0 }) =>
  request(
    api.post('/skill-gap', {
      career_id: careerId,
      skills,
      experience_years: experienceYears,
    }),
    'Skill-gap analysis failed'
  );

/* ---------------------------- profiles ------------------------------ */

export const saveProfile = (profile) =>
  request(api.post('/profiles', profile), 'Could not save the profile');

export const getProfile = (profileId) =>
  request(
    api.get(`/profiles/${encodeURIComponent(profileId)}`),
    'Could not load that profile'
  );


/* --------------------------- learning resources --------------------- */

export const getCareerResources = (careerId) =>
  request(
    api.get(`/careers/${encodeURIComponent(careerId)}/resources`),
    'Could not load learning resources'
  );

export const getSkillResources = (skill) =>
  request(api.get('/resources', { params: { skill } }), 'Could not load resources');

export default api;
