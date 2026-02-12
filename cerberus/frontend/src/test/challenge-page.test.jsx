import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import ChallengePage from '../pages/ChallengePage';

vi.mock('../services/challengeService', () => ({
  submitFlag: vi.fn(() => Promise.resolve({ result: 'correct' })),
  toggleHint: vi.fn(() => Promise.resolve({ enabled: true }))
}));

describe('ChallengePage workflows', () => {
  it('submits a flag and shows result', async () => {
    render(<ChallengePage />);

    fireEvent.change(screen.getByLabelText(/submit flag/i), { target: { value: 'flag{ok}' } });
    fireEvent.click(screen.getByRole('button', { name: /^submit$/i }));

    await waitFor(() => {
      expect(screen.getByText(/submission result: correct/i)).toBeInTheDocument();
    });
  });

  it('toggles hint visibility from hidden to enabled', async () => {
    render(<ChallengePage />);

    expect(screen.getAllByText(/hint hidden/i).length).toBeGreaterThan(0);
    fireEvent.click(screen.getAllByRole('button', { name: /enable/i })[0]);

    await waitFor(() => {
      expect(screen.getByText(/check robots.txt/i)).toBeInTheDocument();
    });
  });
});
