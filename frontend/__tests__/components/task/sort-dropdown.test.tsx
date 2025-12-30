import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Simple SortDropdown component for testing
const SortDropdown = ({
  sortBy,
  sortOrder,
  onSortByChange,
  onSortOrderChange,
}: {
  sortBy: string;
  sortOrder: string;
  onSortByChange: (value: string) => void;
  onSortOrderChange: (value: string) => void;
}) => {
  return (
    <div data-testid="sort-controls" className="flex items-center gap-2">
      <label className="text-sm font-medium text-gray-700">Sort By:</label>
      <select
        value={sortBy}
        onChange={(e) => onSortByChange(e.target.value)}
        aria-label="Sort by"
        className="rounded-md border border-gray-300 px-3 py-2 text-sm"
      >
        <option value="created_at">Date Created</option>
        <option value="priority">Priority</option>
        <option value="title">Title</option>
      </select>

      <select
        value={sortOrder}
        onChange={(e) => onSortOrderChange(e.target.value)}
        aria-label="Sort order"
        className="rounded-md border border-gray-300 px-3 py-2 text-sm"
      >
        <option value="desc">Descending</option>
        <option value="asc">Ascending</option>
      </select>
    </div>
  );
};

describe('SortDropdown Component', () => {
  const defaultProps = {
    sortBy: 'created_at',
    sortOrder: 'desc',
    onSortByChange: jest.fn(),
    onSortOrderChange: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders sort controls', () => {
    render(<SortDropdown {...defaultProps} />);

    expect(screen.getByLabelText(/sort by/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/sort order/i)).toBeInTheDocument();
  });

  it('displays current sort values', () => {
    render(
      <SortDropdown
        {...defaultProps}
        sortBy="priority"
        sortOrder="asc"
      />
    );

    const sortBySelect = screen.getByLabelText(/sort by/i) as HTMLSelectElement;
    const sortOrderSelect = screen.getByLabelText(/sort order/i) as HTMLSelectElement;

    expect(sortBySelect.value).toBe('priority');
    expect(sortOrderSelect.value).toBe('asc');
  });

  it('calls onSortByChange when sort field is changed', async () => {
    render(<SortDropdown {...defaultProps} />);

    const sortBySelect = screen.getByLabelText(/sort by/i);
    await userEvent.selectOptions(sortBySelect, 'title');

    expect(defaultProps.onSortByChange).toHaveBeenCalledWith('title');
  });

  it('calls onSortOrderChange when order is changed', async () => {
    render(<SortDropdown {...defaultProps} />);

    const sortOrderSelect = screen.getByLabelText(/sort order/i);
    await userEvent.selectOptions(sortOrderSelect, 'asc');

    expect(defaultProps.onSortOrderChange).toHaveBeenCalledWith('asc');
  });

  it('has all sort by options', () => {
    render(<SortDropdown {...defaultProps} />);

    const sortBySelect = screen.getByLabelText(/sort by/i);
    expect(sortBySelect).toContainHTML('Date Created');
    expect(sortBySelect).toContainHTML('Priority');
    expect(sortBySelect).toContainHTML('Title');
  });

  it('has all sort order options', () => {
    render(<SortDropdown {...defaultProps} />);

    const sortOrderSelect = screen.getByLabelText(/sort order/i);
    expect(sortOrderSelect).toContainHTML('Descending');
    expect(sortOrderSelect).toContainHTML('Ascending');
  });

  it('default values are set correctly', () => {
    const props = {
      sortBy: 'created_at',
      sortOrder: 'desc',
      onSortByChange: jest.fn(),
      onSortOrderChange: jest.fn(),
    };

    render(<SortDropdown {...props} />);

    const sortBySelect = screen.getByLabelText(/sort by/i) as HTMLSelectElement;
    const sortOrderSelect = screen.getByLabelText(/sort order/i) as HTMLSelectElement;

    expect(sortBySelect.value).toBe('created_at');
    expect(sortOrderSelect.value).toBe('desc');
  });
});
