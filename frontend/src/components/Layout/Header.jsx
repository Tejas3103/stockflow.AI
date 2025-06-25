import React from 'react';
import styled from 'styled-components';

const HeaderBar = styled.header`
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  padding: 20px 40px 16px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: ${({ theme }) => theme.colors.overlay.glass};
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 0 0 24px 24px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.18), 0 1.5px 0 0 rgba(0,0,0,0.10);
  border-bottom: 1px solid rgba(255,255,255,0.10);
  position: sticky;
  top: 0;
  left: 0;
  z-index: 100;
`;

const Brand = styled.div`
  font-family: ${({ theme }) => theme.typography.fontFamily.primary};
  font-size: 1.6rem;
  font-weight: 700;
  color: ${({ theme }) => theme.colors.accent.teal};
  letter-spacing: 1px;
  display: flex;
  align-items: center;
`;

const Status = styled.div`
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.text.secondary};
  background: ${({ theme }) => theme.colors.surface};
  padding: 6px 16px;
  border-radius: 16px;
  font-weight: 500;
  margin-left: 16px;
`;

const Header = () => {
  return (
    <HeaderBar>
      <Brand>
        {/* Optionally add a logo SVG here */}
        Stockflow<span style={{ color: '#fff', marginLeft: 2 }}>.AI</span>
      </Brand>
      <Status>
        {/* Placeholder for market status */}
        Market Status: <span style={{ color: '#00c896', fontWeight: 600 }}>Open</span>
      </Status>
    </HeaderBar>
  );
};

export default Header; 