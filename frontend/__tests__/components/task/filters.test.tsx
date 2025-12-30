import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Simple Filters component for testing
const Filters = ({
  status,
  priority,
  sortBy,
  sortOrder,
  onStatusChange,
  onPriorityChange,
  onSortByChange,
  onSortOrderChange,
  onClear,
}: {
  status: string;
  priority: string;
  sortBy: string;
  sortOrder: string;
  onStatusChange: (value: string) => void;
  onPriorityChange: (value: string) => void;
  onSortByChange: (value: string) => void;
  onSortOrderChange: (value: string) => void;
  onClear: () => void;
}) => {
  const hasActiveFilters = status !== 'all' || priority !== '' || sortBy !== 'created_at' || sortOrder !== 'desc';

  return (
    <div data-testid="filters">
      <select
        value={status}
        onChange={(e) => onStatusChange(e.target.value)}
        aria-label="Status filter"
      >
        <option value="all">All Tasks</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>

      <select
        value={priority}
        onChange={(e) => onPriorityChange(e.target.value)}
        aria-label="Priority filter"
      >
        <option value="">Any Priority</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      <select
        value={sortBy}
        onChange={(e) => onSortByChange(e.target.value)}
        aria-label="Sort by"
      >
        <option value="created_at">Date Created</option>
        <option value="priority">Priority</option>
        <option value="title">Title</option>
      </select>

      <select
        value={sortOrder}
        onChange={(e) => onSortOrderChange(e.target.value)}
        aria-label="Sort order"
      >
        <option value="desc">Descending</option>
        <option value="asc">Ascending</option>
      </select>

      {hasActiveFilters && (
        <button onClick={onClear}>Clear Filters</button>
      )}
    </div>
  );
};

describe('Filters Component', () => {
  const defaultProps = {
    status: 'all',
    priority: '',
    sortBy: 'created_at',
    sortOrder: 'desc',
    onStatusChange: jest.fn(),
    onPriorityChange: jest.fn(),
    onSortByChange: jest.fn(),
    onSortOrderChange: jest.fn(),
    onClear: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders all filter controls', () => {
    render(<Filters {...defaultProps} />);

    expect(screen.getByLabelText(/status filter/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/priority filter/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/sort by/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/sort order/i)).toBeInTheDocument();
  });

  it('calls onStatusChange when status is changed', async () => {
    render(<Filters {...defaultProps} />);

    const statusSelect = screen.getByLabelText(/status filter/i);
    await userEvent.selectOptions(statusSelect, 'completed');

    expect(defaultProps.onStatusChange).toHaveBeenCalledWith('completed');
  });

  it('calls onPriorityChange when priority is changed', async () => {
    render(<Filters {...defaultProps} />);

    const prioritySelect = screen.getByLabelText(/priority filter/i);
    await userEvent.selectOptions(prioritySelect, 'high');

    expect(defaultProps.onPriorityChange).toHaveBeenCalledWith('high');
  });

  it('calls onSortByChange when sort field is changed', async () => {
    render(<Filters {...defaultProps} />);

    const sortBySelect = screen.getByLabelText(/sort by/i);
    await userEvent.selectOptions(sortBySelect, 'title');

    expect(defaultProps.onSortByChange).toHaveBeenCalledWith('title');
  });

  it('calls onSortOrderChange when sort order is changed', async () => {
    render(<Filters {...defaultProps} />);

    const sortOrderSelect = screen.getByLabelText(/sort order/i);
    await userEvent.selectOptions(sortOrderSelect, 'asc');

    expect(defaultProps.onSortOrderChange).toHaveBeenCalledWith('asc');
  });

  it('shows clear button when filters are active', () => {
    render(<Filters {...defaultProps} status="completed" />);

    expect(screen.getByRole('button', { name: /clear filters/i })).toBeInTheDocument();
  });

  it('hides clear button when no filters are active', () => {
    render(<Filters {...defaultProps} />);

    expect(screen.queryByRole('button', { name: /clear filters/i })).not.toBeInTheDocument();
  });

  it('calls onClear when clear button is clicked', () => {
    render(<Filters {...defaultProps} status="completed" />);

    const clearButton = screen.getByRole('button', { name: /clear filters/i });
    fireEvent.click(clearButton);

    expect(defaultProps.onClear).toHaveBeenCalled();
  });

  it('displays current status value', () => {
    render(<Filters {...defaultProps} status="pending" />);

    const statusSelect = screen.getByLabelText(/status filter/i) as HTMLSelectElement;
    expect(statusSelect.value).toBe('pending');
  });

  it('displays current priority value', () => {
    render(<Filters {...defaultProps} priority="high" />);

    const prioritySelect = screen.getByLabelText(/priority filter/i) as HTMLSelectElement;
    expect(prioritySelect.value).toBe('high');
  });

  it('displays current sort values', () => {
    render(<Filters {...defaultProps} sortBy="title" sortOrder="asc" />);

    const sortBySelect = screen.getByLabelText(/sort by/i) as HTMLSelectElement;
    const sortOrderSelect = screen.getByLabelText(/sort order/i) as HTMLSelectElement;

    expect(sortBySelect.value).toBe('title');
    expect(sortOrderSelect.value).toBe('asc');
  });

  it('has all status options', () => {
    render(<Filters {...defaultProps} />);

    const statusSelect = screen.getByLabelText(/status filter/i);
    expect(statusSelect).toContainHTML('All Tasks');
    expect(statusSelect).toContainHTML('Pending');
    expect(statusSelect).toContainHTML('Completed');
  });

  it('has all priority options', () => {
    render(<Filters {...defaultProps} />);

    const prioritySelect = screen.getByLabelText(/priority filter/i);
    expect(prioritySelect).toContainHTML('Any Priority');
    expect(prioritySelect).toContainHTML('High');
    expect(prioritySelect).toContainHTML('Medium');
    expect(prioritySelect).toContainHTML('Low');
  });
});
