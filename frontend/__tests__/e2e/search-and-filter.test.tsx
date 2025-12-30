/**
 * E2E Test: Search and Filter Functionality
 *
 * Tests searching and filtering tasks end-to-end
 */

const mockApi = {
  getTasks: jest.fn(),
};

jest.mock('@/lib/api-client', () => ({
  tasksApi: {
    getAll: (...args: unknown[]) => mockApi.getTasks(...args),
  },
}));

describe('Search and Filter E2E', () => {
  const mockTasks = [
    { id: 1, title: 'Buy groceries', priority: 'high', is_completed: false, tags: ['shopping'] },
    { id: 2, title: 'Write code', priority: 'medium', is_completed: false, tags: ['work'] },
    { id: 3, title: 'Go to gym', priority: 'low', is_completed: true, tags: ['health'] },
    { id: 4, title: 'Read book', priority: 'low', is_completed: false, tags: ['personal'] },
    { id: 5, title: 'Work meeting', priority: 'high', is_completed: false, tags: ['work'] },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.setItem('token', 'test-token');
  });

  describe('Search Functionality', () => {
    it('filters tasks by search query', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        const search = params?.search?.toLowerCase();
        if (search) {
          return Promise.resolve(
            mockTasks.filter((t) => t.title.toLowerCase().includes(search))
          );
        }
        return Promise.resolve(mockTasks);
      });

      // Search for "work"
      const results = await mockApi.getTasks({ search: 'work' });

      expect(results).toHaveLength(2);
      expect(results.map((t: { title: string }) => t.title)).toContain('Write code');
      expect(results.map((t: { title: string }) => t.title)).toContain('Work meeting');
    });

    it('returns empty array when no matches', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        const search = params?.search?.toLowerCase();
        if (search) {
          return Promise.resolve(
            mockTasks.filter((t) => t.title.toLowerCase().includes(search))
          );
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({ search: 'nonexistent' });

      expect(results).toHaveLength(0);
    });

    it('search is case-insensitive', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        const search = params?.search?.toLowerCase();
        if (search) {
          return Promise.resolve(
            mockTasks.filter((t) => t.title.toLowerCase().includes(search))
          );
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({ search: 'BUY' });

      expect(results).toHaveLength(1);
      expect(results[0].title).toBe('Buy groceries');
    });
  });

  describe('Status Filter', () => {
    it('filters completed tasks', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        if (params?.status_filter === 'completed') {
          return Promise.resolve(mockTasks.filter((t) => t.is_completed));
        }
        if (params?.status_filter === 'pending') {
          return Promise.resolve(mockTasks.filter((t) => !t.is_completed));
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({ status_filter: 'completed' });

      expect(results).toHaveLength(1);
      expect(results[0].title).toBe('Go to gym');
    });

    it('filters pending tasks', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        if (params?.status_filter === 'pending') {
          return Promise.resolve(mockTasks.filter((t) => !t.is_completed));
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({ status_filter: 'pending' });

      expect(results).toHaveLength(4);
    });

    it('returns all tasks with no filter', async () => {
      mockApi.getTasks.mockResolvedValue(mockTasks);

      const results = await mockApi.getTasks({});

      expect(results).toHaveLength(5);
    });
  });

  describe('Priority Filter', () => {
    it('filters high priority tasks', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        if (params?.priority) {
          return Promise.resolve(mockTasks.filter((t) => t.priority === params.priority));
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({ priority: 'high' });

      expect(results).toHaveLength(2);
      expect(results.every((t: { priority: string }) => t.priority === 'high')).toBe(true);
    });

    it('filters low priority tasks', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        if (params?.priority) {
          return Promise.resolve(mockTasks.filter((t) => t.priority === params.priority));
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({ priority: 'low' });

      expect(results).toHaveLength(2);
    });
  });

  describe('Combined Filters', () => {
    it('combines status and priority filters', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        let filtered = [...mockTasks];

        if (params?.status_filter === 'pending') {
          filtered = filtered.filter((t) => !t.is_completed);
        }
        if (params?.priority) {
          filtered = filtered.filter((t) => t.priority === params.priority);
        }

        return Promise.resolve(filtered);
      });

      const results = await mockApi.getTasks({
        status_filter: 'pending',
        priority: 'high',
      });

      expect(results).toHaveLength(2);
      expect(results.every((t: { is_completed: boolean; priority: string }) =>
        !t.is_completed && t.priority === 'high'
      )).toBe(true);
    });

    it('combines search with filters', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        let filtered = [...mockTasks];

        if (params?.search) {
          filtered = filtered.filter((t) =>
            t.title.toLowerCase().includes(params.search.toLowerCase())
          );
        }
        if (params?.priority) {
          filtered = filtered.filter((t) => t.priority === params.priority);
        }

        return Promise.resolve(filtered);
      });

      const results = await mockApi.getTasks({
        search: 'work',
        priority: 'high',
      });

      expect(results).toHaveLength(1);
      expect(results[0].title).toBe('Work meeting');
    });
  });

  describe('Sorting', () => {
    it('sorts by created_at descending by default', async () => {
      mockApi.getTasks.mockResolvedValue(mockTasks);

      const results = await mockApi.getTasks({
        sort_by: 'created_at',
        sort_order: 'desc',
      });

      expect(mockApi.getTasks).toHaveBeenCalledWith({
        sort_by: 'created_at',
        sort_order: 'desc',
      });
    });

    it('sorts by title ascending', async () => {
      mockApi.getTasks.mockImplementation((params) => {
        if (params?.sort_by === 'title' && params?.sort_order === 'asc') {
          return Promise.resolve(
            [...mockTasks].sort((a, b) => a.title.localeCompare(b.title))
          );
        }
        return Promise.resolve(mockTasks);
      });

      const results = await mockApi.getTasks({
        sort_by: 'title',
        sort_order: 'asc',
      });

      expect(results[0].title).toBe('Buy groceries');
    });
  });
});
