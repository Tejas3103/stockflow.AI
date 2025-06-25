import { useState, useEffect } from 'react'
import ChatContainer from './components/Chat/ChatContainer'
import MessageList from './components/Chat/MessageList'
import ChatInput from './components/Chat/ChatInput'
import Header from './components/Layout/Header'
import Sidebar from './components/Layout/Sidebar'
import styled from 'styled-components'
import './App.css' // Keep or modify this CSS file later for styling

// Define a type for messages to clarify their structure
interface ChatMessage {
  sender: 'user' | 'agent'; // 'user' or 'agent'
  text: string;
}

const AppBackground = styled.div`
  min-height: 100vh;
  width: 100vw;
  max-width: 100vw;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  background: linear-gradient(120deg, #1a1a1a 60%, #232d2e 100%);
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 32px 0 32px;
  box-sizing: border-box;
  overflow-x: hidden;
`;

const Divider = styled.div`
  width: 1px;
  background: rgba(255,255,255,0.08);
  box-shadow: 0 0 8px 0 rgba(0,0,0,0.10);
  margin: 32px 0;
  border-radius: 2px;
`;

const SidebarGap = styled.div`
  margin-left: 24px;
`;

const SidebarContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-right: 32px;
`;

const ChatColumn = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 112px);
  overflow-y: auto;
  align-items: center;
`;

const ChatContainerGap = styled.div`
  width: 100%;
  max-width: 600px;
`;

const RightPanel = styled.aside`
  width: 300px;
  min-width: 220px;
  max-width: 340px;
  height: auto;
  max-height: calc(100vh - 112px);
  display: flex;
  flex-direction: column;
  align-items: center;
  background: ${({ theme }) => theme.colors.overlay.glass};
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 24px;
  box-shadow: 0 8px 40px 0 rgba(0,0,0,0.18);
  border: 1px solid rgba(255,255,255,0.10);
  padding: 32px 0;
  z-index: 5;
  overflow-y: auto;
  margin-left: 32px;
  margin-right: 24px;
  @media (max-width: 1200px) {
    display: none;
  }
`;

const NewsTitle = styled.div`
  font-size: 1.2rem;
  font-weight: 700;
  color: ${({ theme }) => theme.colors.accent.teal};
  margin-bottom: 18px;
`;

const NewsItem = styled.div`
  color: ${({ theme }) => theme.colors.text.primary};
  background: ${({ theme }) => theme.colors.surface};
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 1rem;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.10);
`;

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
    setIsLoading(true);

    try {
      // Send the message to the backend
      const response = await fetch('http://localhost:8000/tavily_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: messageContent }),
      });

      if (!response.ok) {
        // Attempt to parse error response if available
        const errorData = await response.json().catch(() => null);
        const errorMessageText = errorData?.detail?.[0]?.msg || errorData?.response || `HTTP error! status: ${response.status}`;
         throw new Error(`Backend Error: ${errorMessageText}`);
      }

      const data = await response.json();
      console.log('Response from backend:', data);

      // Add Tavily answer and sources to state
      if (data && data.answer) {
        let answerText = data.answer;
        if (data.sources && Array.isArray(data.sources) && data.sources.length > 0) {
          answerText += '\n\nSources:';
          data.sources.forEach((src: any, idx: number) => {
            if (src.url) {
              answerText += `\n${idx + 1}. ${src.url}`;
            }
          });
        }
        const newAgentMessage: ChatMessage = { sender: 'agent', text: answerText };
        setMessages((prevMessages) => [...prevMessages, newAgentMessage]);
      } else {
        console.error('Backend response did not contain an "answer" field:', data);
        const errorMessage: ChatMessage = { sender: 'agent', text: 'Error: Could not get a valid response from Tavily (unexpected format).' };
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

  return (
    <AppBackground>
      <Header />
      <MainContent>
        <SidebarGap />
        <SidebarContainer>
          <Sidebar />
        </SidebarContainer>
        <Divider />
        <ChatColumn>
          <ChatContainerGap>
            <ChatContainer>
              <MessageList messages={messages} />
              <ChatInput
                value={inputMessage}
                onChange={handleInputChange}
                onSend={handleSendMessage}
                loading={isLoading}
              />
            </ChatContainer>
          </ChatContainerGap>
        </ChatColumn>
        <RightPanel>
          <NewsTitle>Market News</NewsTitle>
          <NewsItem>Fed signals no rate hike this quarter. Markets rally.</NewsItem>
          <NewsItem>Apple unveils new AI chip, stock surges.</NewsItem>
          <NewsItem>Tesla reports record deliveries, shares up 2%.</NewsItem>
          <NewsItem>Microsoft invests $10B in OpenAI partnership.</NewsItem>
        </RightPanel>
      </MainContent>
    </AppBackground>
  );
}

export default App
