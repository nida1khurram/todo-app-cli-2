import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import RegisterPage from '@/app/(auth)/register/page';
import { authApi } from '@/lib/api-client';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  authApi: {
    register: jest.fn(),
  },
}));

// Mock next/navigation
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: jest.fn(),
    prefetch: jest.fn(),
  }),
}));

describe('Register Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders registration form', () => {
    render(<RegisterPage />);

    expect(screen.getByText(/create.*account/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up|register|create/i })).toBeInTheDocument();
  });

  it('shows validation error for invalid email', async () => {
    render(<RegisterPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /sign up|register|create/i });

    await userEvent.type(emailInput, 'invalid-email');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/valid email|invalid email/i)).toBeInTheDocument();
    });
  });

  it('shows validation error for short password', async () => {
    render(<RegisterPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const submitButton = screen.getByRole('button', { name: /sign up|register|create/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, '123');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/password.*characters|too short/i)).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    (authApi.register as jest.Mock).mockResolvedValue({ id: 1, email: 'test@example.com' });

    render(<RegisterPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const submitButton = screen.getByRole('button', { name: /sign up|register|create/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(authApi.register).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'SecurePass123!',
      });
    });
  });

  it('shows error message on registration failure', async () => {
    (authApi.register as jest.Mock).mockRejectedValue(new Error('Email already exists'));

    render(<RegisterPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const submitButton = screen.getByRole('button', { name: /sign up|register|create/i });

    await userEvent.type(emailInput, 'existing@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/error|failed|already exists/i)).toBeInTheDocument();
    });
  });

  it('redirects to login after successful registration', async () => {
    (authApi.register as jest.Mock).mockResolvedValue({ id: 1, email: 'test@example.com' });

    render(<RegisterPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const submitButton = screen.getByRole('button', { name: /sign up|register|create/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/login');
    });
  });

  it('has link to login page', () => {
    render(<RegisterPage />);

    const loginLink = screen.getByRole('link', { name: /sign in|log in|login/i });
    expect(loginLink).toHaveAttribute('href', '/login');
  });

  it('disables submit button while submitting', async () => {
    (authApi.register as jest.Mock).mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(<RegisterPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const submitButton = screen.getByRole('button', { name: /sign up|register|create/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    expect(submitButton).toBeDisabled();
  });
});
