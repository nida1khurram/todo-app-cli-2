import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { EditTaskModal } from '@/components/task/edit-task-modal';
import { Task } from '@/types/task';
import { tasksApi } from '@/lib/api-client';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  tasksApi: {
    update: jest.fn(),
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
  title: 'Original Title',
  description: 'Original description',
  is_completed: false,
  priority: 'medium',
  tags: ['work'],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

describe('EditTaskModal Component', () => {
  const mockOnClose = jest.fn();
  const mockOnUpdate = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders nothing when not open', () => {
    const { container } = render(
      <EditTaskModal
        task={mockTask}
        isOpen={false}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('renders modal when open', () => {
    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    expect(screen.getByText(/edit task/i)).toBeInTheDocument();
  });

  it('pre-fills form with task data', () => {
    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    expect(screen.getByDisplayValue('Original Title')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Original description')).toBeInTheDocument();
  });

  it('calls onClose when cancel button is clicked', () => {
    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelButton);

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('calls onClose when backdrop is clicked', () => {
    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    // Click on backdrop (the overlay div)
    const backdrop = document.querySelector('[aria-hidden="true"]');
    if (backdrop) {
      fireEvent.click(backdrop);
      expect(mockOnClose).toHaveBeenCalled();
    }
  });

  it('submits updated data', async () => {
    (tasksApi.update as jest.Mock).mockResolvedValue({});

    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    const titleInput = screen.getByDisplayValue('Original Title');
    await userEvent.clear(titleInput);
    await userEvent.type(titleInput, 'Updated Title');

    const saveButton = screen.getByRole('button', { name: /save/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(tasksApi.update).toHaveBeenCalledWith(
        mockTask.id,
        expect.objectContaining({ title: 'Updated Title' })
      );
    });
  });

  it('calls onUpdate and onClose after successful save', async () => {
    (tasksApi.update as jest.Mock).mockResolvedValue({});

    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    const saveButton = screen.getByRole('button', { name: /save/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockOnUpdate).toHaveBeenCalled();
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('shows error on save failure', async () => {
    (tasksApi.update as jest.Mock).mockRejectedValue(new Error('Failed to update'));

    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    const saveButton = screen.getByRole('button', { name: /save/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/failed to update/i)).toBeInTheDocument();
    });
  });

  it('allows changing priority', async () => {
    (tasksApi.update as jest.Mock).mockResolvedValue({});

    render(
      <EditTaskModal
        task={mockTask}
        isOpen={true}
        onClose={mockOnClose}
        onUpdate={mockOnUpdate}
      />
    );

    const prioritySelect = screen.getByRole('combobox');
    await userEvent.selectOptions(prioritySelect, 'high');

    const saveButton = screen.getByRole('button', { name: /save/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(tasksApi.update).toHaveBeenCalledWith(
        mockTask.id,
        expect.objectContaining({ priority: 'high' })
      );
    });
  });
});
