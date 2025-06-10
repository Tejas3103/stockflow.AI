import { useState, useEffect } from 'react'
import './App.css' // Keep or modify this CSS file later for styling

// Define a type for messages to clarify their structure
interface ChatMessage {
  sender: 'user' | 'agent'; // 'user' or 'agent'
  text: string;
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]); // State to hold chat messages as objects
  const [inputMessage, setInputMessage] = useState(''); // State to hold current input
  const [isLoading, setIsLoading] = useState(false); // State to indicate if waiting for agent response

  // Add an initial greeting message here later
  useEffect(() => {
    const greetingMessage: ChatMessage = { sender: 'agent', text: 'Hey, I am Stock Agent that will help you recommend Stock:\nHow can I help you?' };
    setMessages([greetingMessage]);
  }, []); // Empty dependency array ensures this runs only once on mount

  const handleSendMessage = async () => { // Make the function async
    const messageContent = inputMessage.trim();
    if (messageContent === '') {
      return; // Don't send empty messages
    }

    // Add user's message to state immediately
    const newUserMessage: ChatMessage = { sender: 'user', text: messageContent };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setInputMessage(''); // Clear the input field
    setIsLoading(true); // Indicate loading

    try {
      // Send the message to the backend
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: messageContent }),
      });

      if (!response.ok) {
        // Attempt to parse error response if available
        const errorData = await response.json().catch(() => null);
        const errorMessageText = errorData?.detail?.[0]?.msg || errorData?.response || `HTTP error! status: ${response.status}`;
         throw new Error(`Backend Error: ${errorMessageText}`);
      }

      const data = await response.json();
      console.log('Response from backend:', data);

      // Add agent's response to state
      // Assuming the backend response has a 'response' field
      if (data && data.response) {
         const newAgentMessage: ChatMessage = { sender: 'agent', text: data.response };
         setMessages((prevMessages) => [...prevMessages, newAgentMessage]);
      } else {
         console.error('Backend response did not contain a "response" field:', data);
         const errorMessage: ChatMessage = { sender: 'agent', text: 'Error: Could not get a valid response from the agent (unexpected format).' };
         setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }

    } catch (error) {
      console.error('Error sending message or receiving response:', error);
      const errorMessage: ChatMessage = { sender: 'agent', text: `Error: ${(error as Error).message || 'An unknown error occurred.'}` };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false); // End loading
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputMessage(event.target.value);
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && !isLoading) {
      handleSendMessage();
    }
  };

  return (
    <div className="chat-container"> {/* Add a class for styling */}
      <div className="messages-display"> {/* Area to display messages */}
        {messages.map((message, index) => (
          // Apply conditional class based on sender
          <p key={index} className={message.sender === 'user' ? 'user-message' : 'agent-message'}>
            {/* Optionally remove the sender label here as styling will differentiate */}
            {/* <strong>{message.sender}:</strong>  */}
            {message.text}
          </p>
        ))}
         {isLoading && <p className="agent-message">Agent is thinking...</p>} {/* Loading indicator with agent styling */}
      </div>
      <div className="input-area"> {/* Area for input and button */}
        <input
          type="text"
          value={inputMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button onClick={handleSendMessage} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
}

export default App
