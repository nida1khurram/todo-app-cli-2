import { render, screen, fireEvent } from '@testing-library/react';

// Simple DeleteModal component for testing
const DeleteModal = ({
  isOpen,
  taskTitle,
  onConfirm,
  onCancel,
  isDeleting = false,
}: {
  isOpen: boolean;
  taskTitle: string;
  onConfirm: () => void;
  onCancel: () => void;
  isDeleting?: boolean;
}) => {
  if (!isOpen) return null;

  return (
    <div data-testid="delete-modal" role="dialog" aria-modal="true">
      <div data-testid="backdrop" onClick={onCancel} />
      <div data-testid="modal-content">
        <h2>Delete Task</h2>
        <p>Are you sure you want to delete "{taskTitle}"?</p>
        <p>This action cannot be undone.</p>
        <div>
          <button onClick={onCancel} disabled={isDeleting}>
            Cancel
          </button>
          <button onClick={onConfirm} disabled={isDeleting}>
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
};

describe('DeleteModal Component', () => {
  const mockOnConfirm = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders nothing when not open', () => {
    const { container } = render(
      <DeleteModal
        isOpen={false}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('renders modal when open', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByTestId('delete-modal')).toBeInTheDocument();
    expect(screen.getByText(/delete task/i)).toBeInTheDocument();
  });

  it('displays task title in confirmation message', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="My Important Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText(/my important task/i)).toBeInTheDocument();
  });

  it('shows warning about action being irreversible', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText(/cannot be undone/i)).toBeInTheDocument();
  });

  it('calls onCancel when cancel button is clicked', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
    expect(mockOnConfirm).not.toHaveBeenCalled();
  });

  it('calls onConfirm when delete button is clicked', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /^delete$/i });
    fireEvent.click(deleteButton);

    expect(mockOnConfirm).toHaveBeenCalled();
    expect(mockOnCancel).not.toHaveBeenCalled();
  });

  it('calls onCancel when backdrop is clicked', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    const backdrop = screen.getByTestId('backdrop');
    fireEvent.click(backdrop);

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('disables buttons when deleting', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
        isDeleting={true}
      />
    );

    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    const deleteButton = screen.getByRole('button', { name: /deleting/i });

    expect(cancelButton).toBeDisabled();
    expect(deleteButton).toBeDisabled();
  });

  it('shows loading state when deleting', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
        isDeleting={true}
      />
    );

    expect(screen.getByText(/deleting/i)).toBeInTheDocument();
  });

  it('has proper aria attributes for accessibility', () => {
    render(
      <DeleteModal
        isOpen={true}
        taskTitle="Test Task"
        onConfirm={mockOnConfirm}
        onCancel={mockOnCancel}
      />
    );

    const modal = screen.getByRole('dialog');
    expect(modal).toHaveAttribute('aria-modal', 'true');
  });
});
