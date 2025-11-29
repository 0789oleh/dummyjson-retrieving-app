// components/Cart/CartSummary.tsx
import { useCart } from '../hooks/useCart';
import { CartItem } from './CartItem';

export function CartSummary() {
  const { cart, totalItems, totalPrice, clearCart, loading } = useCart(1);
  
  if (loading) return <div>Loading cart...</div>;
  if (!cart) return <div>Cart is empty</div>;
  
  return (
    <div className="cart-summary">
      <h2>Cart ({totalItems} items)</h2>
      <p>Total: ${totalPrice}</p>
      <button onClick={clearCart}>Clear Cart</button>
      
      {cart.items.map(item => (
        <CartItem key={item.id} item={item} />
      ))}
    </div>
  );
}