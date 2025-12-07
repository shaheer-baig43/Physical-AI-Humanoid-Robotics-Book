// services/frontend/src/apiClient.js
// A simple API client for interacting with the backend FastAPI service

const API_BASE_URL = "http://localhost:8000/api"; // Adjust if your backend URL changes

const getAuthHeaders = () => {
    // Retrieve token from localStorage, sessionStorage, or a cookie
    const token = localStorage.getItem('access_token'); // Example: stored after login
    if (token) {
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        };
    }
    return {
        'Content-Type': 'application/json',
    };
};

const apiClient = {
    // --- Auth Endpoints ---
    login: () => {
        window.location.href = `${API_BASE_URL}/v1/auth/google/login`;
    },
    logout: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/v1/auth/logout`, {
                method: 'POST',
                headers: getAuthHeaders(),
            });
            if (response.ok) {
                localStorage.removeItem('access_token');
                // Optionally redirect or refresh page
                window.location.href = '/'; 
            } else {
                console.error("Logout failed:", await response.text());
            }
        } catch (error) {
            console.error("Error during logout:", error);
        }
    },
    getMe: async () => {
        const response = await fetch(`${API_BASE_URL}/v1/auth/me`, {
            method: 'GET',
            headers: getAuthHeaders(),
        });
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid, clear it
                localStorage.removeItem('access_token');
                return null;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    },

    // --- User Profile Endpoints ---
    updateUserProfile: async (profileData) => {
        const response = await fetch(`${API_BASE_URL}/v1/user/profile`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(profileData),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    },

    // --- RAG Chatbot Endpoint ---
    ragQuery: async (query, selectedText = null, userId = null) => {
        const response = await fetch(`${API_BASE_URL}/v1/rag`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ query, selected_text: selectedText, user_id: userId }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    },

    // --- Personalization Endpoint ---
    personalizeChapter: async (chapterMarkdown, chapterPath, userId) => {
        const response = await fetch(`${API_BASE_URL}/v1/personalize`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ chapter_markdown: chapterMarkdown, chapter_path: chapterPath, user_id: userId }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    },

    // --- Translation Endpoint ---
    translateChapter: async (chapterMarkdown, chapterPath, lang) => {
        const response = await fetch(`${API_BASE_URL}/v1/translate?lang=${lang}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ chapter_markdown: chapterMarkdown, chapter_path: chapterPath }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    },
};

export default apiClient;
