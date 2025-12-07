import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

type Message = {
  text: string;
  sender: 'user' | 'bot' | 'context';
};

// Custom event type
interface AskAiSelectionEvent extends CustomEvent {
  detail: {
    text: string;
  };
}

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectionContext, setSelectionContext] = useState<string | null>(null);
  const messageListRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to the bottom of the message list when new messages are added
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    const handleAskSelection = (event: AskAiSelectionEvent) => {
      setSelectionContext(event.detail.text);
      setMessages([{ text: `Context:\n"${event.detail.text}"`, sender: 'context' }]);
      setIsOpen(true);
    };

    document.addEventListener('ask-ai-selection', handleAskSelection as EventListener);
    return () => {
      document.removeEventListener('ask-ai-selection', handleAskSelection as EventListener);
    };
  }, []);
  
  const toggleChat = () => setIsOpen(!isOpen);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage: Message = { text: inputValue, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: inputValue, 
          session_id: sessionId,
          selected_text: selectionContext,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      const botMessage: Message = { text: data.answer, sender: 'bot' };
      setMessages((prev) => [...prev, botMessage]);
      setSessionId(data.session_id);

    } catch (error) {
      console.error('Error fetching chat response:', error);
      const errorMessage: Message = { text: 'Sorry, I am having trouble connecting. Please try again later.', sender: 'bot' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      // Clear context after the first question about it
      setSelectionContext(null);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>AI Course Assistant</h3>
          </div>
          <div className={styles.messageList} ref={messageListRef}>
            {messages.map((msg, index) => (
              <div key={index} className={styles[`${msg.sender}Message`]}>
                <div className={styles.messageContent}>{msg.text.split('\n').map((line, i) => <p key={i}>{line}</p>)}</div>
              </div>
            ))}
          </div>
          <form className={styles.inputForm} onSubmit={handleSendMessage}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={selectionContext ? "Ask a question about the text..." : "Ask a question..."}
              autoFocus
            />
            <button type="submit" className="button button--primary">Send</button>
          </form>
        </div>
      )}
      <button className={styles.toggleButton} onClick={toggleChat}>
        {isOpen ? 'X' : '🤖'}
      </button>
    </div>
  );
};

export default Chatbot;
