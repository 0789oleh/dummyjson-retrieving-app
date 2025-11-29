import type { UserWithCart } from '../../types/user';

interface UserCardsProps {
  users: UserWithCart[];
}

export function UserCards({ users }: UserCardsProps) {
  return (
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
              <h4 className="font-semibold text-lg mb-4">
                Корзина ({user.cart.items.length} товаров)
              </h4>
              <div className="space-y-3 max-h-40 overflow-y-auto">
                {user.cart.items.map((item) => (
                  <div key={item.productId} className="flex justify-between text-sm">
                    <span className="text-gray-700 truncate max-w-[120px]">
                      {item.productId} × {item.quantity}
                    </span>
                    <span className="font-medium whitespace-nowrap">
                      ${(item.price * item.quantity).toFixed(2)}
                    </span>
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
            <div className="border-t pt-6">
              <p className="text-gray-500 italic text-center py-4">Корзина пуста</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}