import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import AdminPanelPage from '../pages/AdminPanelPage';

vi.mock('../services/challengeService', () => ({
  deleteChallenge: vi.fn(() => Promise.resolve({ deleted: true, id: 1 }))
}));

describe('AdminPanelPage destructive confirmation', () => {
  it('requires confirmation phrase before delete', async () => {
    const promptSpy = vi.spyOn(window, 'prompt').mockReturnValue('wrong-confirmation');

    render(<AdminPanelPage />);

    fireEvent.click(screen.getByRole('button', { name: /delete challenge #1/i }));

    await waitFor(() => {
      expect(screen.getByText(/confirmation phrase mismatch/i)).toBeInTheDocument();
    });

    promptSpy.mockRestore();
  });
});
