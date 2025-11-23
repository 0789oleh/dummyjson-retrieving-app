import { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  id: number;
  title: string;
  price: number;
}

interface CartItem {
  product: Product;
  quantity: number;
}

interface User {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  cart?: {
    items: CartItem[];
    totalPrice: number;
  };
}

export default function DashboardPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://localhost:8000/users/with-carts")
      .then(res => {
        setUsers(res.data);
        setLoading(false);
      })
      .catch(() => {
        alert("Не забудь запустить бэкенд: docker compose up --build");
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center py-20 text-2xl">Загрузка пользователей и корзин...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Пользователи и их корзины
          </h1>
          <p className="text-xl text-gray-600">
            Данные из dummyjson.com + связи + PostgreSQL
          </p>
        </header>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {users.map(user => (
            <div key={user.id} className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  {user.firstName[0]}{user.lastName[0]}
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-800">
                    {user.firstName} {user.lastName}
                  </h3>
                  <p className="text-gray-600">{user.email}</p>
                </div>
              </div>

              {user.cart ? (
                <div className="border-t pt-6">
                  <h4 className="font-semibold text-lg mb-4">Корзина ({user.cart.items.length} товаров):</h4>
                  <div className="space-y-3">
                    {user.cart.items.map((item, i) => (
                      <div key={i} className="flex justify-between text-sm">
                        <span className="text-gray-700">{item.product.title} × {item.quantity}</span>
                        <span className="font-medium">${(item.product.price * item.quantity).toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6 pt-6 border-t text-right">
                    <span className="text-2xl font-bold text-indigo-600">
                      Итого: ${user.cart.totalPrice.toFixed(2)}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500 italic">Корзина пуста</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}