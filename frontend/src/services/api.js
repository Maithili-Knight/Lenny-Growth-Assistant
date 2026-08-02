const API_BASE_URL = "http://localhost:8000";

/**
 * Sends a chat request to the non-streaming /chat/ endpoint.
 * 
 * @param {object} payload - { message, session_id, system_prompt }
 * @returns {Promise<object>} - Resolves to the chat response payload containing response and artifact_id
 */
export async function sendChatRequest({ message, session_id, system_prompt, llm_provider }) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "accept": "application/json",
      },
      body: JSON.stringify({
        message,
        session_id: session_id ? parseInt(session_id) : null,
        system_prompt,
        llm_provider,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "AI service temporarily unavailable");
    }

    return await response.json();
  } catch (error) {
    if (error.message && error.name === "TypeError" && error.message.includes("Failed to fetch")) {
      throw new Error("Server is not reachable");
    }
    throw error;
  }
}

/**
 * Sends a chat request to the streaming /chat/stream endpoint.
 * 
 * @param {object} payload - { message, session_id, system_prompt, llm_provider }
 * @param {function} onChunk - Callback for each incoming string chunk
 * @param {function} onDone - Callback when streaming is completed
 * @param {function} onError - Callback for errors
 */
export async function streamChatRequest({ message, session_id, system_prompt, llm_provider }, onChunk, onDone, onError) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        session_id: session_id ? parseInt(session_id) : null,
        system_prompt,
        llm_provider,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "AI service temporarily unavailable");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }
      const chunkText = decoder.decode(value, { stream: true });
      onChunk(chunkText);
    }
    onDone();
  } catch (error) {
    if (error.message && error.message.includes("Failed to fetch")) {
      onError(new Error("Server is not reachable"));
    } else {
      onError(error);
    }
  }
}

/**
 * Fetches all chat sessions from the backend database.
 * 
 * @returns {Promise<Array>} - List of session objects
 */
export async function fetchSessions() {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/`);
    if (!response.ok) {
      throw new Error("Failed to retrieve sessions list");
    }
    return await response.json();
  } catch (error) {
    throw new Error("Server is not reachable");
  }
}

/**
 * Creates a brand new chat session in the database.
 * 
 * @returns {Promise<object>} - Newly created session object
 */
export async function createSession() {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/`, {
      method: "POST",
    });
    if (!response.ok) {
      throw new Error("Failed to create new session");
    }
    return await response.json();
  } catch (error) {
    throw new Error("Server is not reachable");
  }
}

/**
 * Fetches the message history for a specific chat session.
 * 
 * @param {string|number} session_id - The session ID
 * @returns {Promise<Array>} - Chronological list of message history
 */
export async function fetchSessionMessages(session_id) {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/${session_id}/messages`);
    if (!response.ok) {
      throw new Error("Failed to load message history");
    }
    return await response.json();
  } catch (error) {
    throw new Error("Server is not reachable");
  }
}

/**
 * Fetches detail metrics for a specific artifact from the database.
 * 
 * @param {string|number} artifact_id - The artifact ID
 * @returns {Promise<object>} - The artifact details (title, content, type)
 */
export async function fetchArtifact(artifact_id) {
  try {
    const response = await fetch(`${API_BASE_URL}/artifacts/${artifact_id}`);
    if (!response.ok) {
      throw new Error("Failed to load artifact viewer content");
    }
    return await response.json();
  } catch (error) {
    throw new Error("Server is not reachable");
  }
}

/**
 * Renames a chat session title.
 * 
 * @param {string|number} session_id - The session ID
 * @param {string} title - The new title
 * @returns {Promise<object>} - Updated session object
 */
export async function renameSession(session_id, title) {
  try {
    const response = await fetch(`${API_BASE_URL}/sessions/${session_id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    if (!response.ok) {
      throw new Error("Failed to rename session");
    }
    return await response.json();
  } catch (error) {
    throw new Error("Server is not reachable");
  }
}
