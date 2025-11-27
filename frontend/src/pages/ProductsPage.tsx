import { useEffect, useState } from "react";
import axios from "axios";
import { productsApi } from "../api/api";
import type { Product } from "../../types/product";
import { useProducts } from "../hooks/useProduct";
import { ProductCard } from "../components/ProductCard";
import { Pagination } from "../components/Pagination";




const PAGE_SIZE = 12;

export default function ProductsPage() {
  const {
    products,
    loading,
    error,
    page,
    setPage,
    sortBy,
    setSortBy,
    totalPages,
    editingId,
    editForm,
    setEditForm,
    startEdit,
    cancelEdit,
    saveEdit,
    deleteProduct
  } = useProducts();

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <div className="text-red-600 text-xl">{error}</div>
        </div>
      </div>
    );
  }

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

        {/* Кнопки сортировки */}
        <div className="flex justify-center gap-4 mb-8 flex-wrap">
          <button
            onClick={() => setSortBy('title')}
            className={`px-6 py-3 rounded-lg font-medium transition ${
              sortBy === 'title' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            По названию
          </button>
          <button
            onClick={() => setSortBy('price-asc')}
            className={`px-6 py-3 rounded-lg font-medium transition ${
              sortBy === 'price-asc' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            По цене ↑
          </button>
          <button
            onClick={() => setSortBy('price-desc')}
            className={`px-6 py-3 rounded-lg font-medium transition ${
              sortBy === 'price-desc' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
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
            {/* Сетка продуктов */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {products.map((p) => (
                <ProductCard
                  key={p.id}
                  product={p}
                  isEditing={editingId === p.id}
                  editForm={editForm}
                  onEditFormChange={setEditForm}
                  onStartEdit={() => startEdit(p)}
                  onSaveEdit={saveEdit}
                  onCancelEdit={cancelEdit}
                  onDelete={() => deleteProduct(p.id)}
                />
              ))}
            </div>

            {/* Пагинация */}
            <Pagination
              page={page}
              totalPages={totalPages}
              onPageChange={setPage}
            />
          </>
        )}
      </div>
    </div>
  );
}
