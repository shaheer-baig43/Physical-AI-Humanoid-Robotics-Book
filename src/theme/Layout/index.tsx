import React, {type ReactNode, useState, useEffect, useRef} from 'react';
import Layout from '@theme-original/Layout';
import type LayoutType from '@theme/Layout';
import type {WrapperProps} from '@docusaurus/types';
import Chatbot from '@site/src/components/Chatbot';
import apiClient from '@site/services/frontend/src/apiClient'; // Import apiClient
import Link from '@docusaurus/Link'; // Import Link for navigation

type Props = WrapperProps<typeof LayoutType>;

const SelectionAskButton = ({ top, left, onAsk }) => {
  const style: React.CSSProperties = {
    position: 'absolute',
    top: `${top}px`,
    left: `${left}px`,
    backgroundColor: 'var(--ifm-color-primary)',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    padding: '5px 10px',
    cursor: 'pointer',
    zIndex: 1001,
    boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
    userSelect: 'none', // Prevent selecting the button's text
    transform: 'translateX(-50%)', // Center the button on the selection
  };
  return <button style={style} onClick={onAsk}>Ask AI</button>;
};

export default function LayoutWrapper(props: Props): ReactNode {
  const [selection, setSelection] = useState<{ top: number; left: number; text: string } | null>(null);
  const [currentUser, setCurrentUser] = useState<any>(null); // State to hold current user info
  const [isLoadingUser, setIsLoadingUser] = useState(true); // State for loading status

  // Fetch current user on component mount
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await apiClient.getMe();
        setCurrentUser(user);
      } catch (error) {
        console.warn("No active user session or failed to fetch user (this is normal if not logged in):", error);
        setCurrentUser(null);
      } finally {
        setIsLoadingUser(false);
      }
    };
    fetchUser();
  }, []); // Run only once on mount

  const handleMouseUp = (event: MouseEvent) => {
    const target = event.target as Element;
    // Check if selection is within the chat widget or a button, to avoid interfering
    if (target.closest(`[class*="chatbotContainer"]`) || target.closest('button')) {
      setSelection(null);
      return;
    }
    
    const selected = window.getSelection();
    const selectedText = selected.toString().trim();

    // Only show "Ask AI" button for meaningful selections (e.g., more than 5 characters)
    if (selectedText && selectedText.length > 5 && selectedText.length < 500) { 
      const range = selected.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      const scrollTop = window.scrollY || document.documentElement.scrollTop;

      setSelection({
        top: rect.bottom + scrollTop + 5, // 5px below selection
        left: rect.left + rect.width / 2, // Centered on selection
        text: selectedText,
      });
    } else {
      setSelection(null);
    }
  };

  const handleAsk = () => {
    if (selection) {
      document.dispatchEvent(new CustomEvent('ask-ai-selection', { detail: { text: selection.text } }));
      setSelection(null); // Hide button after clicking
    }
  };

  // Add event listener for text selection
  useEffect(() => {
    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);


  return (
    <>


      <Layout {...props} />
      {selection && <SelectionAskButton top={selection.top} left={selection.left} onAsk={handleAsk} />}
      <Chatbot />
    </>
  );
}
