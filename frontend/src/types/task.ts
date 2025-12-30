/**
 * Task type definitions
 */

export type Priority = 'high' | 'medium' | 'low';

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  priority: Priority;
  created_at: string;
  updated_at: string;
  tags: string[];
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: Priority;
  tags?: string[];
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: Priority;
  is_completed?: boolean;
  tags?: string[];
}

export interface TaskFilters {
  status?: 'all' | 'completed' | 'pending';
  priority?: Priority;
  tags?: string[];
  search?: string;
  sort_by?: 'created_at' | 'priority' | 'title';
  sort_order?: 'asc' | 'desc';
}
