import { useState, useEffect } from "react";
import { 
  sendChatRequest, 
  streamChatRequest, 
  fetchSessions, 
  createSession, 
  fetchSessionMessages,
  renameSession as renameSessionAPI,
} from "../services/api";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [sessionsList, setSessionsList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [llmProvider, setLlmProvider] = useState("ollama"); // "ollama" or "claude"

  // 1. Initial load: fetch all sessions, set the active one
  useEffect(() => {
    async function initSessions() {
      try {
        const list = await fetchSessions();
        setSessionsList(list);

        let activeId = localStorage.getItem("chat_session_id");
        
        if (activeId && list.some(s => String(s.id) === String(activeId))) {
          setSessionId(activeId);
          loadSession(activeId);
        } else if (list.length > 0) {
          const mostRecentId = String(list[0].id);
          setSessionId(mostRecentId);
          localStorage.setItem("chat_session_id", mostRecentId);
          loadSession(mostRecentId);
        } else {
          await startNewSession();
        }
      } catch (err) {
        setError(err.message || "Failed to connect to backend server");
      }
    }
    initSessions();
  }, []);

  // 2. Fetch and render messages for a specific session ID
  const loadSession = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const history = await fetchSessionMessages(id);
      const formattedHistory = history.map((msg) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        artifact_id: msg.artifact_id || null,
        timestamp: new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }));
      setMessages(formattedHistory);
      setSessionId(String(id));
      localStorage.setItem("chat_session_id", String(id));
    } catch (err) {
      setError(err.message || "Failed to load session message history");
    } finally {
      setLoading(false);
    }
  };

  // 3. Create a new chat session in the database
  const startNewSession = async () => {
    setLoading(true);
    setError(null);
    try {
      const newSession = await createSession();
      setSessionsList((prev) => [newSession, ...prev]);
      setSessionId(String(newSession.id));
      localStorage.setItem("chat_session_id", String(newSession.id));
      setMessages([]);
    } catch (err) {
      setError(err.message || "Failed to create new session");
    } finally {
      setLoading(false);
    }
  };

  // 4. Rename a session title (manual user rename)
  const renameSession = async (id, newTitle) => {
    try {
      await renameSessionAPI(id, newTitle);
      setSessionsList((prev) =>
        prev.map((s) =>
          String(s.id) === String(id) ? { ...s, title: newTitle } : s
        )
      );
    } catch (err) {
      setError(err.message || "Failed to rename session");
    }
  };

  // Helper: update a session title in the local sessions list (used by auto-title)
  const updateSessionTitleLocally = (id, newTitle) => {
    setSessionsList((prev) =>
      prev.map((s) =>
        String(s.id) === String(id) ? { ...s, title: newTitle } : s
      )
    );
  };

  const resetChat = () => {
    startNewSession();
  };

  const sendMessage = async (messageText, systemPrompt = "", useStreaming = false) => {
    if (!messageText || !messageText.trim()) {
      setError("Please enter a message");
      return;
    }

    if (!sessionId) {
      setError("No active session found. Please create a new chat.");
      return;
    }

    setError(null);

    const userMessage = {
      id: "u-" + Date.now() + "-" + Math.random().toString(36).substr(2, 5),
      role: "user",
      content: messageText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    const payload = {
      message: messageText,
      session_id: sessionId,
      system_prompt: systemPrompt || undefined,
      llm_provider: llmProvider,
    };

    if (useStreaming) {
      const assistantMessageId = "a-" + Date.now() + "-" + Math.random().toString(36).substr(2, 5);
      
      setMessages((prev) => [
        ...prev,
        {
          id: assistantMessageId,
          role: "assistant",
          content: "",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          isStreaming: true,
        },
      ]);

      await streamChatRequest(
        payload,
        (chunk) => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessageId
                ? { ...msg, content: msg.content + chunk }
                : msg
            )
          );
        },
        () => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessageId ? { ...msg, isStreaming: false } : msg
            )
          );
          setLoading(false);
          loadSession(sessionId);
        },
        (err) => {
          setError(err.message || "AI service temporarily unavailable");
          setMessages((prev) => prev.filter((msg) => msg.id !== assistantMessageId));
          setLoading(false);
        }
      );
    } else {
      try {
        const data = await sendChatRequest(payload);
        const assistantMessage = {
          id: "a-" + Date.now() + "-" + Math.random().toString(36).substr(2, 5),
          role: "assistant",
          content: data.response,
          artifact_id: data.artifact_id || null,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, assistantMessage]);

        if (data.session_title) {
          updateSessionTitleLocally(sessionId, data.session_title);
        }
      } catch (err) {
        setError(err.message || "AI service temporarily unavailable");
      } finally {
        setLoading(false);
      }
    }
  };

  return {
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
    resetChat,
  };
}
