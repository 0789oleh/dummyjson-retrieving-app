import type { Product } from '../../types/product';
import { formatPrice } from '../utils/format';

interface ProductCardProps {
  product: Product;
  onEdit?: (product: Product) => void;
  onDelete?: (productId: number) => void;
  onAddToCart?: (product: Product) => void;
  className?: string;
}

export function ProductCard({ product, onAddToCart, onEdit, onDelete, className }: ProductCardProps) {
  return (
    <div className={`product-card p-4 border rounded-lg ${className}`}>
      <h3 className="font-semibold text-lg mb-1">{product.title}</h3>
      <p className="text-gray-600 mb-2">{product.description}</p>
      <div className="font-bold mb-2">{formatPrice(product.price)}</div>
      <div className="flex gap-2">
        <button
          className="px-3 py-1 bg-indigo-600 text-white rounded"
          onClick={() => onAddToCart?.(product)}
        >
          Add to Cart
        </button>
        <button
          className="px-3 py-1 bg-yellow-500 text-white rounded"
          onClick={() => onEdit?.(product)}
        >
          Edit
        </button>
        <button
          className="px-3 py-1 bg-red-600 text-white rounded"
          onClick={() => onDelete?.(product.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
