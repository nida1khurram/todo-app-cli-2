import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock component for task form since it's inline in the page
const TaskForm = ({
  onSubmit,
  isLoading = false,
}: {
  onSubmit: (data: { title: string; description?: string; priority: string; tags: string[] }) => void;
  isLoading?: boolean;
}) => {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    onSubmit({
      title: formData.get('title') as string,
      description: formData.get('description') as string || undefined,
      priority: formData.get('priority') as string || 'medium',
      tags: [],
    });
  };

  return (
    <form onSubmit={handleSubmit} data-testid="task-form">
      <input name="title" placeholder="Task title" required aria-label="Title" />
      <textarea name="description" placeholder="Description" aria-label="Description" />
      <select name="priority" aria-label="Priority" defaultValue="medium">
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Creating...' : 'Create Task'}
      </button>
    </form>
  );
};

describe('TaskForm Component', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form with all fields', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/priority/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create/i })).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/title/i);
    const descInput = screen.getByLabelText(/description/i);
    const submitButton = screen.getByRole('button', { name: /create/i });

    await userEvent.type(titleInput, 'New Task');
    await userEvent.type(descInput, 'Task description');
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith({
      title: 'New Task',
      description: 'Task description',
      priority: 'medium',
      tags: [],
    });
  });

  it('requires title field', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/title/i);
    expect(titleInput).toBeRequired();
  });

  it('allows selecting priority', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const prioritySelect = screen.getByLabelText(/priority/i);
    await userEvent.selectOptions(prioritySelect, 'high');

    const titleInput = screen.getByLabelText(/title/i);
    await userEvent.type(titleInput, 'High Priority Task');

    const submitButton = screen.getByRole('button', { name: /create/i });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ priority: 'high' })
    );
  });

  it('description is optional', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/title/i);
    await userEvent.type(titleInput, 'Task without description');

    const submitButton = screen.getByRole('button', { name: /create/i });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ description: undefined })
    );
  });

  it('disables submit button when loading', () => {
    render(<TaskForm onSubmit={mockOnSubmit} isLoading={true} />);

    const submitButton = screen.getByRole('button');
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent(/creating/i);
  });

  it('default priority is medium', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const prioritySelect = screen.getByLabelText(/priority/i) as HTMLSelectElement;
    expect(prioritySelect.value).toBe('medium');
  });
});
