import React from 'react';
import styled from 'styled-components';

const Card = styled.div`
  background: ${({ theme }) => theme.colors.overlay.glass};
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-radius: 20px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.16);
  border: 1px solid rgba(255,255,255,0.10);
  padding: 20px 24px;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 220px;
`;

const Row = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Name = styled.div`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.text.primary};
`;

const Ticker = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: ${({ theme }) => theme.colors.accent.teal};
  background: ${({ theme }) => theme.colors.surface};
  border-radius: 8px;
  padding: 2px 10px;
  margin-left: 8px;
`;

const Price = styled.div`
  font-size: 1.2rem;
  font-weight: 700;
  color: ${({ theme }) => theme.colors.text.primary};
`;

const Change = styled.div`
  font-size: 1rem;
  font-weight: 600;
  color: ${({ change, theme }) => change >= 0 ? theme.colors.accent.green : theme.colors.accent.red};
  margin-left: 10px;
`;

const Recommendation = styled.div`
  font-size: 0.98rem;
  color: ${({ theme }) => theme.colors.text.secondary};
  margin-top: 6px;
`;

const StockCard = ({ name, ticker, price, change, recommendation }) => {
  return (
    <Card>
      <Row>
        <Name>{name}</Name>
        <Ticker>{ticker}</Ticker>
      </Row>
      <Row>
        <Price>${price}</Price>
        <Change change={change}>{change >= 0 ? '+' : ''}{change}%</Change>
      </Row>
      <Recommendation>{recommendation}</Recommendation>
    </Card>
  );
};

export default StockCard; 