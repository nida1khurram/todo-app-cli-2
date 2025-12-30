import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { SearchBar } from '@/components/task/search-bar';

describe('SearchBar Component', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('renders search input', () => {
    render(<SearchBar value="" onChange={() => {}} />);
    expect(screen.getByRole('searchbox')).toBeInTheDocument();
  });

  it('renders with placeholder', () => {
    render(<SearchBar value="" onChange={() => {}} placeholder="Search tasks..." />);
    expect(screen.getByPlaceholderText('Search tasks...')).toBeInTheDocument();
  });

  it('displays current value', () => {
    render(<SearchBar value="test query" onChange={() => {}} />);
    expect(screen.getByRole('searchbox')).toHaveValue('test query');
  });

  it('calls onChange with debounce', async () => {
    const handleChange = jest.fn();
    render(<SearchBar value="" onChange={handleChange} />);

    const input = screen.getByRole('searchbox');
    fireEvent.change(input, { target: { value: 'test' } });

    // Should not be called immediately
    expect(handleChange).not.toHaveBeenCalled();

    // Advance timers by debounce delay
    act(() => {
      jest.advanceTimersByTime(300);
    });

    expect(handleChange).toHaveBeenCalledWith('test');
  });

  it('shows clear button when value is present', () => {
    render(<SearchBar value="test" onChange={() => {}} />);
    // Look for clear button (X icon)
    const clearButton = screen.getByRole('button');
    expect(clearButton).toBeInTheDocument();
  });

  it('does not show clear button when value is empty', () => {
    render(<SearchBar value="" onChange={() => {}} />);
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('clears input when clear button is clicked', () => {
    const handleChange = jest.fn();
    render(<SearchBar value="test" onChange={handleChange} />);

    const clearButton = screen.getByRole('button');
    fireEvent.click(clearButton);

    expect(handleChange).toHaveBeenCalledWith('');
  });

  it('renders search icon', () => {
    render(<SearchBar value="" onChange={() => {}} />);
    // Check for SVG element (search icon)
    const svg = document.querySelector('svg');
    expect(svg).toBeInTheDocument();
  });

  it('updates local value on input change', () => {
    render(<SearchBar value="" onChange={() => {}} />);

    const input = screen.getByRole('searchbox');
    fireEvent.change(input, { target: { value: 'new search' } });

    expect(input).toHaveValue('new search');
  });

  it('syncs with external value changes', () => {
    const { rerender } = render(<SearchBar value="initial" onChange={() => {}} />);

    expect(screen.getByRole('searchbox')).toHaveValue('initial');

    rerender(<SearchBar value="updated" onChange={() => {}} />);

    expect(screen.getByRole('searchbox')).toHaveValue('updated');
  });
});
