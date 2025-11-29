import type { Product } from '../../types/product';
import { useCart } from '../hooks/useCart';
import { useProducts } from '../hooks/useProduct';
import { formatPrice } from '../utils/format';

interface ProductCardProps {
  product: Product;
  onEdit?: (product: Product) => void;
  onDelete?: (productId: number) => void;
  onAddToCart?: (product: Product) => void;
  className?: string;
}

export function ProductCard({ product, onAddToCart, onEdit, className }: ProductCardProps) {
  const { addItem } = useCart();
  const { updateProduct } = useProducts();
  
  const handleAddToCart = () => {
    addItem(product.id, 1);
    onAddToCart?.(product);
  };

  const handleEdit = () => {
    // Handle edit logic here
    updateProduct(product.id, { title: product.title, price: product.price });
    onEdit?.(product);
  }

  return (
    <div className={`product-card ${className}`}>
      <h3>{product.title}</h3>
      <p>{product.description}</p>
      <div className="price">{formatPrice(product.price)}</div>
      <button onClick={handleAddToCart}>Add to Cart</button>
      <button onClick={handleEdit}>Edit</button>
    </div>
  );
}