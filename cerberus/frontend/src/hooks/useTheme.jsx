import { createContext, useContext, useEffect, useMemo, useState } from 'react';

const ThemeContext = createContext(null);

const THEME_KEY = 'cerberus_theme';
const BRAND_KEY = 'cerberus_brand';

const initialBrand = {
  color: '#0284c7',
  logo: '',
  background: ''
};

export function ThemeProvider({ children }) {
  const [themeMode, setThemeMode] = useState(localStorage.getItem(THEME_KEY) || 'system');
  const [highContrast, setHighContrast] = useState(false);
  const [brand, setBrand] = useState(() => {
    const raw = localStorage.getItem(BRAND_KEY);
    return raw ? JSON.parse(raw) : initialBrand;
  });

  useEffect(() => {
    const root = document.documentElement;
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const applyDark = themeMode === 'dark' || (themeMode === 'system' && systemDark);
    root.classList.toggle('dark', applyDark);
    root.classList.toggle('high-contrast', highContrast);
    root.style.setProperty('--brand-primary', brand.color);
    localStorage.setItem(THEME_KEY, themeMode);
    localStorage.setItem(BRAND_KEY, JSON.stringify(brand));
  }, [themeMode, highContrast, brand]);

  const value = useMemo(
    () => ({
      themeMode,
      setThemeMode,
      highContrast,
      setHighContrast,
      brand,
      setBrand
    }),
    [themeMode, highContrast, brand]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error('useTheme must be used inside ThemeProvider');
  }
  return ctx;
}
