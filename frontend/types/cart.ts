import type { Base } from './base';

export interface Cart extends Base {
    userId: number;
    items: CartItem[];
}

export interface CartItem extends Base {
    product: {
        id: number;
        title: string;
        price: number;
        description?: string;
    };
    quantity: number;
}

export interface CreateCartDto {
    userId: number;
    items?: { productId: number; quantity: number }[];
}

export interface UpdateCartDto {
    items?: { productId: number; quantity: number }[];
}