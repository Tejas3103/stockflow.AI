import React from 'react';
import styled, { css } from 'styled-components';

const Bubble = styled.div`
  padding: 12px 16px;
  max-width: 80%;
  margin: 8px 0;
  border-radius: 20px 20px 8px 20px;
  font-size: 16px;
  word-break: break-word;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.10);
  transition: background 0.3s, color 0.3s;
  ${({ sender, theme }) => sender === 'user' ? css`
    background: ${theme.colors.accent.teal};
    color: #000;
    align-self: flex-end;
    border-radius: 20px 20px 8px 20px;
  ` : css`
    background: ${theme.colors.surface};
    color: ${theme.colors.text.primary};
    align-self: flex-start;
    border-radius: 20px 20px 20px 8px;
    backdrop-filter: blur(8px) saturate(180%);
    -webkit-backdrop-filter: blur(8px) saturate(180%);
  `}
`;

const ChatBubble = ({ sender, text }) => {
  return <Bubble sender={sender}>{text}</Bubble>;
};

export default ChatBubble; 