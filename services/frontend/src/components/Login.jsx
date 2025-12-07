import React, { useState } from 'react';
import apiClient from '../apiClient'; // Adjust path as needed
import styles from './LoginSignup.module.css'; // Shared styles

const Login = () => {
  const [error, setError] = useState(null);

  const handleLogin = () => {
    try {
      apiClient.login(); // Redirects to Better-Auth login
    } catch (err) {
      setError("Failed to initiate login. Please try again.");
      console.error("Login initiation error:", err);
    }
  };

  return (
    <div className={styles.authContainer}>
      <h2>Login</h2>
      {error && <p className={styles.error}>{error}</p>}
      <button className={styles.authButton} onClick={handleLogin}>
        Login with Better-Auth
      </button>
      <p>Don't have an account? <a href="/signup">Sign up</a></p>
    </div>
  );
};

export default Login;
