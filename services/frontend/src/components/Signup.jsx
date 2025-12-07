import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient'; // Adjust path as needed
import styles from './LoginSignup.module.css'; // Shared styles

const Signup = () => {
  const [formData, setFormData] = useState({
    programming_skill_level: 'beginner',
    robotics_experience: 'none',
    hardware_access: '', // Comma-separated
    preferred_language: 'en',
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    // Check if user is already logged in and needs to complete profile
    const fetchUser = async () => {
      try {
        const user = await apiClient.getMe();
        if (user) {
          setCurrentUser(user);
          // Pre-fill form if profile data exists
          if (user.profile) {
            setFormData({
              programming_skill_level: user.profile.programming_skill_level || 'beginner',
              robotics_experience: user.profile.robotics_experience || 'none',
              hardware_access: user.profile.hardware_access || '',
              preferred_language: user.profile.preferred_language || 'en',
            });
          }
        } else {
          // If not logged in, user needs to go through Better-Auth first
          setError("Please log in first to complete your profile.");
        }
      } catch (err) {
        setError("Failed to fetch user data. Please try logging in again.");
        console.error("Error fetching user data:", err);
      }
    };
    fetchUser();
  }, []);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!currentUser) {
        setError("You must be logged in to complete your profile.");
        return;
    }

    try {
      const response = await apiClient.updateUserProfile(formData);
      setSuccess("Profile updated successfully!");
      console.log("Profile updated:", response);
      // Optionally redirect user after successful signup/profile completion
      window.location.href = '/'; // Redirect to home or docs
    } catch (err) {
      setError("Failed to update profile. Please check your inputs.");
      console.error("Profile update error:", err);
    }
  };

  if (!currentUser) {
    return (
        <div className={styles.authContainer}>
            <h2>Complete Your Profile</h2>
            <p className={styles.error}>{error || "Loading user data..."}</p>
            <p>You need to log in first using Google before completing your profile.</p>
            <button className={styles.authButton} onClick={apiClient.login}>Login with Google</button>
        </div>
    );
  }

  return (
    <div className={styles.authContainer}>
      <h2>Complete Your Profile</h2>
      {error && <p className={styles.error}>{error}</p>}
      {success && <p className={styles.success}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className={styles.authInputGroup}>
          <label htmlFor="programming_skill_level">Programming Skill Level:</label>
          <select
            id="programming_skill_level"
            name="programming_skill_level"
            value={formData.programming_skill_level}
            onChange={handleChange}
            required
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className={styles.authInputGroup}>
          <label htmlFor="robotics_experience">Robotics Experience:</label>
          <select
            id="robotics_experience"
            name="robotics_experience"
            value={formData.robotics_experience}
            onChange={handleChange}
            required
          >
            <option value="none">None</option>
            <option value="basic">Basic</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className={styles.authInputGroup}>
          <label htmlFor="hardware_access">Hardware Access (comma-separated, e.g., Arduino,GPU):</label>
          <input
            type="text"
            id="hardware_access"
            name="hardware_access"
            value={formData.hardware_access}
            onChange={handleChange}
            placeholder="Arduino, Raspberry Pi, GPU"
          />
        </div>

        <div className={styles.authInputGroup}>
          <label htmlFor="preferred_language">Preferred Language:</label>
          <select
            id="preferred_language"
            name="preferred_language"
            value={formData.preferred_language}
            onChange={handleChange}
            required
          >
            <option value="en">English</option>
            <option value="ur">Urdu</option>
          </select>
        </div>

        <button type="submit" className={styles.authButton}>Save Profile</button>
      </form>
    </div>
  );
};

export default Signup;
