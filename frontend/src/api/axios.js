import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cf_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 globally — clear token and redirect
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('cf_token')
      localStorage.removeItem('cf_user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

// ── Auth APIs ──────────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
  updateProfile: (data) => api.put('/api/auth/me', data),
}

// ── Career APIs ───────────────────────────────────────────────────
export const careerAPI = {
  analyze: (data) => api.post('/api/career/analyze', data),
  getHistory: (limit = 10) => api.get(`/api/career/history?limit=${limit}`),
}

// ── College APIs ──────────────────────────────────────────────────
export const collegeAPI = {
  predict: (data) => api.post('/api/college/predict', data),
  list: (params = {}) => api.get('/api/college/list', { params }),
}

// ── Resume APIs ───────────────────────────────────────────────────
export const resumeAPI = {
  analyze: (formData) => api.post('/api/resume/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000,
  }),
  getHistory: (limit = 10) => api.get(`/api/resume/history?limit=${limit}`),
}

// ── Chat APIs ─────────────────────────────────────────────────────
export const chatAPI = {
  sendMessage: (data) => api.post('/api/chat/message', data),
  getHistory: (limit = 20) => api.get(`/api/chat/history?limit=${limit}`),
  clearSession: (sessionId) => api.delete(`/api/chat/session/${sessionId}`),
}

export default api
