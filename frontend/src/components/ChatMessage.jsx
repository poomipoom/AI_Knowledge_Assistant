import { Bot, User } from 'lucide-react';
import './ChatMessage.css';

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="avatar">
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div className="message-content">
        <div className="message-bubble">
          {message.content}
        </div>
        
        {message.citations && message.citations.length > 0 && (
          <div className="citations">
            <span className="citation-label">Sources:</span>
            {message.citations.map((cite, i) => (
              <span key={i} className="citation-chip" title={cite.content}>
                {cite.document_name}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
