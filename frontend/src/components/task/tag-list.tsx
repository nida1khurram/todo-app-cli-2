'use client';

interface TagListProps {
  tags: string[];
  onRemove?: (tag: string) => void;
  className?: string;
}

export function TagList({ tags, onRemove, className = '' }: TagListProps) {
  if (tags.length === 0) return null;

  return (
    <div className={`flex flex-wrap gap-1 ${className}`}>
      {tags.map((tag) => (
        <span
          key={tag}
          className="inline-flex items-center rounded-full bg-primary-50 px-2 py-0.5 text-xs font-medium text-primary-700"
        >
          {tag}
          {onRemove && (
            <button
              type="button"
              onClick={() => onRemove(tag)}
              className="ml-1 inline-flex h-4 w-4 items-center justify-center rounded-full text-primary-400 hover:bg-primary-200 hover:text-primary-600"
              aria-label={`Remove ${tag} tag`}
            >
              <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          )}
        </span>
      ))}
    </div>
  );
}
