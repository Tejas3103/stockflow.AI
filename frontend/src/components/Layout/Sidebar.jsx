import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import StockCard from '../UI/StockCard';

const SidebarContainer = styled.aside`
  width: 240px;
  min-width: 180px;
  max-width: 260px;
  height: auto;
  max-height: calc(100vh - 80px);
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
  @media (max-width: 900px) {
    display: none;
  }
`;

const CardsWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
`;

const Sidebar = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('http://localhost:8000/top_stocks')
      .then(res => res.json())
      .then(data => {
        setStocks(data.stocks || []);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load stocks.');
        setLoading(false);
      });
  }, []);

  return (
    <SidebarContainer>
      <CardsWrapper>
        {loading && <div style={{ color: '#a0a0a0', marginTop: 24 }}>Loading top stocks...</div>}
        {error && <div style={{ color: '#ef4444', marginTop: 24 }}>{error}</div>}
        {!loading && !error && stocks.map(stock => (
          <StockCard
            key={stock.ticker}
            name={stock.name}
            ticker={stock.ticker}
            price={stock.price}
            change={stock.change}
            recommendation={stock.recommendation}
          />
        ))}
      </CardsWrapper>
    </SidebarContainer>
  );
};

export default Sidebar; 