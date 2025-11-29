// components/ProductForm.tsx
import { useState } from 'react';
import type { Product } from '../../types/product';

interface ProductFormProps {
  product: Product;
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

export function ProductForm({ product, onSubmit, onCancel }: ProductFormProps) {
  const [formData, setFormData] = useState({
    title: product.title,
    price: product.price,
    description: product.description || ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Название</label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
          className="w-full border p-2 rounded"
          required
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium mb-1">Цена</label>
        <input
          type="number"
          value={formData.price}
          onChange={(e) => setFormData(prev => ({ ...prev, price: Number(e.target.value) }))}
          className="w-full border p-2 rounded"
          required
        />
      </div>

      <div className="flex gap-2 pt-4">
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">
          Сохранить
        </button>
        <button type="button" onClick={onCancel} className="bg-gray-500 text-white px-4 py-2 rounded">
          Отмена
        </button>
      </div>
    </form>
  );
}