// frontend/src/pages/ProductsPage.tsx
import { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  id: number;
  title: string;
  price: number;
  description?: string;
}





const PAGE_SIZE = 12;

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const [sortBy, setSortBy] = useState<"title" | "price-asc" | "price-desc">("title");

  const sortedProducts = [...products].sort((a, b) => {
    if (sortBy === "title") return a.title.localeCompare(b.title);
    if (sortBy === "price-asc") return a.price - b.price;
    if (sortBy === "price-desc") return b.price - a.price;
    return 0;
  });

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState({ title: "", price: 0 });

  useEffect(() => {
    setLoading(true);
    axios
      .get(`https://dummyjson.com/products?limit=${PAGE_SIZE}&skip=${(page - 1) * PAGE_SIZE}`)
      .then((res) => {
        setProducts(res.data.products);
        setTotal(res.data.total);
        setLoading(false);
      });
  }, [page]);

  const startEdit = (p: Product) => {
    setEditingId(p.id);
    setEditForm({ title: p.title, price: p.price });
  };

  const saveEdit = async (id: number) => {
    try {
      await axios.patch(`http://localhost:8000/products/${id}`, editForm);
      setProducts((prev) =>
        prev.map((p) => (p.id === id ? { ...p, ...editForm } : p))
      );
      setEditingId(null);
    } catch {
      alert("Ошибка сохранения — бэкенд должен быть запущен");
    }
  };

  const deleteProduct = async (id: number) => {
    if (!confirm("Удалить товар?")) return;
    try {
      await axios.delete(`http://localhost:8000/products/${id}`);
      setProducts((prev) => prev.filter((p) => p.id !== id));
    } catch {
      alert("Ошибка удаления");
    }
  };

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
            Товары из dummyjson
          </h1>
          <p className="text-lg text-gray-600">
            Просмотр • Редактирование • Удаление • Сохранение в PostgreSQL
          </p>
        </header>

        <div className="flex justify-center gap-4 mb-8 flex-wrap">
  <button
    onClick={() => setSortBy("title")}
    className={`px-6 py-3 rounded-lg font-medium transition ${sortBy === "title" ? "bg-indigo-600 text-white" : "bg-gray-200 text-gray-700"}`}
  >
    По названию
  </button>
  <button
    onClick={() => setSortBy("price-asc")}
    className={`px-6 py-3 rounded-lg font-medium transition ${sortBy === "price-asc" ? "bg-indigo-600 text-white" : "bg-gray-200 text-gray-700"}`}
  >
    По цене ↑
  </button>
  <button
    onClick={() => setSortBy("price-desc")}
    className={`px-6 py-3 rounded-lg font-medium transition ${sortBy === "price-desc" ? "bg-indigo-600 text-white" : "bg-gray-200 text-gray-700"}`}
  >
    По цене ↓
  </button>
</div>

        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {sortedProducts.map((p) => (
                <div
                  key={p.id}
                  className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden"
                >
                  <div className="bg-gray-200 border-2 border-dashed rounded-t-xl w-full h-48" />
                  
                  <div className="p-5">
                    {editingId === p.id ? (
                      <div className="space-y-3">
                        <input
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                          value={editForm.title}
                          onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                        />
                        <input
                          type="number"
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                          value={editForm.price}
                          onChange={(e) => setEditForm({ ...editForm, price: +e.target.value })}
                        />
                        <div className="flex gap-2">
                          <button
                            onClick={() => saveEdit(p.id)}
                            className="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
                          >
                            Сохранить
                          </button>
                          <button
                            onClick={() => setEditingId(null)}
                            className="flex-1 bg-gray-500 text-white py-2 rounded-lg hover:bg-gray-600 transition"
                          >
                            Отмена
                          </button>
                        </div>
                      </div>
                    ) : (
                      <>
                        <h3 className="font-bold text-lg text-gray-800 line-clamp-2">
                          {p.title}
                        </h3>
                        <p className="text-3xl font-bold text-indigo-600 mt-2">
                          ${p.price}
                        </p>
                        {p.description && (
                          <p className="text-sm text-gray-600 mt-3 line-clamp-3">
                            {p.description}
                          </p>
                        )}

                        <div className="mt-5 flex gap-3">
                          <button
                            onClick={() => startEdit(p)}
                            className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-medium"
                          >
                            Редактировать
                          </button>
                          <button
                            onClick={() => deleteProduct(p.id)}
                            className="flex-1 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition font-medium"
                          >
                            Удалить
                          </button>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Пагинация */}
            <div className="flex justify-center items-center gap-4 mt-12">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className={`px-6 py-3 rounded-lg font-medium transition ${
                  page === 1
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-indigo-600 text-white hover:bg-indigo-700"
                }`}
              >
                ← Назад
              </button>

              <span className="text-lg font-medium text-gray-700">
                Страница {page} из {totalPages} ({total} товаров)
              </span>

              <button
                onClick={() => setPage((p) => p + 1)}
                disabled={page >= totalPages}
                className={`px-6 py-3 rounded-lg font-medium transition ${
                  page >= totalPages
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-indigo-600 text-white hover:bg-indigo-700"
                }`}
              >
                Вперед →
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}