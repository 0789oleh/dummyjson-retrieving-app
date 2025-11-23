import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000/api/v1' });

export const productsApi = {
  getAll: () => api.get('/products').then(res => res.data),
  create: (data: any) => api.post('/products', data).then(res => res.data),
  // update, delete
};

export const cartsApi = {
  getByUser: (userId: number) => api.get(`/carts/user/${userId}`).then(res => res.data),
  // etc.
};