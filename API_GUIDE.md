I have updated the project to use Google's Gemini models instead of OpenAI. Here is the revised guide on how to obtain the necessary API keys.

First, create a new file named `.env` inside the `chatbot` directory. You will fill this file with the secrets you generate below.

**Important:** Never share these keys or commit your `.env` file to version control.

---

### 1. Google Gemini API Key (`GEMINI_API_KEY`)

The chatbot will use the Gemini API for understanding and generating responses.

1.  **Navigate to Google AI Studio:** Go to [https://aistudio.google.com/](https://aistudio.google.com/).
2.  **Log In:** Sign in with your Google account.
3.  **Get API Key:** In the top left corner, click on the "**Get API key**" button.
4.  **Create API Key:** Click "**Create API key in new project**". This will generate a new key for you.
5.  **Copy and Save:** A window will pop up with your new API key. **Copy this key immediately** and paste it into your `.env` file for the `GEMINI_API_KEY` variable.

---

### 2. Qdrant Cloud URL & API Key (`QDRANT_CLOUD_URL`, `QDRANT_API_KEY`)

Qdrant will store the vector representations of your book's content.

1.  **Navigate to Qdrant Cloud:** Go to [https://cloud.qdrant.io/](https://cloud.qdrant.io/).
2.  **Log In or Sign Up:** Create a free account or log in.
3.  **Create a Cluster:** Create a new cluster. The **Free Tier** is sufficient for this project.
4.  **Get Credentials:** Once the cluster's status is "Ready", click on it to open its overview page.
    *   Copy the **Cluster URL** and paste it into your `.env` file for the `QDRANT_CLOUD_URL` variable.
    *   Find the **API Key** in the "Authentication" section. Click the copy icon and paste the key into your `.env` file for the `QDRANT_API_KEY` variable.

---

### 3. Neon Serverless Postgres URL (`NEON_DATABASE_URL`)

Neon provides the database for storing chat history.

1.  **Navigate to Neon:** Go to [https://neon.tech/](https://neon.tech/).
2.  **Log In or Sign Up:** Create a free account or log in.
3.  **Create a Project:** Create a new project on the free tier.
4.  **Get Connection String:** On the project dashboard, find the "**Connection Details**" widget. Copy the connection URL (it starts with `postgres://`) and paste it into your `.env` file for the `NEON_DATABASE_URL` variable.

---

After you have filled in your `.env` file, the backend will be ready for the next steps. I will now proceed with updating the code to use this new tech stack.