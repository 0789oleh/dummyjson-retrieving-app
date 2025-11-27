import { useState, useEffect } from 'react';
import { productsApi } from '../api/api';
import type { Product } from '../../types/product';

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        setError(null);
        const data = await productsApi.getAll();
        setProducts(data);
      } catch (err) {
        setError('Failed to load products');
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, []);

  const createProduct = async (productData: any) => {
    try {
      const newProduct = await productsApi.create(productData);
      setProducts(prev => [...prev, newProduct]);
      return newProduct;
    } catch (err) {
      setError('Failed to create product');
      throw err;
    }
  };

  return { products, loading, error, createProduct };
}