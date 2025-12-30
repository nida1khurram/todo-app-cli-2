'use client';

import { useState, useEffect, useCallback } from 'react';
import { tagsApi } from '@/lib/api-client';

interface TagFilterProps {
  selectedTags: string[];
  onTagsChange: (tags: string[]) => void;
}

export function TagFilter({ selectedTags, onTagsChange }: TagFilterProps) {
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchTags = useCallback(async () => {
    setIsLoading(true);
    try {
      const tags = await tagsApi.getAll(searchQuery);
      const tagNames = tags.map((t: { name: string }) => t.name);
      setAvailableTags(tagNames);
    } catch (error) {
      console.error('Failed to fetch tags:', error);
    } finally {
      setIsLoading(false);
    }
  }, [searchQuery]);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchTags();
    }, 300);

    return () => clearTimeout(timer);
  }, [fetchTags]);

  const toggleTag = (tag: string) => {
    if (selectedTags.includes(tag)) {
      onTagsChange(selectedTags.filter((t) => t !== tag));
    } else {
      onTagsChange([...selectedTags, tag]);
    }
  };

  const filteredTags = availableTags.filter(
    (tag) => !selectedTags.includes(tag) && tag.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="relative" data-testid="tag-filter">
      <label className="mb-1 block text-sm font-medium text-gray-700">
        Tags
      </label>

      {/* Selected tags */}
      {selectedTags.length > 0 && (
        <div className="mb-2 flex flex-wrap gap-1">
          {selectedTags.map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() => toggleTag(tag)}
              className="inline-flex items-center rounded-full bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-700 hover:bg-primary-200"
              aria-label={`Remove tag: ${tag}`}
            >
              {tag}
              <svg className="ml-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          ))}
        </div>
      )}

      {/* Search input */}
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search tags..."
        className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
        aria-label="Search tags"
      />

      {/* Tag options dropdown */}
      {(searchQuery || filteredTags.length > 0) && (
        <div className="absolute z-10 mt-1 max-h-40 w-full overflow-auto rounded-md border border-gray-200 bg-white py-1 shadow-lg">
          {isLoading ? (
            <div className="px-3 py-2 text-sm text-gray-500">Loading...</div>
          ) : filteredTags.length > 0 ? (
            filteredTags.map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => {
                  toggleTag(tag);
                  setSearchQuery('');
                }}
                className="block w-full px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
                role="option"
                aria-selected={selectedTags.includes(tag)}
              >
                {tag}
              </button>
            ))
          ) : (
            <div className="px-3 py-2 text-sm text-gray-500">
              No tags found
            </div>
          )}
        </div>
      )}

      {/* Clear all button */}
      {selectedTags.length > 0 && (
        <button
          type="button"
          onClick={() => onTagsChange([])}
          className="mt-1 text-xs text-gray-500 hover:text-gray-700"
        >
          Clear all tags
        </button>
      )}
    </div>
  );
}
