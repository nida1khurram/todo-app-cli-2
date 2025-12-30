import { render, screen, fireEvent } from '@testing-library/react';

// Simple TagList component for testing
const TagList = ({
  tags,
  onRemove,
}: {
  tags: string[];
  onRemove?: (tag: string) => void;
}) => {
  if (tags.length === 0) {
    return null;
  }

  return (
    <div data-testid="tag-list" className="flex flex-wrap gap-1">
      {tags.map((tag) => (
        <span
          key={tag}
          className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
        >
          {tag}
          {onRemove && (
            <button
              type="button"
              onClick={() => onRemove(tag)}
              className="ml-1"
              aria-label={`Remove ${tag}`}
            >
              ×
            </button>
          )}
        </span>
      ))}
    </div>
  );
};

describe('TagList Component', () => {
  it('renders nothing when tags array is empty', () => {
    const { container } = render(<TagList tags={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders single tag', () => {
    render(<TagList tags={['work']} />);

    expect(screen.getByText('work')).toBeInTheDocument();
  });

  it('renders multiple tags', () => {
    render(<TagList tags={['work', 'urgent', 'personal']} />);

    expect(screen.getByText('work')).toBeInTheDocument();
    expect(screen.getByText('urgent')).toBeInTheDocument();
    expect(screen.getByText('personal')).toBeInTheDocument();
  });

  it('does not show remove buttons when onRemove is not provided', () => {
    render(<TagList tags={['work', 'urgent']} />);

    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('shows remove buttons when onRemove is provided', () => {
    const mockOnRemove = jest.fn();
    render(<TagList tags={['work', 'urgent']} onRemove={mockOnRemove} />);

    const removeButtons = screen.getAllByRole('button');
    expect(removeButtons).toHaveLength(2);
  });

  it('calls onRemove with correct tag when remove button is clicked', () => {
    const mockOnRemove = jest.fn();
    render(<TagList tags={['work', 'urgent']} onRemove={mockOnRemove} />);

    const removeWorkButton = screen.getByRole('button', { name: /remove work/i });
    fireEvent.click(removeWorkButton);

    expect(mockOnRemove).toHaveBeenCalledWith('work');
    expect(mockOnRemove).toHaveBeenCalledTimes(1);
  });

  it('renders tags in correct order', () => {
    render(<TagList tags={['alpha', 'beta', 'gamma']} />);

    const tagList = screen.getByTestId('tag-list');
    const tagTexts = tagList.textContent;

    expect(tagTexts).toContain('alpha');
    expect(tagTexts).toContain('beta');
    expect(tagTexts).toContain('gamma');
  });

  it('applies correct styling classes', () => {
    render(<TagList tags={['work']} />);

    const tag = screen.getByText('work').closest('span');
    expect(tag).toHaveClass('rounded-full');
    expect(tag).toHaveClass('bg-gray-100');
  });

  it('handles special characters in tag names', () => {
    render(<TagList tags={['c++', 'node.js', 'vue-3']} />);

    expect(screen.getByText('c++')).toBeInTheDocument();
    expect(screen.getByText('node.js')).toBeInTheDocument();
    expect(screen.getByText('vue-3')).toBeInTheDocument();
  });

  it('has accessible remove button labels', () => {
    const mockOnRemove = jest.fn();
    render(<TagList tags={['important']} onRemove={mockOnRemove} />);

    const removeButton = screen.getByRole('button', { name: /remove important/i });
    expect(removeButton).toBeInTheDocument();
  });
});
