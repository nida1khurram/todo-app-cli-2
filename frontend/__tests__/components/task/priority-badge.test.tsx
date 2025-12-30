import { render, screen } from '@testing-library/react';
import { PriorityBadge } from '@/components/task/priority-badge';

describe('PriorityBadge Component', () => {
  it('renders high priority with red color', () => {
    render(<PriorityBadge priority="high" />);
    const badge = screen.getByText('high');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-red-100', 'text-red-700');
  });

  it('renders medium priority with yellow color', () => {
    render(<PriorityBadge priority="medium" />);
    const badge = screen.getByText('medium');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-700');
  });

  it('renders low priority with green color', () => {
    render(<PriorityBadge priority="low" />);
    const badge = screen.getByText('low');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-green-100', 'text-green-700');
  });

  it('renders priority text', () => {
    render(<PriorityBadge priority="high" />);
    expect(screen.getByText('high')).toBeInTheDocument();
  });

  it('has rounded-full class for pill shape', () => {
    render(<PriorityBadge priority="medium" />);
    const badge = screen.getByText('medium');
    expect(badge).toHaveClass('rounded-full');
  });
});
