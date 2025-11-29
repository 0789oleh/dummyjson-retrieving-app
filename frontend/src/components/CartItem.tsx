import { useCart } from '../hooks/useCart';
import { formatPrice } from '../utils/format';
import type { CartItem } from '../../types/cart';

interface CartItemProps {
  item: CartItem;
  compact?: boolean;
  editable?: boolean;
}

export function CartItem({ item, compact = false, editable = true }: CartItemProps) {
  const { updateQuantity, removeItem } = useCart(1);

  const handleQuantityChange = (newQuantity: number) => {
    if (newQuantity === 0) {
      removeItem(item.id);
    } else {
      updateQuantity(item.id, newQuantity);
    }
  };

  if (compact) {
    return (
      <div className="flex justify-between items-center py-2">
        <div className="flex-1">
          <h4 className="font-medium truncate">{item.product.title}</h4>
          <p className="text-sm text-gray-600">
            {item.quantity} × {formatPrice(item.product.price)}
          </p>
        </div>
        <span className="font-semibold">
          {formatPrice(item.product.price * item.quantity)}
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-4 py-4 border-b">

      {/* Product Info */}
      <div className="flex-1">
        <h3 className="font-semibold">{item.product.title}</h3>
        <p className="text-gray-600">{formatPrice(item.product.price)}</p>
      </div>

      {/* Quantity Controls */}
      {editable && (
        <div className="flex items-center space-x-2">
          <button
            onClick={() => handleQuantityChange(item.quantity - 1)}
            className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-gray-100"
          >
            -
          </button>
          <span className="w-8 text-center">{item.quantity}</span>
          <button
            onClick={() => handleQuantityChange(item.quantity + 1)}
            className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-gray-100"
          >
            +
          </button>
        </div>
      )}

      {/* Total Price */}
      <div className="text-right">
        <p className="font-semibold">
          {formatPrice(item.product.price * item.quantity)}
        </p>
        {editable && (
          <button
            onClick={() => removeItem(item.id)}
            className="text-red-500 text-sm hover:text-red-700 mt-1"
          >
            Remove
          </button>
        )}
      </div>
    </div>
  );
}