import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  width: 100%;
  max-width: 520px;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  background: ${({ theme }) => theme.colors.overlay.glass};
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 24px;
  box-shadow: 0 8px 40px 0 rgba(0,0,0,0.32);
  border: 1px solid rgba(255,255,255,0.10);
  overflow: hidden;
`;

const ChatContainer = ({ children }) => {
  return <Container className="glass">{children}</Container>;
};

export default ChatContainer; 