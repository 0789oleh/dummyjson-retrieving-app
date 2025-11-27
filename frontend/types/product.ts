import type { Base } from './base';

export interface Product extends Base {
  title: string;
  price: number;
  description?: string;
}

export interface CreateProductDto {
  title: string;
  price: number;
  description?: string;
}

export interface UpdateProductDto {
  title?: string;
  price?: number;
  description?: string;
}