import type { Base } from './base';

export interface User extends Base {
    firstName: string;
    lastName: string;
    email: string;
}

export interface CreateUserDto {
    firstName: string;
    lastName: string;
    email: string;
    password: string;
}

export interface UpdateUserDto {
    firstName?: string;
    lastName?: string;
    email?: string;
    password?: string;
}

export interface UserWithCart extends User {
    cart?: {
        id: number;
        items: Array<{
            productId: number;
            quantity: number;
            price: number;
        }>;
        totalPrice: number;
    };
}