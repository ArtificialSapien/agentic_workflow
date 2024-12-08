import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, X } from 'lucide-react';
import { Link } from 'react-router-dom';

interface ChatSectionProps {
  odd: boolean;
}

const ChatWindow: React.FC<ChatSectionProps> = ({ odd }) => {
  const [messages, setMessages] = useState<Array<{ sender: string; text: string }>>([
    { sender: 'bot', text: 'Hello! How can I assist you today?' },
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Automatically scrolls to the latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (input.trim() === '') return;

    // Add the user's message
    setMessages([...messages, { sender: 'user', text: input }]);

    // Simulate a bot response after a short delay
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Thank you for your message! How else can I assist you?' },
      ]);
    }, 1000);

    setInput('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <section className={`bg-gradient-to-b ${odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'} text-center py-20`}>
      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-primary-600">Chatbot</h1>
          <Link to="/" className="text-accent-500 hover:text-accent-600 flex items-center">
            <X className="w-6 h-6 mr-1" />
            Close
          </Link>
        </div>

        {/* Chat Interface */}
        <div className="flex flex-col h-[60vh] bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Messages Area */}
          <div className="flex-1 p-6 overflow-y-auto">
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                className={`mb-4 flex ${
                  msg.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <div
                  className={`max-w-xs p-4 rounded-lg ${
                    msg.sender === 'user'
                      ? 'bg-accent-500 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {msg.text}
                </div>
              </motion.div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Your message..."
              className="flex-1 px-4 py-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-accent-400"
              aria-label="Enter chat message"
            />
            <button
              onClick={handleSend}
              className="bg-accent-500 text-white p-3 rounded-r-md hover:bg-accent-600 focus:outline-none focus:ring-2 focus:ring-accent-400 transition"
              aria-label="Send message"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChatWindow;
