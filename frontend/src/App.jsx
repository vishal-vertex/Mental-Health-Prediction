import { createContext, useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import Home from './pages/Home/Home';
import Predict from './pages/Predict/Predict';
import About from './pages/About/About';
import NotFound from './pages/NotFound/NotFound';

export const ThemeContext = createContext();

function App() {
  const [theme, setTheme] = useState('dark');

  // Load theme preference
  useEffect(() => {
    const saved = localStorage.getItem('mhp_theme');
    if (saved) {
      setTheme(saved);
      document.documentElement.setAttribute('data-theme', saved);
    }
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => {
      const next = prev === 'dark' ? 'light' : 'dark';
      localStorage.setItem('mhp_theme', next);
      document.documentElement.setAttribute('data-theme', next);
      return next;
    });
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <BrowserRouter>
        <Navbar />
        <div style={{ paddingTop: '76px', minHeight: 'calc(100vh - 76px)' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
        <Footer />
        <Toaster 
          position="bottom-right"
          toastOptions={{
            style: {
              background: 'var(--clr-bg-tertiary)',
              color: 'var(--clr-text-primary)',
              border: '1px solid var(--clr-border)',
            }
          }}
        />
      </BrowserRouter>
    </ThemeContext.Provider>
  );
}

export default App;
