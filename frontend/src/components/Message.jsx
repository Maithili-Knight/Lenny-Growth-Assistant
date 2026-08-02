import React from "react";

export function Message({ message, onSelectArtifact }) {
  const { role, content, timestamp, isStreaming, artifact_id } = message;
  const isUser = role === "user";

  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      {/* Avatar circle */}
      <div className={`message-avatar ${isUser ? "user" : "assistant"}`}>
        {isUser ? "U" : "L"}
      </div>

      {/* Content bubble & metadata */}
      <div className="message-content-container">
        <div className="message-bubble">
          {content}
          {isStreaming && <span className="cursor-typing" />}
        </div>
        <div className="message-meta">
          <span>{timestamp}</span>
          {artifact_id && (
            <span 
              className="badge-artifact" 
              onClick={() => onSelectArtifact && onSelectArtifact(artifact_id)}
            >
              Artifact #{artifact_id}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
