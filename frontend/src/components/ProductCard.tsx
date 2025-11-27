// components/ProductCard/ProductCard.tsx
import type { Product } from '../../types/product';
import { useCart } from '../hooks/useCart';
import { formatPrice } from '../utils/format';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  className?: string;
}

export function ProductCard({ product, onAddToCart, className }: ProductCardProps) {
  const { addItem } = useCart();
  
  const handleAddToCart = () => {
    addItem(product.id, 1);
    onAddToCart?.(product);
  };

  return (
    <div className={`product-card ${className}`}>
      <h3>{product.title}</h3>
      <p>{product.description}</p>
      <div className="price">{formatPrice(product.price)}</div>
      <button onClick={handleAddToCart}>Add to Cart</button>
    </div>
  );
}