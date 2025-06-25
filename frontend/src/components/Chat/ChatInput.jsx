import React from 'react';
import styled from 'styled-components';

const InputRow = styled.div`
  display: flex;
  align-items: center;
  padding: 16px;
  background: ${({ theme }) => theme.colors.surfaceElevated};
  border-top: 1px solid rgba(255,255,255,0.08);
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 20px;
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.1);
  background: ${({ theme }) => theme.colors.surface};
  color: ${({ theme }) => theme.colors.text.primary};
  font-size: 16px;
  outline: none;
  margin-right: 12px;
  &::placeholder {
    color: ${({ theme }) => theme.colors.text.muted};
  }
`;

const SendButton = styled.button`
  background: ${({ theme }) => theme.colors.accent.teal};
  color: #000;
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
  &:hover:not(:disabled) {
    background: ${({ theme }) => theme.colors.accent.tealLight};
  }
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const ChatInput = ({ value, onChange, onSend, loading }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && value.trim() && !loading) {
      onSend();
    }
  };
  return (
    <InputRow>
      <Input
        type="text"
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        disabled={loading}
      />
      <SendButton onClick={onSend} disabled={loading || !value.trim()}>
        {loading ? '...' : 'Send'}
      </SendButton>
    </InputRow>
  );
};

export default ChatInput; 