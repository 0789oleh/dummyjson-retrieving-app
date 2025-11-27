import axios from 'axios';
import dotenv from 'dotenv';
import type { Product } from '../../types/product';

dotenv.config();

const api = axios.create({ baseURL: process.env.BASE_URL});

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
  getAll: () => handleRequest(api.get('/users')),
  create: (data: any) => handleRequest(api.post('/users', data)),
  update: (id: number, data: any) => handleRequest(api.put(`/users/${id}`, data)),
  delete: (id: number) => handleRequest(api.delete(`/users/${id}`)),
};

export const cartsApi = {
  getByUser: (userId: number) => handleRequest(api.get(`/carts/user/${userId}`)),
  addItem: (userId: number, data: any) => handleRequest(api.post(`/carts/user/${userId}/items`, data)),
  removeItem: (userId: number, itemId: number) => handleRequest(api.delete(`/carts/user/${userId}/items/${itemId}`)),  
  // etc.
};