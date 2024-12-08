import React, { useState } from 'react';
import { Bot } from 'lucide-react';

const ChatbotButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Chatbot Button */}
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 bg-accent-500 text-white p-4 rounded-full shadow-lg hover:bg-accent-600 focus:outline-none focus:ring-2 focus:ring-accent-400 transition"
        aria-label="Open Chatbot"
      >
        <Bot className="w-6 h-6" />
      </button>

      {/* Chatbot Window */}
      {isOpen && (
        <div className="fixed bottom-20 right-6 bg-white w-80 h-96 rounded-lg shadow-lg flex flex-col">
          <div className="flex justify-between items-center bg-accent-500 text-white p-4 rounded-t-lg">
            <span>Help</span>
            <button onClick={toggleChat} aria-label="Close Chatbot">
              ✕
            </button>
          </div>
          <div className="flex-grow p-4 overflow-y-auto">
            {/* Embed your chatbot client here */}
            <p>Welcome! How can I help you?</p>
            {/* Example chat messages */}
          </div>
          <div className="p-4 border-t">
            <input
              type="text"
              placeholder="Your message..."
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-accent-400"
              aria-label="Enter chat message"
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotButton;
