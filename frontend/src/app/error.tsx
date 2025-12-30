'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4">
      <div className="text-center">
        <div className="mb-4 text-6xl">
          <span role="img" aria-label="Error">⚠️</span>
        </div>
        <h1 className="mb-2 text-2xl font-bold text-gray-900">
          Something went wrong!
        </h1>
        <p className="mb-6 text-gray-600">
          We apologize for the inconvenience. Please try again.
        </p>
        {error.message && (
          <p className="mb-6 rounded-md bg-red-50 p-3 text-sm text-red-700">
            Error: {error.message}
          </p>
        )}
        <div className="flex justify-center gap-4">
          <Button onClick={reset}>Try again</Button>
          <Button variant="outline" onClick={() => (window.location.href = '/')}>
            Go to Home
          </Button>
        </div>
      </div>
    </div>
  );
}
