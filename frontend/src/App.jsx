import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import DocumentPanel from './components/DocumentPanel';
import ChatArea from './components/ChatArea';
import './App.css';

function App() {
  const [currentSession, setCurrentSession] = useState(null);

  return (
    <div className="app-container">
      <Sidebar 
        currentSession={currentSession} 
        onSelectSession={setCurrentSession} 
      />
      
      <main className="main-workspace">
        {currentSession ? (
          <>
            <DocumentPanel session={currentSession} />
            <ChatArea session={currentSession} />
          </>
        ) : (
          <div className="empty-state glass-panel">
            <h2>Welcome to AI Knowledge Assistant</h2>
            <p>Select a session from the sidebar or create a new one to begin.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
