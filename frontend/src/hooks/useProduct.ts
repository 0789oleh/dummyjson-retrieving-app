import { useState, useEffect, useMemo } from 'react';
import { productsApi } from '../api/api';
import type { Product, CreateProductDto, UpdateProductDto } from '../../types/product';

type SortOption = 'title' | 'price-asc' | 'price-desc';

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Состояния для UI
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState<SortOption>('title');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<UpdateProductDto>({ title: '', price: 0 });

  const PAGE_SIZE = 12;

  // Загрузка продуктов
  useEffect(() => {
    const loadProducts = async () => {
      try {
        setError(null);
        const data = await productsApi.getAll();
        setProducts(data);
      } catch (err) {
        setError('Failed to load products');
        console.error('Error loading products:', err);
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, []);

  // Сортировка и пагинация
  const { totalPages, paginatedProducts } = useMemo(() => {
    // Сортировка
    const sorted = [...products].sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'price-asc':
          return a.price - b.price;
        case 'price-desc':
          return b.price - a.price;
        default:
          return 0;
      }
    });

    // Пагинация
    const startIndex = (page - 1) * PAGE_SIZE;
    const paginated = sorted.slice(startIndex, startIndex + PAGE_SIZE);

    return {
      sortedProducts: sorted,
      paginatedProducts: paginated,
      totalPages: Math.ceil(sorted.length / PAGE_SIZE)
    };
  }, [products, sortBy, page]);

  // CRUD операции
  const createProduct = async (productData: CreateProductDto): Promise<Product> => {
    try {
      const newProduct = await productsApi.create(productData);
      setProducts(prev => [...prev, newProduct]);
      return newProduct;
    } catch (err) {
      setError('Failed to create product');
      throw err;
    }
  };

  const updateProduct = async (id: number, productData: UpdateProductDto): Promise<void> => {
    try {
      const updatedProduct = await productsApi.update(id, productData) as Product;
      setProducts(prev => prev.map(p => p.id === id ? updatedProduct : p));
      setEditingId(null);
      setEditForm({ title: '', price: 0 });
    } catch (err) {
      setError('Failed to update product');
      throw err;
    }
  };

  const deleteProduct = async (id: number): Promise<void> => {
    try {
      await productsApi.delete(id);
      setProducts(prev => prev.filter(p => p.id !== id));
      // Сброс страницы если удалили последний элемент на странице
      if (paginatedProducts.length === 1 && page > 1) {
        setPage(prev => prev - 1);
      }
    } catch (err) {
      setError('Failed to delete product');
      throw err;
    }
  };

  // Редактирование
  const startEdit = (product: Product) => {
    setEditingId(product.id);
    setEditForm({ title: product.title, price: product.price });
  };
  

  const cancelEdit = () => {
    setEditingId(null);
    setEditForm({ title: '', price: 0 });
  };

  const saveEdit = () => {
    if (editingId) {
      updateProduct(editingId, editForm);
      setEditForm({ title: '', price: 0 });
    }
  };

  return {
    // Данные
    products: paginatedProducts,
    allProducts: products,
    loading,
    error,
    
    // Пагинация и сортировка
    page,
    setPage,
    sortBy, 
    setSortBy,
    totalPages,
    
    // Редактирование
    editingId,
    editForm,
    setEditForm,
    startEdit,
    cancelEdit,
    saveEdit,
    
    // CRUD операции
    createProduct,
    updateProduct,
    deleteProduct,
  };
}