'use client';

import { useState, useEffect, useRef } from 'react';
import { tagsApi } from '@/lib/api-client';

interface TagInputProps {
  selectedTags: string[];
  onTagsChange: (tags: string[]) => void;
  placeholder?: string;
}

export function TagInput({
  selectedTags,
  onTagsChange,
  placeholder = 'Add tags...',
}: TagInputProps) {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    if (inputValue.trim().length < 1) {
      setSuggestions([]);
      return;
    }

    // Debounce API calls
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(async () => {
      setIsLoading(true);
      try {
        const tags = await tagsApi.getAll(inputValue);
        const tagNames = tags
          .map((t: { name: string }) => t.name)
          .filter((name: string) => !selectedTags.includes(name));
        setSuggestions(tagNames);
      } catch (error) {
        console.error('Failed to fetch tags:', error);
        setSuggestions([]);
      } finally {
        setIsLoading(false);
      }
    }, 300);

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [inputValue, selectedTags]);

  const addTag = (tag: string) => {
    const normalizedTag = tag.trim().toLowerCase();
    if (normalizedTag && !selectedTags.includes(normalizedTag)) {
      onTagsChange([...selectedTags, normalizedTag]);
    }
    setInputValue('');
    setSuggestions([]);
    setShowSuggestions(false);
  };

  const removeTag = (tagToRemove: string) => {
    onTagsChange(selectedTags.filter((tag) => tag !== tagToRemove));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      addTag(inputValue);
    } else if (e.key === 'Backspace' && !inputValue && selectedTags.length > 0) {
      removeTag(selectedTags[selectedTags.length - 1]!);
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  return (
    <div className="relative">
      <div className="flex flex-wrap items-center gap-1 rounded-md border border-gray-300 bg-white px-2 py-1.5 focus-within:border-primary-500 focus-within:ring-2 focus-within:ring-primary-500">
        {selectedTags.map((tag) => (
          <span
            key={tag}
            className="inline-flex items-center rounded-full bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-700"
          >
            {tag}
            <button
              type="button"
              onClick={() => removeTag(tag)}
              className="ml-1 inline-flex h-3 w-3 items-center justify-center rounded-full text-primary-400 hover:bg-primary-200 hover:text-primary-600"
            >
              <svg className="h-2 w-2" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </span>
        ))}
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setShowSuggestions(true);
          }}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          onKeyDown={handleKeyDown}
          placeholder={selectedTags.length === 0 ? placeholder : ''}
          className="flex-1 border-none bg-transparent p-1 text-sm outline-none placeholder:text-gray-400"
        />
      </div>

      {/* Suggestions dropdown */}
      {showSuggestions && (suggestions.length > 0 || inputValue.trim()) && (
        <div className="absolute z-10 mt-1 w-full rounded-md border border-gray-200 bg-white py-1 shadow-lg">
          {isLoading ? (
            <div className="px-3 py-2 text-sm text-gray-500">Loading...</div>
          ) : (
            <>
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => addTag(suggestion)}
                  className="block w-full px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-100"
                >
                  {suggestion}
                </button>
              ))}
              {inputValue.trim() && !suggestions.includes(inputValue.trim().toLowerCase()) && (
                <button
                  type="button"
                  onClick={() => addTag(inputValue)}
                  className="block w-full px-3 py-2 text-left text-sm text-primary-600 hover:bg-gray-100"
                >
                  Create &quot;{inputValue.trim()}&quot;
                </button>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
