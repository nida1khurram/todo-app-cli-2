import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginPage from '@/app/(auth)/login/page';
import { authApi } from '@/lib/api-client';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  authApi: {
    login: jest.fn(),
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

describe('Login Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  it('renders login form', () => {
    render(<LoginPage />);

    expect(screen.getByText(/sign in|log in|welcome/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in|log in/i })).toBeInTheDocument();
  });

  it('shows validation error for empty email', async () => {
    render(<LoginPage />);

    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/email.*required|enter.*email/i)).toBeInTheDocument();
    });
  });

  it('shows validation error for empty password', async () => {
    render(<LoginPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });

    await userEvent.type(emailInput, 'test@example.com');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/password.*required|enter.*password/i)).toBeInTheDocument();
    });
  });

  it('submits form with valid credentials', async () => {
    (authApi.login as jest.Mock).mockResolvedValue({
      access_token: 'test-token',
      token_type: 'bearer',
    });

    render(<LoginPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(authApi.login).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'SecurePass123!',
      });
    });
  });

  it('stores token in localStorage on successful login', async () => {
    (authApi.login as jest.Mock).mockResolvedValue({
      access_token: 'test-token',
      token_type: 'bearer',
    });

    render(<LoginPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(localStorage.setItem).toHaveBeenCalledWith('token', 'test-token');
    });
  });

  it('shows error message on login failure', async () => {
    (authApi.login as jest.Mock).mockRejectedValue(new Error('Invalid credentials'));

    render(<LoginPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'WrongPassword');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid|incorrect|failed/i)).toBeInTheDocument();
    });
  });

  it('redirects to tasks page after successful login', async () => {
    (authApi.login as jest.Mock).mockResolvedValue({
      access_token: 'test-token',
      token_type: 'bearer',
    });

    render(<LoginPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/tasks');
    });
  });

  it('has link to register page', () => {
    render(<LoginPage />);

    const registerLink = screen.getByRole('link', { name: /sign up|register|create.*account/i });
    expect(registerLink).toHaveAttribute('href', '/register');
  });

  it('disables submit button while submitting', async () => {
    (authApi.login as jest.Mock).mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(<LoginPage />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in|log in/i });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'SecurePass123!');
    fireEvent.click(submitButton);

    expect(submitButton).toBeDisabled();
  });
});
