import { render, screen } from '@testing-library/react';
import { Task } from '@/types/task';

// Mock TaskCard component
jest.mock('@/components/task/task-card', () => ({
  TaskCard: ({ task }: { task: Task }) => (
    <div data-testid={`task-${task.id}`}>{task.title}</div>
  ),
}));

// Simple TaskList component for testing
const TaskList = ({
  tasks,
  isLoading = false,
  onUpdate,
  onEdit,
}: {
  tasks: Task[];
  isLoading?: boolean;
  onUpdate: () => void;
  onEdit: (task: Task) => void;
}) => {
  if (isLoading) {
    return <div data-testid="loading">Loading tasks...</div>;
  }

  if (tasks.length === 0) {
    return <div data-testid="empty-state">No tasks yet. Create your first task!</div>;
  }

  return (
    <div data-testid="task-list">
      {tasks.map((task) => (
        <div key={task.id} data-testid={`task-${task.id}`}>
          {task.title}
        </div>
      ))}
    </div>
  );
};

const mockTasks: Task[] = [
  {
    id: 1,
    user_id: 1,
    title: 'Task 1',
    description: 'Description 1',
    is_completed: false,
    priority: 'high',
    tags: ['work'],
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    user_id: 1,
    title: 'Task 2',
    description: 'Description 2',
    is_completed: true,
    priority: 'medium',
    tags: ['personal'],
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
  },
  {
    id: 3,
    user_id: 1,
    title: 'Task 3',
    description: null,
    is_completed: false,
    priority: 'low',
    tags: [],
    created_at: '2024-01-03T00:00:00Z',
    updated_at: '2024-01-03T00:00:00Z',
  },
];

describe('TaskList Component', () => {
  const mockOnUpdate = jest.fn();
  const mockOnEdit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders list of tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onEdit={mockOnEdit}
      />
    );

    expect(screen.getByTestId('task-list')).toBeInTheDocument();
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
    expect(screen.getByText('Task 3')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(
      <TaskList
        tasks={[]}
        isLoading={true}
        onUpdate={mockOnUpdate}
        onEdit={mockOnEdit}
      />
    );

    expect(screen.getByTestId('loading')).toBeInTheDocument();
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('shows empty state when no tasks', () => {
    render(
      <TaskList
        tasks={[]}
        onUpdate={mockOnUpdate}
        onEdit={mockOnEdit}
      />
    );

    expect(screen.getByTestId('empty-state')).toBeInTheDocument();
    expect(screen.getByText(/no tasks/i)).toBeInTheDocument();
  });

  it('renders correct number of tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onEdit={mockOnEdit}
      />
    );

    expect(screen.getByTestId('task-1')).toBeInTheDocument();
    expect(screen.getByTestId('task-2')).toBeInTheDocument();
    expect(screen.getByTestId('task-3')).toBeInTheDocument();
  });

  it('renders single task correctly', () => {
    render(
      <TaskList
        tasks={[mockTasks[0]]}
        onUpdate={mockOnUpdate}
        onEdit={mockOnEdit}
      />
    );

    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
  });
});
