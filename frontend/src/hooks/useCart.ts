import { useState, useEffect, useCallback } from 'react';
import { cartsApi } from '../api/api';
import type { Cart } from '../../types/cart';

export function useCart(userId?: number) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Cart loading
  useEffect(() => {
    if (!userId) {
      setLoading(false);
      return;
    }

    const loadCart = async () => {
      try {
        setError(null);
        const cartData = await cartsApi.getByUser(userId);
        setCart(cartData);
      } catch (err) {
        setError('Failed to load cart');
        console.error('Error loading cart:', err);
      } finally {
        setLoading(false);
      }
    };

    loadCart();
  }, [userId]);

  // Adding item to cart
  const addItem = useCallback(async (productId: number, quantity: number = 1) => {
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      setError(null);
      await cartsApi.addItem(userId, { productId, quantity });
      
      // Update local state
      const updatedCart = await cartsApi.getByUser(userId);
      setCart(updatedCart);
    } catch (err) {
      setError('Failed to add item to cart');
      console.error('Error adding item:', err);
      throw err;
    }
  }, [userId]);

  // Removing item from cart
  const removeItem = useCallback(async (itemId: number) => {
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      setError(null);
      await cartsApi.removeItem(userId, itemId);
      
      // Update local state
      const updatedCart = await cartsApi.getByUser(userId);
      setCart(updatedCart);
    } catch (err) {
      setError('Failed to remove item from cart');
      console.error('Error removing item:', err);
      throw err;
    }
  }, [userId]);

  // Updating item quantity
  const updateQuantity = useCallback(async (itemId: number, quantity: number) => {
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    if (quantity <= 0) {
      return removeItem(itemId);
    }

    try {
      setError(null);
      await cartsApi.updateItem(userId, itemId, { quantity });
      
      const updatedCart = await cartsApi.getByUser(userId);
      setCart(updatedCart);
    } catch (err) {
      setError('Failed to update item quantity');
      console.error('Error updating quantity:', err);
      throw err;
    }
  }, [userId, removeItem]);

  // Clearing the cart
  const clearCart = useCallback(async () => {
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    try {
      setError(null);
      await cartsApi.clearCart(userId);
      setCart(null);
    } catch (err) {
      setError('Failed to clear cart');
      console.error('Error clearing cart:', err);
      throw err;
    }
  }, [userId]);

  // Helper getters
  const totalItems = cart?.items.reduce((sum, item) => sum + item.quantity, 0) || 0;
  const totalPrice = cart?.items.reduce((sum, item) => sum + (item.product.price * item.quantity), 0) || 0;

  const getItemQuantity = useCallback((productId: number): number => {
    const item = cart?.items.find(item => item.product.id === productId);
    return item?.quantity || 0;
  }, [cart]);

  const isInCart = useCallback((productId: number): boolean => {
    return cart?.items.some(item => item.product.id === productId) || false;
  }, [cart]);

  return {
    // State
    cart,
    loading,
    error,
    
    // Methods
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    
    // Getters
    totalItems,
    totalPrice,
    getItemQuantity,
    isInCart,
    
    // Validation
    hasItems: totalItems > 0,
  };
}