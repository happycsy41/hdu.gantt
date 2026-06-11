import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || ''

const api = axios.create({ baseURL: BASE })

// Attach JWT to every request
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// Auto-logout on 401
api.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.reload()
    }
    return Promise.reject(err)
  }
)

// ── Auth ──────────────────────────────────────────────────────────────────
export const register = (email, username, password) =>
  api.post('/api/auth/register', { email, username, password })

export const login = async (username, password) => {
  const form = new URLSearchParams({ username, password })
  const { data } = await api.post('/api/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
  localStorage.setItem('token', data.access_token)
  return data
}

export const getMe = () => api.get('/api/auth/me').then(r => r.data)

export const logout = () => localStorage.removeItem('token')

// ── Projects ──────────────────────────────────────────────────────────────
export const getProjects  = ()        => api.get('/api/projects/').then(r => r.data)
export const createProject = body     => api.post('/api/projects/', body).then(r => r.data)
export const updateProject = (id, body) => api.put(`/api/projects/${id}`, body).then(r => r.data)
export const deleteProject = id       => api.delete(`/api/projects/${id}`)

// ── Capacity ──────────────────────────────────────────────────────────────
export const getCapacity    = ()       => api.get('/api/capacity/').then(r => r.data)
export const upsertCapacity = settings => api.put('/api/capacity/', { settings }).then(r => r.data)
