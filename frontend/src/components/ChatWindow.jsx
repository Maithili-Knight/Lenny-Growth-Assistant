import React, { useEffect, useRef } from "react";
import { Message } from "./Message";

export function ChatWindow({ messages, loading, onSelectArtifact }) {
  const windowRef = useRef(null);

  // Auto scroll to the bottom on new messages or loading transitions
  useEffect(() => {
    if (windowRef.current) {
      windowRef.current.scrollTop = windowRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const showLoadingIndicator = loading && !messages.some((msg) => msg.isStreaming);

  return (
    <div className="chat-window" ref={windowRef}>
      <div className="chat-container-inner">
        {messages.length === 0 ? (
          <div style={{ textAlign: "center", color: "#64748b", marginTop: "40px", fontSize: "0.9rem" }}>
            No messages yet. Start a conversation below!
          </div>
        ) : (
          messages.map((msg) => (
            <Message 
              key={msg.id} 
              message={msg} 
              onSelectArtifact={onSelectArtifact} 
            />
          ))
        )}

        {showLoadingIndicator && (
          <div className="loading-indicator">
            <span className="pulse-dot" />
            <span className="pulse-dot" />
            <span className="pulse-dot" />
          </div>
        )}
      </div>
    </div>
  );
}
