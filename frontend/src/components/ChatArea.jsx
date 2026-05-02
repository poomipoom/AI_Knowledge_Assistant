import { Send, Loader2 } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import ChatMessage from './ChatMessage';
import './ChatArea.css';

export default function ChatArea({ session }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Load chat history
  useEffect(() => {
    if (session?.id) {
      api.getSession(session.id).then(data => {
        if (data.messages) {
          setMessages(data.messages);
        }
      });
    }
  }, [session]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await api.chat(session.id, userMessage.content);
      setMessages(prev => [...prev, { ...response.message, citations: response.citations }]);
    } catch (error) {
      console.error("Chat error", error);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-area glass-panel">
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <p>Start a conversation with your AI Assistant.</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))
        )}
        {isTyping && (
          <div className="message assistant">
            <div className="message-bubble typing">
              <Loader2 className="spinner" size={20} />
              <span>Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-area" onSubmit={handleSend}>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="chat-input"
        />
        <button type="submit" className="btn btn-send" disabled={isTyping || !input.trim()}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
