import React, { useState, useEffect } from "react";
import { useChat } from "./hooks/useChat";
import { ChatWindow } from "./components/ChatWindow";
import { InputBox } from "./components/InputBox";
import { ArtifactViewer } from "./components/ArtifactViewer";

function App() {
  const { 
    messages, 
    sessionsList, 
    loading, 
    error, 
    sessionId, 
    llmProvider,
    setLlmProvider,
    sendMessage, 
    loadSession, 
    startNewSession,
    renameSession, 
  } = useChat();

  const [systemPrompt, setSystemPrompt] = useState("");
  const [useStreaming, setUseStreaming] = useState(false);
  const [showErrorBanner, setShowErrorBanner] = useState(true);
  const [activeArtifactId, setActiveArtifactId] = useState(null);

  // Inline rename state
  const [editingSessionId, setEditingSessionId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

  // Auto-open newly generated artifacts
  useEffect(() => {
    if (messages.length > 0) {
      const lastMsg = messages[messages.length - 1];
      if (lastMsg.role === "assistant" && lastMsg.artifact_id) {
        setActiveArtifactId(lastMsg.artifact_id);
      }
    }
  }, [messages]);

  useEffect(() => {
    if (error) setShowErrorBanner(true);
  }, [error]);

  const handleSend = (text) => {
    sendMessage(text, systemPrompt, useStreaming);
  };

  // --- Inline rename handlers ---
  const handleDoubleClick = (session) => {
    setEditingSessionId(session.id);
    setEditingTitle(session.title);
  };

  const handleRenameSubmit = (e) => {
    e.preventDefault();
    if (editingTitle.trim() && editingSessionId) {
      renameSession(editingSessionId, editingTitle.trim());
    }
    setEditingSessionId(null);
    setEditingTitle("");
  };

  const handleRenameBlur = () => {
    if (editingTitle.trim() && editingSessionId) {
      renameSession(editingSessionId, editingTitle.trim());
    }
    setEditingSessionId(null);
    setEditingTitle("");
  };

  const isWelcomeScreen = messages.length === 0;

  return (
    <div className="main-layout">
      {/* ─── Left Sidebar ─── */}
      <aside className="sidebar">
        <button className="btn-new-chat" onClick={startNewSession} disabled={loading}>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" style={{ marginRight: "8px" }}>
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
          New chat
        </button>

        <div className="sessions-list">
          <div className="sessions-header">Chats</div>
          {sessionsList.map((session) => {
            const isActive = String(session.id) === String(sessionId);
            const isEditing = editingSessionId === session.id;

            return (
              <div
                key={session.id}
                className={`session-item ${isActive ? "active" : ""}`}
              >
                {isEditing ? (
                  <form onSubmit={handleRenameSubmit} className="rename-form">
                    <input
                      className="rename-input"
                      value={editingTitle}
                      onChange={(e) => setEditingTitle(e.target.value)}
                      onBlur={handleRenameBlur}
                      autoFocus
                    />
                  </form>
                ) : (
                  <button
                    className="session-item-btn"
                    onClick={() => !loading && loadSession(session.id)}
                    onDoubleClick={() => handleDoubleClick(session)}
                    disabled={loading}
                    title="Double-click to rename"
                  >
                    <span className="session-title">{session.title}</span>
                  </button>
                )}
              </div>
            );
          })}
        </div>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          <div className="toggle-container">
            <span>Stream</span>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={useStreaming}
                onChange={(e) => setUseStreaming(e.target.checked)}
              />
              <span className="slider" />
            </label>
          </div>
        </div>
      </aside>

      {/* ─── Main Content Pane ─── */}
      <main className="content-pane">
        <div className={`chat-pane ${activeArtifactId ? "split" : "full"}`}>

          {/* Top bar with Model Selector */}
          <header className="app-header">
            <div className="header-title-section">
              <h1>Lenny Growth Assistant</h1>
              <div className="model-selector-wrapper">
                <select 
                  className="model-select-dropdown" 
                  value={llmProvider}
                  onChange={(e) => setLlmProvider(e.target.value)}
                  disabled={loading}
                >
                  <option value="ollama">⚡ Local (Ollama)</option>
                  <option value="claude">☁️ Cloud (Claude 3.5)</option>
                </select>
              </div>
            </div>
          </header>

          {isWelcomeScreen ? (
            /* ─── Welcome Screen (ChatGPT style) ─── */
            <div className="welcome-screen">
              <div className="welcome-content">
                <h2 className="welcome-heading">Where should we begin?</h2>
              </div>
              <div className="welcome-input-area">
                {error && showErrorBanner && (
                  <div className="error-banner">
                    <span>{error}</span>
                    <button className="btn-close-error" onClick={() => setShowErrorBanner(false)}>
                      &times;
                    </button>
                  </div>
                )}
                <InputBox onSend={handleSend} loading={loading} />
              </div>
            </div>
          ) : (
            /* ─── Active Chat View ─── */
            <>
              {/* System Prompt Bar */}
              <div className="system-prompt-bar">
                <label htmlFor="system-prompt">System Prompt:</label>
                <input
                  id="system-prompt"
                  type="text"
                  className="system-prompt-input"
                  placeholder="You are a helpful AI assistant."
                  value={systemPrompt}
                  onChange={(e) => setSystemPrompt(e.target.value)}
                />
              </div>

              <ChatWindow 
                messages={messages} 
                loading={loading} 
                onSelectArtifact={setActiveArtifactId} 
              />

              <div className="input-area">
                {error && showErrorBanner && (
                  <div className="error-banner">
                    <span>{error}</span>
                    <button className="btn-close-error" onClick={() => setShowErrorBanner(false)}>
                      &times;
                    </button>
                  </div>
                )}
                <InputBox onSend={handleSend} loading={loading} />
              </div>
            </>
          )}
        </div>

        {/* ─── Artifact Viewer Splitscreen ─── */}
        {activeArtifactId && (
          <div className="artifact-pane-wrapper">
            <ArtifactViewer 
              artifactId={activeArtifactId} 
              onClose={() => setActiveArtifactId(null)} 
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
