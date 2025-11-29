// components/DashboardPage.tsx
import { useDashboard } from '../hooks/useDashboard';
import { StatsCards } from '../components/StatCards';
import { UserCards } from '../components/UserCards';

export default function DashboardPage() {
  const { users, stats, loading, error, refresh } = useDashboard();

  if (loading) return (
    <>
      <div>Загрузка...</div>
      <div>Пожалуйста, подождите</div>
    </>
  );

  if (error) {
    return (
      <div>
        <div>{error}</div>
        <button onClick={refresh}>Повторить</button>
      </div>
    );
  }


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
          
          {/* Статистика */}
          {stats && <StatsCards stats={stats} />}
        </header>

        {/* Пользователи */}
        <UserCards users={users} />
      </div>
    </div>
  );
}