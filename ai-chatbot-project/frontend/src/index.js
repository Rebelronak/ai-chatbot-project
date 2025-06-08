import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Modern React 18 rendering method
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);