import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
}

export function Pagination({ 
  page, 
  totalPages, 
  onPageChange, 
  className = '' 
}: PaginationProps) {
  if (totalPages <= 1) return null;

  //const pages = Array.from({ length: totalPages }, (_, i) => i + 1);
  const visiblePages = getVisiblePages(page, totalPages);

  return (
    <nav className={`flex justify-center items-center space-x-2 ${className}`}>
      {/* Previous Button */}
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page === 1}
        className="p-2 rounded border disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronLeft size={16} />
      </button>

      {/* Page Numbers */}
      {visiblePages.map((pageNum) => (
        <button
          key={pageNum}
          onClick={() => onPageChange(pageNum)}
          className={`px-3 py-1 rounded border ${
            pageNum === page
              ? 'bg-blue-500 text-white'
              : 'hover:bg-gray-100'
          }`}
        >
          {pageNum}
        </button>
      ))}

      {/* Next Button */}
      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page === totalPages}
        className="p-2 rounded border disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronRight size={16} />
      </button>
    </nav>
  );
}

// Хелпер для "умной" пагинации (1 ... 4 5 6 ... 20)
function getVisiblePages(current: number, total: number): number[] {
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  if (current <= 4) {
    return [1, 2, 3, 4, 5, -1, total]; // -1 для ellipsis
  }

  if (current >= total - 3) {
    return [1, -1, total - 4, total - 3, total - 2, total - 1, total];
  }

  return [1, -1, current - 1, current, current + 1, -1, total];
}