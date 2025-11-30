import axios from 'axios';
import type { Product } from '../../types/product';
import type { Cart } from '../../types/cart';
import type { User, UserWithCart } from '../../types/user';
import type { DashboardStats } from '../../types/dashboard';

const api = axios.create({ baseURL: import.meta.env.VITE_BASE_URL });

const handleRequest = async <T>(promise: Promise<any>): Promise<T> => {
  try {
    const response = await promise;
    return response.data;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

export const productsApi = {
  getAll: () => handleRequest<Product[]>(api.get('/products')),
  create: (data: any) => handleRequest<Product>(api.post('/products', data)),
  update: (id: number, data: any) => handleRequest(api.put(`/products/${id}`, data)),
  delete: (id: number) => handleRequest(api.delete(`/products/${id}`)),
};

export const usersApi = {
  getAll: () => handleRequest<User[]>(api.get('/users')),
  create: (data: any) => handleRequest<User>(api.post('/users', data)),
  update: (id: number, data: any) => handleRequest<User>(api.put(`/users/${id}`, data)),
  delete: (id: number) => handleRequest(api.delete(`/users/${id}`)),
};

export const cartsApi = {
  getByUser: (userId: number) => handleRequest<Cart>(api.get(`/carts/user/${userId}`)),
  addItem: (userId: number, data: any) => handleRequest(api.post(`/carts/user/${userId}/items`, data)),
  removeItem: (userId: number, itemId: number) => handleRequest(api.delete(`/carts/user/${userId}/items/${itemId}`)),
  clearCart: (userId: number) => handleRequest(api.delete(`/carts/user/${userId}`)),
  updateItem: (userId: number, itemId: number, data: any) => handleRequest(api.put(`/carts/user/${userId}/items/${itemId}`, data)),
  createCart: (userId: number, data: any) => handleRequest(api.post(`/carts/user/${userId}`, data)), 
};

export const dashboardApi = {
  getUsersWithCarts: (): Promise<UserWithCart[]> => 
    handleRequest(api.get<UserWithCart[]>('/dashboard/users-with-carts')),
  
  getStats: (): Promise<DashboardStats> =>
    handleRequest(api.get<DashboardStats>('/dashboard/stats')),
};