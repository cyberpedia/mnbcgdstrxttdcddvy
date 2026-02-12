import { useTheme } from '../hooks/useTheme';

function ThemeControls() {
  const { themeMode, setThemeMode, highContrast, setHighContrast, brand, setBrand } = useTheme();

  return (
    <section aria-label="Theme controls" className="flex flex-wrap items-center gap-2">
      <label className="text-sm" htmlFor="theme-mode">
        Theme
      </label>
      <select
        id="theme-mode"
        className="rounded border border-slate-400 bg-white px-2 py-1 text-sm dark:bg-slate-800"
        value={themeMode}
        onChange={(event) => setThemeMode(event.target.value)}
      >
        <option value="light">Light</option>
        <option value="dark">Dark</option>
        <option value="system">System</option>
      </select>

      <label className="flex items-center gap-1 text-sm" htmlFor="high-contrast">
        <input
          id="high-contrast"
          type="checkbox"
          checked={highContrast}
          onChange={(event) => setHighContrast(event.target.checked)}
        />
        High contrast
      </label>

      <label className="text-sm" htmlFor="brand-color">
        Brand color
      </label>
      <input
        id="brand-color"
        type="color"
        value={brand.color}
        onChange={(event) => setBrand({ ...brand, color: event.target.value })}
        aria-label="Brand color picker"
      />
    </section>
  );
}

export default ThemeControls;
