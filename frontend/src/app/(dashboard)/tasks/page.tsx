'use client';

import { useEffect, useState, useCallback } from 'react';
import { Task, TaskCreate, TaskFilters, Priority } from '@/types/task';
import { tasksApi } from '@/lib/api-client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { TaskCard } from '@/components/task/task-card';
import { EditTaskModal } from '@/components/task/edit-task-modal';
import { SearchBar } from '@/components/task/search-bar';
import { TagInput } from '@/components/task/tag-input';
import { useToast } from '@/components/ui/toast';

export default function TasksPage() {
  const { addToast } = useToast();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Form state
  const [showForm, setShowForm] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newPriority, setNewPriority] = useState<Priority>('medium');
  const [newTags, setNewTags] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Filter state
  const [filters, setFilters] = useState<TaskFilters>({
    status: 'all',
    sort_by: 'created_at',
    sort_order: 'desc',
  });
  const [searchQuery, setSearchQuery] = useState('');

  const fetchTasks = useCallback(async () => {
    try {
      const params: Record<string, string> = {};
      if (filters.status && filters.status !== 'all') {
        params['status_filter'] = filters.status;
      }
      if (filters.priority) {
        params['priority'] = filters.priority;
      }
      if (searchQuery) {
        params['search'] = searchQuery;
      }
      if (filters.sort_by) {
        params['sort_by'] = filters.sort_by;
      }
      if (filters.sort_order) {
        params['sort_order'] = filters.sort_order;
      }

      const data = await tasksApi.getAll(params);
      setTasks(data);
    } catch {
      setError('Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  }, [filters, searchQuery]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) {
      addToast('Please enter a task title', 'error');
      return;
    }

    setIsSubmitting(true);
    try {
      const taskData: TaskCreate = {
        title: newTitle.trim(),
        description: newDescription.trim() || undefined,
        priority: newPriority,
        tags: newTags,
      };
      await tasksApi.create(taskData);
      setNewTitle('');
      setNewDescription('');
      setNewPriority('medium');
      setNewTags([]);
      setShowForm(false);
      addToast('Task created successfully!', 'success');
      fetchTasks();
    } catch {
      addToast('Failed to create task', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const clearFilters = () => {
    setFilters({
      status: 'all',
      sort_by: 'created_at',
      sort_order: 'desc',
    });
    setSearchQuery('');
  };

  const hasActiveFilters =
    filters.status !== 'all' ||
    filters.priority ||
    searchQuery ||
    filters.sort_by !== 'created_at' ||
    filters.sort_order !== 'desc';

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">My Tasks</h2>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add Task'}
        </Button>
      </div>

      {/* Error message */}
      {error && (
        <div className="rounded-md bg-red-50 p-3 text-sm text-red-700">
          {error}
          <button
            onClick={() => setError('')}
            className="ml-2 underline hover:no-underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Task Creation Form */}
      {showForm && (
        <form
          onSubmit={handleCreateTask}
          className="rounded-lg border bg-white p-4 shadow-sm"
        >
          <h3 className="mb-4 font-medium text-gray-900">Create New Task</h3>
          <div className="space-y-4">
            <Input
              label="Title"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="What needs to be done?"
              required
            />

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Description (optional)
              </label>
              <textarea
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder="Add more details..."
                rows={3}
                className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm placeholder:text-gray-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Priority
                </label>
                <select
                  value={newPriority}
                  onChange={(e) => setNewPriority(e.target.value as Priority)}
                  className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Tags
                </label>
                <TagInput selectedTags={newTags} onTagsChange={setNewTags} />
              </div>
            </div>

            <Button type="submit" isLoading={isSubmitting}>
              Create Task
            </Button>
          </div>
        </form>
      )}

      {/* Search and Filters */}
      <div className="space-y-4 rounded-lg border bg-white p-4">
        <div className="flex flex-wrap items-end gap-4">
          {/* Search */}
          <div className="w-full sm:w-64">
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Search
            </label>
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              placeholder="Search tasks..."
            />
          </div>

          {/* Status Filter */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  status: e.target.value as 'all' | 'completed' | 'pending',
                })
              }
              className="rounded-md border border-gray-300 px-3 py-2 text-sm"
            >
              <option value="all">All Tasks</option>
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          {/* Priority Filter */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Priority
            </label>
            <select
              value={filters.priority || ''}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  priority: e.target.value as Priority | undefined || undefined,
                })
              }
              className="rounded-md border border-gray-300 px-3 py-2 text-sm"
            >
              <option value="">Any Priority</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          {/* Sort By */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Sort By
            </label>
            <select
              value={filters.sort_by}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  sort_by: e.target.value as 'created_at' | 'priority' | 'title',
                })
              }
              className="rounded-md border border-gray-300 px-3 py-2 text-sm"
            >
              <option value="created_at">Date Created</option>
              <option value="priority">Priority</option>
              <option value="title">Title</option>
            </select>
          </div>

          {/* Sort Order */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Order
            </label>
            <select
              value={filters.sort_order}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  sort_order: e.target.value as 'asc' | 'desc',
                })
              }
              className="rounded-md border border-gray-300 px-3 py-2 text-sm"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>

          {/* Clear Filters */}
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearFilters}>
              Clear Filters
            </Button>
          )}
        </div>

        {/* Active filters indicator */}
        {hasActiveFilters && (
          <p className="text-sm text-gray-500">
            Showing {tasks.length} task{tasks.length !== 1 ? 's' : ''}
            {searchQuery && ` matching "${searchQuery}"`}
          </p>
        )}
      </div>

      {/* Task List */}
      {tasks.length === 0 ? (
        <div className="rounded-lg border border-dashed border-gray-300 p-12 text-center">
          <p className="text-gray-500">
            {hasActiveFilters
              ? 'No tasks match your filters.'
              : 'No tasks yet. Create your first task!'}
          </p>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearFilters} className="mt-2">
              Clear Filters
            </Button>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onUpdate={fetchTasks}
              onEdit={setEditingTask}
            />
          ))}
        </div>
      )}

      {/* Edit Task Modal */}
      <EditTaskModal
        task={editingTask}
        isOpen={editingTask !== null}
        onClose={() => setEditingTask(null)}
        onUpdate={fetchTasks}
      />
    </div>
  );
}
