import React, { useState, useEffect } from "react";
import { fetchArtifact } from "../services/api";

function parseMarkdown(text) {
  if (!text) return "";
  
  // Escape HTML characters first
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Code blocks (fenced ```...```)
  html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
    return `<pre class="artifact-code-block"><code>${code.trim()}</code></pre>`;
  });

  // Headings
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Bold & Italics & Inline Code
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

  // List bullets & Numbered lists
  html = html.replace(/^\s*[-*+]\s+(.*$)/gim, '<li>$1</li>');
  html = html.replace(/^\s*\d+\.\s+(.*$)/gim, '<li>$1</li>');

  // Wrap lines in paragraphs if they are not headers, code blocks, or lists
  html = html.split('\n').map(line => {
    const trimmed = line.trim();
    if (!trimmed) return '';
    if (trimmed.startsWith('<li>') || trimmed.startsWith('<h') || trimmed.startsWith('<pre') || trimmed.startsWith('</pre>') || trimmed.startsWith('<code>')) return line;
    return `<p>${line}</p>`;
  }).join('\n');

  return html;
}

export function ArtifactViewer({ artifactId, onClose }) {
  const [artifact, setArtifact] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tab, setTab] = useState("preview"); // "preview" or "code"

  useEffect(() => {
    if (!artifactId) return;

    async function loadArtifact() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchArtifact(artifactId);
        setArtifact(data);
      } catch (err) {
        setError(err.message || "Failed to load artifact");
      } finally {
        setLoading(false);
      }
    }

    loadArtifact();
  }, [artifactId]);

  if (!artifactId) return null;

  return (
    <div className="artifact-viewer-panel">
      {/* Panel Header */}
      <div className="artifact-viewer-header">
        <div className="artifact-title-section">
          <h3>{loading ? "Loading..." : artifact?.title || "Artifact Viewer"}</h3>
          <span className="artifact-type-badge">{artifact?.type || "Document"}</span>
        </div>
        <div className="artifact-header-actions">
          {/* Tabs */}
          {!loading && artifact && (
            <div className="artifact-tabs">
              <button
                className={`tab-btn ${tab === "preview" ? "active" : ""}`}
                onClick={() => setTab("preview")}
              >
                Preview
              </button>
              <button
                className={`tab-btn ${tab === "code" ? "active" : ""}`}
                onClick={() => setTab("code")}
              >
                Code
              </button>
            </div>
          )}
          <button className="btn-close-panel" onClick={onClose}>
            &times;
          </button>
        </div>
      </div>

      {/* Panel Content */}
      <div className="artifact-viewer-content">
        {loading && (
          <div className="artifact-state-message">
            <span className="pulse-dot" />
            <span className="pulse-dot" />
            <span className="pulse-dot" />
          </div>
        )}

        {error && (
          <div className="artifact-state-message error">
            {error}
          </div>
        )}

        {!loading && !error && artifact && (
          <div className="artifact-display-area">
            {tab === "preview" ? (
              artifact.type === "html" ? (
                <iframe
                  title={artifact.title}
                  srcDoc={artifact.content}
                  className="artifact-html-preview"
                  sandbox="allow-scripts"
                />
              ) : (
                <div 
                  className="artifact-markdown-preview"
                  dangerouslySetInnerHTML={{ __html: parseMarkdown(artifact.content) }}
                />
              )
            ) : (
              <pre className="artifact-code-raw">
                <code>{artifact.content}</code>
              </pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
