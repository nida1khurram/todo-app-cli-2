import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { TaskCard } from '@/components/task/task-card';
import { Task } from '@/types/task';
import { tasksApi } from '@/lib/api-client';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  tasksApi: {
    toggleComplete: jest.fn(),
    delete: jest.fn(),
  },
}));

// Mock the toast hook
jest.mock('@/components/ui/toast', () => ({
  useToast: () => ({
    addToast: jest.fn(),
  }),
}));

const mockTask: Task = {
  id: 1,
  user_id: 1,
  title: 'Test Task',
  description: 'Test description',
  is_completed: false,
  priority: 'medium',
  tags: ['work', 'urgent'],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

describe('TaskCard Component', () => {
  const mockOnUpdate = jest.fn();
  const mockOnEdit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task title', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('renders task description', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText('Test description')).toBeInTheDocument();
  });

  it('renders priority badge', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText('medium')).toBeInTheDocument();
  });

  it('renders tags', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText('work')).toBeInTheDocument();
    expect(screen.getByText('urgent')).toBeInTheDocument();
  });

  it('renders checkbox for completion', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).not.toBeChecked();
  });

  it('renders checkbox as checked for completed task', () => {
    const completedTask = { ...mockTask, is_completed: true };
    render(<TaskCard task={completedTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).toBeChecked();
  });

  it('applies strikethrough style for completed task', () => {
    const completedTask = { ...mockTask, is_completed: true };
    render(<TaskCard task={completedTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText('Test Task')).toHaveClass('line-through');
  });

  it('calls onEdit when edit button is clicked', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    fireEvent.click(screen.getByText('Edit'));
    expect(mockOnEdit).toHaveBeenCalledWith(mockTask);
  });

  it('toggles completion when checkbox is clicked', async () => {
    (tasksApi.toggleComplete as jest.Mock).mockResolvedValue({});
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(tasksApi.toggleComplete).toHaveBeenCalledWith(mockTask.id);
    });
  });

  it('calls onUpdate after successful toggle', async () => {
    (tasksApi.toggleComplete as jest.Mock).mockResolvedValue({});
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(mockOnUpdate).toHaveBeenCalled();
    });
  });

  it('shows delete button', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText('Delete')).toBeInTheDocument();
  });

  it('asks for confirmation before deleting', () => {
    window.confirm = jest.fn(() => false);
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);

    fireEvent.click(screen.getByText('Delete'));

    expect(window.confirm).toHaveBeenCalled();
    expect(tasksApi.delete).not.toHaveBeenCalled();
  });

  it('deletes task when confirmed', async () => {
    window.confirm = jest.fn(() => true);
    (tasksApi.delete as jest.Mock).mockResolvedValue({});
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);

    fireEvent.click(screen.getByText('Delete'));

    await waitFor(() => {
      expect(tasksApi.delete).toHaveBeenCalledWith(mockTask.id);
    });
  });

  it('renders created date', () => {
    render(<TaskCard task={mockTask} onUpdate={mockOnUpdate} onEdit={mockOnEdit} />);
    expect(screen.getByText(/Created:/)).toBeInTheDocument();
  });
});
