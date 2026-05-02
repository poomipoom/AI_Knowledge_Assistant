import { PlusCircle, MessageSquare, Trash2, Edit2, Check, X } from 'lucide-react';
import { useState, useEffect } from 'react';
import { api } from '../services/api';
import './Sidebar.css';

export default function Sidebar({ currentSession, onSelectSession }) {
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");

  useEffect(() => {
    api.getSessions().then(data => {
      setSessions(data || []);
      // If there are sessions and no active session, select the most recent one
      if (data && data.length > 0 && !currentSession) {
        onSelectSession(data[0]);
      }
    }).catch(err => console.error("Failed to fetch sessions", err));
  }, []);

  const handleNewSession = async () => {
    setIsLoading(true);
    try {
      const newSession = await api.createSession(`Session ${sessions.length + 1}`);
      setSessions([newSession, ...sessions]);
      onSelectSession(newSession);
    } catch (error) {
      console.error("Failed to create session", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteSession = async (e, sessionId) => {
    e.stopPropagation(); // Prevent triggering the select session click
    try {
      await api.deleteSession(sessionId);
      setSessions(sessions.filter(s => s.id !== sessionId));
      if (currentSession?.id === sessionId) {
        onSelectSession(null);
      }
    } catch (error) {
      console.error("Failed to delete session", error);
    }
  };

  const startEditing = (e, session) => {
    e.stopPropagation();
    setEditingId(session.id);
    setEditTitle(session.title);
  };

  const cancelEditing = (e) => {
    e.stopPropagation();
    setEditingId(null);
  };

  const saveEditing = async (e, sessionId) => {
    e.stopPropagation();
    if (!editTitle.trim()) {
      setEditingId(null);
      return;
    }
    
    try {
      const updated = await api.updateSession(sessionId, editTitle);
      setSessions(sessions.map(s => s.id === sessionId ? updated : s));
      if (currentSession?.id === sessionId) {
        onSelectSession(updated);
      }
      setEditingId(null);
    } catch (error) {
      console.error("Failed to update session", error);
    }
  };

  const handleKeyDown = (e, sessionId) => {
    if (e.key === 'Enter') saveEditing(e, sessionId);
    if (e.key === 'Escape') cancelEditing(e);
  };

  return (
    <div className="sidebar glass-panel">
      <div className="sidebar-header">
        <h1 className="logo">🧠 K-Assistant</h1>
        <button className="btn w-full" onClick={handleNewSession} disabled={isLoading}>
          <PlusCircle size={18} /> New Session
        </button>
      </div>
      
      <div className="session-list">
        {sessions.map(session => (
          <div 
            key={session.id} 
            className={`session-item ${currentSession?.id === session.id ? 'active' : ''}`}
            onClick={() => { if(editingId !== session.id) onSelectSession(session); }}
          >
            <MessageSquare size={16} className="session-icon" />
            
            {editingId === session.id ? (
              <div className="edit-container" onClick={e => e.stopPropagation()}>
                <input 
                  type="text" 
                  className="edit-input"
                  value={editTitle}
                  onChange={e => setEditTitle(e.target.value)}
                  onKeyDown={e => handleKeyDown(e, session.id)}
                  autoFocus
                />
                <button className="btn-icon success-btn" onClick={e => saveEditing(e, session.id)}>
                  <Check size={14} />
                </button>
                <button className="btn-icon cancel-btn" onClick={cancelEditing}>
                  <X size={14} />
                </button>
              </div>
            ) : (
              <>
                <span className="session-title">{session.title}</span>
                <div className="session-actions">
                  <button 
                    className="btn-icon edit-btn" 
                    onClick={(e) => startEditing(e, session)}
                    title="Rename session"
                  >
                    <Edit2 size={14} />
                  </button>
                  <button 
                    className="btn-icon delete-btn" 
                    onClick={(e) => handleDeleteSession(e, session.id)}
                    title="Delete session"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
