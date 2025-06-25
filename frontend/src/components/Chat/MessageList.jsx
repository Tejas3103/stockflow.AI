import React, { useRef, useEffect } from 'react';
import ChatBubble from './ChatBubble';
import styled from 'styled-components';

const ListContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 24px 16px 0 16px;
`;

const MessageList = ({ messages }) => {
  const bottomRef = useRef(null);
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);
  return (
    <ListContainer>
      {messages.map((msg, idx) => (
        <ChatBubble key={idx} sender={msg.sender} text={msg.text} />
      ))}
      <div ref={bottomRef} />
    </ListContainer>
  );
};

export default MessageList; 