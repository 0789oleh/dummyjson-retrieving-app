import type { DashboardStats } from "../../types/dashboard";

// components/StatsCards.tsx
interface StatsCardsProps {
  stats: DashboardStats;
}

export function StatsCards({ stats }: StatsCardsProps) {
  return (
    <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-6 max-w-6xl mx-auto">
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <div className="text-3xl font-bold text-indigo-600">{stats.totalUsers}</div>
        <div className="text-gray-600">Всего пользователей</div>
      </div>
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <div className="text-3xl font-bold text-green-600">{stats.usersWithCarts}</div>
        <div className="text-gray-600">С активными корзинами</div>
      </div>
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <div className="text-3xl font-bold text-purple-600">${stats.totalRevenue}</div>
        <div className="text-gray-600">Общий доход</div>
      </div>
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <div className="text-3xl font-bold text-blue-600">${stats.averageCartValue}</div>
        <div className="text-gray-600">Средний чек</div>
      </div>
    </div>
  );
}