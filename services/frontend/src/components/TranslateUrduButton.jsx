import React, { useState } from 'react';
import apiClient from '../apiClient'; // Adjust path as needed
import styles from './ChapterButtons.module.css'; // Shared styles for chapter actions

const TranslateUrduButton = ({ chapterPath, originalMarkdown, onTranslate, onToggleOriginal }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isUrdu, setIsUrdu] = useState(false);

  const handleTranslate = async () => {
    if (isUrdu) {
      // If currently Urdu, toggle back to English (original)
      onToggleOriginal();
      setIsUrdu(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.translateChapter(originalMarkdown, chapterPath, 'ur');
      if (response && response.translated_markdown) {
        onTranslate(response.translated_markdown);
        setIsUrdu(true);
      } else {
        setError("Failed to get Urdu translation.");
      }
    } catch (err) {
      setError("Error translating chapter. Please try again.");
      console.error("Translation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleTranslate} disabled={loading} className={styles.chapterButton}>
      {loading ? 'ترجمہ ہو رہا ہے...' : (isUrdu ? 'Show English' : 'اردو میں ترجمہ کریں')}
      {error && <span className={styles.buttonError} title={error}>⚠️</span>}
    </button>
  );
};

export default TranslateUrduButton;
