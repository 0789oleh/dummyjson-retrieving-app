import type { Product } from './product';

export interface CartWithItems {
  id: number;
  total: number;  // ← Используйте total везде
  items: CartItemWithProduct[];
}

export interface CartItemWithProduct {
  id: number;
  productId: number;
  quantity: number;
  product: Product;  // ← Полный продукт, а не только price
}

export interface DashboardStats {
  totalUsers: number;
  usersWithCarts: number;
  totalRevenue: number;
  averageCartValue: number;
  popularProducts: Product[];
}