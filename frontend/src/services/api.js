// In development, use local backend port. In production, use '/api' which Nginx proxies to the backend.
const API_URL = import.meta.env.MODE === 'development' ? 'http://localhost:8000' : '/api';

export const api = {
  createSession: async (title = 'New Session') => {
    const res = await fetch(`${API_URL}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });
    return res.json();
  },
  
  getSessions: async () => {
    const res = await fetch(`${API_URL}/sessions`);
    return res.json();
  },
  
  getSession: async (sessionId) => {
    const res = await fetch(`${API_URL}/sessions/${sessionId}`);
    return res.json();
  },
  
  deleteSession: async (sessionId) => {
    const res = await fetch(`${API_URL}/sessions/${sessionId}`, {
      method: 'DELETE',
    });
    return res.json();
  },

  updateSession: async (sessionId, title) => {
    const res = await fetch(`${API_URL}/sessions/${sessionId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });
    return res.json();
  },
  
  uploadDocument: async (sessionId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const res = await fetch(`${API_URL}/sessions/${sessionId}/documents`, {
      method: 'POST',
      body: formData,
    });
    return res.json();
  },
  
  chat: async (sessionId, content) => {
    const res = await fetch(`${API_URL}/sessions/${sessionId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    return res.json();
  }
};
