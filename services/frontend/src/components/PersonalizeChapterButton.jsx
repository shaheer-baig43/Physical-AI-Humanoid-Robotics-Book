import React, { useState } from 'react';
import apiClient from '../apiClient'; // Adjust path as needed
import styles from './ChapterButtons.module.css'; // Shared styles for chapter actions

const PersonalizeChapterButton = ({ chapterPath, originalMarkdown, onPersonalize }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePersonalize = async () => {
    setLoading(true);
    setError(null);
    try {
      // apiClient.personalizeChapter automatically fetches user_id internally via token
      const response = await apiClient.personalizeChapter(originalMarkdown, chapterPath);
      if (response && response.personalized_markdown) {
        onPersonalize(response.personalized_markdown);
      } else {
        setError("Failed to get personalized content.");
      }
    } catch (err) {
      setError("Error personalizing chapter. Please ensure you are logged in and your profile is complete.");
      console.error("Personalization error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handlePersonalize} disabled={loading} className={styles.chapterButton}>
      {loading ? 'Personalizing...' : 'Personalize This Chapter'}
      {error && <span className={styles.buttonError} title={error}>⚠️</span>}
    </button>
  );
};

export default PersonalizeChapterButton;
