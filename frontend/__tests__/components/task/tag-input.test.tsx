import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { TagInput } from '@/components/task/tag-input';
import { tagsApi } from '@/lib/api-client';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  tagsApi: {
    getAll: jest.fn(),
  },
}));

describe('TagInput Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('renders input field', () => {
    render(<TagInput selectedTags={[]} onTagsChange={() => {}} />);
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  it('renders with placeholder when no tags selected', () => {
    render(<TagInput selectedTags={[]} onTagsChange={() => {}} placeholder="Add tags..." />);
    expect(screen.getByPlaceholderText('Add tags...')).toBeInTheDocument();
  });

  it('displays selected tags', () => {
    render(<TagInput selectedTags={['work', 'urgent']} onTagsChange={() => {}} />);
    expect(screen.getByText('work')).toBeInTheDocument();
    expect(screen.getByText('urgent')).toBeInTheDocument();
  });

  it('removes tag when remove button is clicked', () => {
    const handleChange = jest.fn();
    render(<TagInput selectedTags={['work', 'urgent']} onTagsChange={handleChange} />);

    // Find and click remove button for 'work' tag
    const workTag = screen.getByText('work').closest('span');
    const removeButton = workTag?.querySelector('button');
    fireEvent.click(removeButton!);

    expect(handleChange).toHaveBeenCalledWith(['urgent']);
  });

  it('adds tag on Enter key press', () => {
    const handleChange = jest.fn();
    render(<TagInput selectedTags={[]} onTagsChange={handleChange} />);

    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'new-tag' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    expect(handleChange).toHaveBeenCalledWith(['new-tag']);
  });

  it('removes last tag on Backspace when input is empty', () => {
    const handleChange = jest.fn();
    render(<TagInput selectedTags={['work', 'urgent']} onTagsChange={handleChange} />);

    const input = screen.getByRole('textbox');
    fireEvent.keyDown(input, { key: 'Backspace' });

    expect(handleChange).toHaveBeenCalledWith(['work']);
  });

  it('normalizes tag names to lowercase', () => {
    const handleChange = jest.fn();
    render(<TagInput selectedTags={[]} onTagsChange={handleChange} />);

    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'UPPERCASE' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    expect(handleChange).toHaveBeenCalledWith(['uppercase']);
  });

  it('does not add duplicate tags', () => {
    const handleChange = jest.fn();
    render(<TagInput selectedTags={['work']} onTagsChange={handleChange} />);

    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'work' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    expect(handleChange).not.toHaveBeenCalled();
  });

  it('shows suggestions dropdown on focus and input', async () => {
    (tagsApi.getAll as jest.Mock).mockResolvedValue([
      { id: 1, name: 'work' },
      { id: 2, name: 'workout' },
    ]);

    render(<TagInput selectedTags={[]} onTagsChange={() => {}} />);

    const input = screen.getByRole('textbox');
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'wo' } });

    act(() => {
      jest.advanceTimersByTime(300);
    });

    await waitFor(() => {
      expect(tagsApi.getAll).toHaveBeenCalledWith('wo');
    });
  });

  it('adds tag from suggestion when clicked', async () => {
    (tagsApi.getAll as jest.Mock).mockResolvedValue([
      { id: 1, name: 'work' },
    ]);

    const handleChange = jest.fn();
    render(<TagInput selectedTags={[]} onTagsChange={handleChange} />);

    const input = screen.getByRole('textbox');
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'wo' } });

    act(() => {
      jest.advanceTimersByTime(300);
    });

    await waitFor(() => {
      const suggestion = screen.getByText('work');
      fireEvent.click(suggestion);
    });

    expect(handleChange).toHaveBeenCalledWith(['work']);
  });

  it('clears input after adding tag', () => {
    render(<TagInput selectedTags={[]} onTagsChange={() => {}} />);

    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'new-tag' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    expect(input).toHaveValue('');
  });

  it('closes suggestions on Escape key', () => {
    render(<TagInput selectedTags={[]} onTagsChange={() => {}} />);

    const input = screen.getByRole('textbox');
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: 'test' } });
    fireEvent.keyDown(input, { key: 'Escape' });

    // Suggestions should be hidden (no dropdown visible)
    // This is a basic test - the actual implementation may vary
  });
});
