import { FileUp, FileText } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import { api } from '../services/api';
import './DocumentPanel.css';

export default function DocumentPanel({ session }) {
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (session?.id) {
      api.getSession(session.id).then(data => {
        if (data.documents) {
          setDocuments(data.documents);
        }
      });
    }
  }, [session]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    try {
      const newDoc = await api.uploadDocument(session.id, file);
      setDocuments([...documents, newDoc]);
    } catch (error) {
      console.error("Upload failed", error);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="document-panel glass-panel">
      <div className="doc-header">
        <h3>Knowledge Base</h3>
        <input 
          type="file" 
          accept="application/pdf" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileUpload}
        />
        <button 
          className="btn" 
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
        >
          <FileUp size={16} />
          {isUploading ? 'Uploading...' : 'Upload PDF'}
        </button>
      </div>

      <div className="doc-list">
        {documents.length === 0 ? (
          <p className="no-docs">No documents uploaded yet.</p>
        ) : (
          documents.map(doc => (
            <div key={doc.id} className="doc-item">
              <FileText size={18} />
              <span>{doc.filename}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
