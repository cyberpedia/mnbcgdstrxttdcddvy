import { useEffect } from 'react';

export default function useKeyboardNav(listRef, onEnter) {
  useEffect(() => {
    const node = listRef.current;
    if (!node) return;

    const handler = (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      const selected = document.activeElement?.getAttribute('data-key');
      if (selected) {
        onEnter(selected);
      }
    };

    node.addEventListener('keydown', handler);
    return () => node.removeEventListener('keydown', handler);
  }, [listRef, onEnter]);
}
