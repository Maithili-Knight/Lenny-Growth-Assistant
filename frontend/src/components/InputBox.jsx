import React, { useState } from "react";

export function InputBox({ onSend, loading }) {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text || !text.trim() || loading) return;
    onSend(text);
    setText("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="input-area-inner">
      <form className="input-row" onSubmit={handleSubmit}>
        <textarea
          className="input-box"
          placeholder="Message Lenny Growth Assistant..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          rows="1"
        />
        <button className="btn-send" type="submit" disabled={loading || !text.trim()}>
          <svg viewBox="0 0 24 24">
            <path d="M12 2c5.52 0 10 4.48 10 10s-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2zm1 10h3l-4-4-4 4h3v4h2v-4z" />
          </svg>
        </button>
      </form>
      <div className="input-disclaimer">
        Lenny Growth Assistant can make mistakes. Verify important info.
      </div>
    </div>
  );
}
