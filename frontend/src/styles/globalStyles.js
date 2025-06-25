import { createGlobalStyle } from 'styled-components';
import theme from './theme';

const GlobalStyles = createGlobalStyle`
  body {
    background: ${theme.colors.background};
    color: ${theme.colors.text.primary};
    font-family: ${theme.typography.fontFamily.primary};
    margin: 0;
    padding: 0;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  
  #root {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: ${theme.colors.background};
  }

  .glass {
    background: ${theme.colors.overlay.glass};
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 32px 0 rgba(0,0,0,0.24);
  }
`;

export default GlobalStyles; 