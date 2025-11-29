import { useState, useEffect } from 'react';
import { dashboardApi } from '../api/api';
import type { DashboardStats } from '../../types/dashboard';
import type { UserWithCart } from '../../types/user';

export function useDashboard() {
  const [users, setUsers] = useState<UserWithCart[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setError(null);
      setLoading(true);
      
      // ✅ Параллельная загрузка пользователей и статистики
      const [usersData, statsData] = await Promise.all([
        dashboardApi.getUsersWithCarts(),
        dashboardApi.getStats()
      ]);
      
      setUsers(usersData);
      setStats(statsData);
    } catch (err) {
      setError('Не удалось загрузить данные дашборда');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const refresh = () => {
    fetchDashboardData();
  };

  return {
    // Данные
    users,
    stats,
    
    // Состояние
    loading,
    error,
    
    // Методы
    refresh,
  };
}