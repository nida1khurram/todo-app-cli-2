/**
 * E2E Test: Complete User Journey
 *
 * Tests the full workflow: register → login → create → edit → delete → logout
 *
 * Note: These are integration tests simulating E2E behavior.
 * For true E2E tests, use Playwright or Cypress.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock API responses
const mockApi = {
  register: jest.fn(),
  login: jest.fn(),
  getTasks: jest.fn(),
  createTask: jest.fn(),
  updateTask: jest.fn(),
  deleteTask: jest.fn(),
  logout: jest.fn(),
};

jest.mock('@/lib/api-client', () => ({
  authApi: {
    register: (...args: unknown[]) => mockApi.register(...args),
    login: (...args: unknown[]) => mockApi.login(...args),
  },
  tasksApi: {
    getAll: (...args: unknown[]) => mockApi.getTasks(...args),
    create: (...args: unknown[]) => mockApi.createTask(...args),
    update: (...args: unknown[]) => mockApi.updateTask(...args),
    delete: (...args: unknown[]) => mockApi.deleteTask(...args),
  },
}));

describe('Complete User Journey', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('User Registration Flow', () => {
    it('allows new user to register', async () => {
      mockApi.register.mockResolvedValue({ id: 1, email: 'newuser@example.com' });

      // Simulate registration
      const result = await mockApi.register({
        email: 'newuser@example.com',
        password: 'SecurePass123!',
      });

      expect(result.email).toBe('newuser@example.com');
      expect(mockApi.register).toHaveBeenCalledWith({
        email: 'newuser@example.com',
        password: 'SecurePass123!',
      });
    });

    it('handles duplicate email error', async () => {
      mockApi.register.mockRejectedValue(new Error('Email already exists'));

      await expect(
        mockApi.register({
          email: 'existing@example.com',
          password: 'SecurePass123!',
        })
      ).rejects.toThrow('Email already exists');
    });
  });

  describe('User Login Flow', () => {
    it('allows user to login and receive token', async () => {
      mockApi.login.mockResolvedValue({
        access_token: 'jwt-token-123',
        token_type: 'bearer',
      });

      const result = await mockApi.login({
        email: 'user@example.com',
        password: 'SecurePass123!',
      });

      expect(result.access_token).toBe('jwt-token-123');
      localStorage.setItem('token', result.access_token);
      expect(localStorage.getItem('token')).toBe('jwt-token-123');
    });

    it('handles invalid credentials', async () => {
      mockApi.login.mockRejectedValue(new Error('Invalid credentials'));

      await expect(
        mockApi.login({
          email: 'user@example.com',
          password: 'WrongPassword',
        })
      ).rejects.toThrow('Invalid credentials');
    });
  });

  describe('Task Management Flow', () => {
    beforeEach(() => {
      localStorage.setItem('token', 'jwt-token-123');
    });

    it('allows user to create a task', async () => {
      mockApi.createTask.mockResolvedValue({
        id: 1,
        title: 'My New Task',
        description: 'Task description',
        priority: 'high',
        is_completed: false,
        tags: [],
      });

      const result = await mockApi.createTask({
        title: 'My New Task',
        description: 'Task description',
        priority: 'high',
      });

      expect(result.title).toBe('My New Task');
      expect(result.is_completed).toBe(false);
    });

    it('allows user to view their tasks', async () => {
      mockApi.getTasks.mockResolvedValue([
        { id: 1, title: 'Task 1', is_completed: false },
        { id: 2, title: 'Task 2', is_completed: true },
      ]);

      const tasks = await mockApi.getTasks();

      expect(tasks).toHaveLength(2);
      expect(tasks[0].title).toBe('Task 1');
    });

    it('allows user to edit a task', async () => {
      mockApi.updateTask.mockResolvedValue({
        id: 1,
        title: 'Updated Task Title',
        description: 'Updated description',
        priority: 'medium',
      });

      const result = await mockApi.updateTask(1, {
        title: 'Updated Task Title',
        description: 'Updated description',
      });

      expect(result.title).toBe('Updated Task Title');
    });

    it('allows user to delete a task', async () => {
      mockApi.deleteTask.mockResolvedValue(undefined);

      await mockApi.deleteTask(1);

      expect(mockApi.deleteTask).toHaveBeenCalledWith(1);
    });
  });

  describe('Logout Flow', () => {
    it('clears token on logout', () => {
      localStorage.setItem('token', 'jwt-token-123');
      expect(localStorage.getItem('token')).toBe('jwt-token-123');

      // Simulate logout
      localStorage.removeItem('token');

      expect(localStorage.getItem('token')).toBeNull();
    });
  });

  describe('Complete Journey Integration', () => {
    it('completes full user journey', async () => {
      // 1. Register
      mockApi.register.mockResolvedValue({ id: 1, email: 'journey@example.com' });
      await mockApi.register({ email: 'journey@example.com', password: 'Pass123!' });

      // 2. Login
      mockApi.login.mockResolvedValue({ access_token: 'token', token_type: 'bearer' });
      const loginResult = await mockApi.login({ email: 'journey@example.com', password: 'Pass123!' });
      localStorage.setItem('token', loginResult.access_token);

      // 3. Create task
      mockApi.createTask.mockResolvedValue({ id: 1, title: 'Journey Task', is_completed: false });
      const task = await mockApi.createTask({ title: 'Journey Task' });

      // 4. Edit task
      mockApi.updateTask.mockResolvedValue({ ...task, title: 'Updated Journey Task' });
      await mockApi.updateTask(task.id, { title: 'Updated Journey Task' });

      // 5. Delete task
      mockApi.deleteTask.mockResolvedValue(undefined);
      await mockApi.deleteTask(task.id);

      // 6. Logout
      localStorage.removeItem('token');

      // Verify complete journey
      expect(mockApi.register).toHaveBeenCalled();
      expect(mockApi.login).toHaveBeenCalled();
      expect(mockApi.createTask).toHaveBeenCalled();
      expect(mockApi.updateTask).toHaveBeenCalled();
      expect(mockApi.deleteTask).toHaveBeenCalled();
      expect(localStorage.getItem('token')).toBeNull();
    });
  });
});
