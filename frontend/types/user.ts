import type { Base } from './base';

export interface User extends Base { 
    firstName: string;
    lastName: string;
    email: string;
}