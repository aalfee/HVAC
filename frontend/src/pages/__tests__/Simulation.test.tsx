import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Simulation from '../Simulation';

describe('Simulation Page', () => {
  it('renders form and submits', () => {
    render(<Simulation />);
    expect(screen.getByText(/Simulation Control/i)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/Building ID/i), { target: { value: 'B1' } });
    fireEvent.change(screen.getByLabelText(/Start Time/i), { target: { value: '2025-10-03T10:00' } });
    fireEvent.change(screen.getByLabelText(/End Time/i), { target: { value: '2025-10-03T12:00' } });
    fireEvent.change(screen.getByLabelText(/Parameters/i), { target: { value: '{"temp": 22}' } });
    expect(screen.getByRole('button', { name: /Run Simulation/i })).toBeInTheDocument();
  });
});
