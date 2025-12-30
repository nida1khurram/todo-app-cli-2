'use client';

import { useState, KeyboardEvent } from 'react';
import { Task } from '@/types/task';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PriorityBadge } from '@/components/task/priority-badge';
import { tasksApi } from '@/lib/api-client';
import { useToast } from '@/components/ui/toast';

interface TaskCardProps {
  task: Task;
  onUpdate: () => void;
  onEdit: (task: Task) => void;
}

export function TaskCard({ task, onUpdate, onEdit }: TaskCardProps) {
  const { addToast } = useToast();
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggleComplete = async () => {
    setIsToggling(true);
    try {
      await tasksApi.toggleComplete(task.id);
      addToast(
        task.is_completed ? 'Task marked as incomplete' : 'Task completed!',
        'success'
      );
      onUpdate();
    } catch {
      addToast('Failed to update task', 'error');
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setIsDeleting(true);
    try {
      await tasksApi.delete(task.id);
      addToast('Task deleted', 'success');
      onUpdate();
    } catch {
      addToast('Failed to delete task', 'error');
    } finally {
      setIsDeleting(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    // Only handle if focus is on the card itself (not on interactive elements)
    if (e.target !== e.currentTarget) return;

    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        onEdit(task);
        break;
      case 'Delete':
      case 'Backspace':
        e.preventDefault();
        handleDelete();
        break;
    }
  };

  return (
    <Card
      variant="bordered"
      className={`transition-opacity focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 ${
        task.is_completed ? 'opacity-60' : ''
      }`}
      tabIndex={0}
      onKeyDown={handleKeyDown}
      role="article"
      aria-label={`Task: ${task.title}. Press Enter to edit, Delete to remove.`}
    >
      <div className="flex items-start gap-4">
        <button
          type="button"
          onClick={handleToggleComplete}
          disabled={isToggling}
          className="mt-1 h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500 disabled:cursor-wait cursor-pointer flex items-center justify-center"
          aria-label={`Mark "${task.title}" as ${task.is_completed ? 'incomplete' : 'complete'}`}
        >
          {task.is_completed && (
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3
              className={`font-medium truncate ${
                task.is_completed ? 'text-gray-500 line-through' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            <PriorityBadge priority={task.priority} />
          </div>

          {task.description && (
            <p className="mt-1 text-sm text-gray-500 line-clamp-2">
              {task.description}
            </p>
          )}

          {task.tags && task.tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {task.tags.map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          <p className="mt-2 text-xs text-gray-400">
            Created: {new Date(task.created_at).toLocaleDateString()}
            {task.updated_at !== task.created_at && (
              <> · Updated: {new Date(task.updated_at).toLocaleDateString()}</>
            )}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onEdit(task)}
            className="text-gray-600 hover:text-gray-900"
            aria-label={`Edit "${task.title}"`}
          >
            Edit
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleDelete}
            isLoading={isDeleting}
            className="text-red-600 hover:bg-red-50 hover:text-red-700"
            aria-label={`Delete "${task.title}"`}
          >
            Delete
          </Button>
        </div>
      </div>
    </Card>
  );
}
