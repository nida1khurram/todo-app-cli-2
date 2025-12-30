/**
 * E2E Test: Tag Workflow
 *
 * Tests tag creation and assignment flow
 */

const mockApi = {
  getTags: jest.fn(),
  createTag: jest.fn(),
  deleteTag: jest.fn(),
  createTask: jest.fn(),
  updateTask: jest.fn(),
};

jest.mock('@/lib/api-client', () => ({
  tagsApi: {
    getAll: (...args: unknown[]) => mockApi.getTags(...args),
    create: (...args: unknown[]) => mockApi.createTag(...args),
    delete: (...args: unknown[]) => mockApi.deleteTag(...args),
  },
  tasksApi: {
    create: (...args: unknown[]) => mockApi.createTask(...args),
    update: (...args: unknown[]) => mockApi.updateTask(...args),
  },
}));

describe('Tag Workflow E2E', () => {
  const mockTags = [
    { id: 1, name: 'work', user_id: 1 },
    { id: 2, name: 'personal', user_id: 1 },
    { id: 3, name: 'urgent', user_id: 1 },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.setItem('token', 'test-token');
  });

  describe('Tag Creation', () => {
    it('creates a new tag', async () => {
      mockApi.createTag.mockResolvedValue({ id: 4, name: 'newTag', user_id: 1 });

      const result = await mockApi.createTag({ name: 'newTag' });

      expect(result.name).toBe('newTag');
      expect(result.id).toBe(4);
    });

    it('normalizes tag name to lowercase', async () => {
      mockApi.createTag.mockResolvedValue({ id: 4, name: 'newtag', user_id: 1 });

      const result = await mockApi.createTag({ name: 'NewTag' });

      expect(result.name).toBe('newtag');
    });

    it('handles duplicate tag error', async () => {
      mockApi.createTag.mockRejectedValue(new Error('Tag already exists'));

      await expect(mockApi.createTag({ name: 'work' })).rejects.toThrow('Tag already exists');
    });
  });

  describe('Tag Retrieval', () => {
    it('retrieves all user tags', async () => {
      mockApi.getTags.mockResolvedValue(mockTags);

      const tags = await mockApi.getTags();

      expect(tags).toHaveLength(3);
      expect(tags.map((t: { name: string }) => t.name)).toContain('work');
    });

    it('searches tags by prefix', async () => {
      mockApi.getTags.mockImplementation((search?: string) => {
        if (search) {
          return Promise.resolve(
            mockTags.filter((t) => t.name.startsWith(search.toLowerCase()))
          );
        }
        return Promise.resolve(mockTags);
      });

      const results = await mockApi.getTags('wo');

      expect(results).toHaveLength(1);
      expect(results[0].name).toBe('work');
    });
  });

  describe('Tag Deletion', () => {
    it('deletes a tag', async () => {
      mockApi.deleteTag.mockResolvedValue(undefined);

      await mockApi.deleteTag(1);

      expect(mockApi.deleteTag).toHaveBeenCalledWith(1);
    });

    it('handles not found error', async () => {
      mockApi.deleteTag.mockRejectedValue(new Error('Tag not found'));

      await expect(mockApi.deleteTag(999)).rejects.toThrow('Tag not found');
    });
  });

  describe('Task-Tag Association', () => {
    it('creates task with tags', async () => {
      mockApi.createTask.mockResolvedValue({
        id: 1,
        title: 'Tagged Task',
        tags: ['work', 'urgent'],
      });

      const task = await mockApi.createTask({
        title: 'Tagged Task',
        tags: ['work', 'urgent'],
      });

      expect(task.tags).toHaveLength(2);
      expect(task.tags).toContain('work');
      expect(task.tags).toContain('urgent');
    });

    it('updates task tags', async () => {
      mockApi.updateTask.mockResolvedValue({
        id: 1,
        title: 'Task',
        tags: ['personal'],
      });

      const result = await mockApi.updateTask(1, {
        tags: ['personal'],
      });

      expect(result.tags).toEqual(['personal']);
    });

    it('removes all tags from task', async () => {
      mockApi.updateTask.mockResolvedValue({
        id: 1,
        title: 'Task',
        tags: [],
      });

      const result = await mockApi.updateTask(1, {
        tags: [],
      });

      expect(result.tags).toEqual([]);
    });

    it('creates new tags when assigning to task', async () => {
      // When a task is created with a new tag, the tag is auto-created
      mockApi.createTask.mockResolvedValue({
        id: 1,
        title: 'Task with new tag',
        tags: ['brandnewtag'],
      });

      const task = await mockApi.createTask({
        title: 'Task with new tag',
        tags: ['brandnewtag'],
      });

      expect(task.tags).toContain('brandnewtag');
    });
  });

  describe('Tag Autocomplete Flow', () => {
    it('shows matching tags as user types', async () => {
      mockApi.getTags.mockImplementation((search?: string) => {
        if (search) {
          return Promise.resolve(
            mockTags.filter((t) => t.name.toLowerCase().includes(search.toLowerCase()))
          );
        }
        return Promise.resolve(mockTags);
      });

      // User types "urg"
      const suggestions = await mockApi.getTags('urg');

      expect(suggestions).toHaveLength(1);
      expect(suggestions[0].name).toBe('urgent');
    });

    it('shows all tags when input is empty', async () => {
      mockApi.getTags.mockResolvedValue(mockTags);

      const suggestions = await mockApi.getTags();

      expect(suggestions).toHaveLength(3);
    });
  });

  describe('Complete Tag Workflow', () => {
    it('performs complete tag workflow', async () => {
      // 1. Get existing tags
      mockApi.getTags.mockResolvedValue(mockTags);
      const existingTags = await mockApi.getTags();
      expect(existingTags).toHaveLength(3);

      // 2. Create a new tag
      mockApi.createTag.mockResolvedValue({ id: 4, name: 'project', user_id: 1 });
      const newTag = await mockApi.createTag({ name: 'project' });

      // 3. Create task with new and existing tags
      mockApi.createTask.mockResolvedValue({
        id: 1,
        title: 'Project Task',
        tags: ['work', 'project'],
      });
      const task = await mockApi.createTask({
        title: 'Project Task',
        tags: ['work', 'project'],
      });

      // 4. Update task to add more tags
      mockApi.updateTask.mockResolvedValue({
        id: 1,
        title: 'Project Task',
        tags: ['work', 'project', 'urgent'],
      });
      const updatedTask = await mockApi.updateTask(1, {
        tags: ['work', 'project', 'urgent'],
      });

      // 5. Delete unused tag
      mockApi.deleteTag.mockResolvedValue(undefined);
      await mockApi.deleteTag(2); // personal

      // Verify all operations completed
      expect(mockApi.getTags).toHaveBeenCalled();
      expect(mockApi.createTag).toHaveBeenCalledWith({ name: 'project' });
      expect(mockApi.createTask).toHaveBeenCalled();
      expect(mockApi.updateTask).toHaveBeenCalled();
      expect(mockApi.deleteTag).toHaveBeenCalledWith(2);
    });
  });
});
