import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

import App from '../App';

describe('App navigation', () => {
  it('renders shell and role-aware links', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(screen.getByTestId('app-shell')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /admin/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /notifications/i })).toBeInTheDocument();
  });
});
