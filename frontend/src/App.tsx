import { Routes, Route, Link } from "react-router-dom";
import ProductsPage from "./pages/ProductsPage";
import DashboardPage from './pages/DashboardPage';

function Navigation() {
  return (
    <nav className="hidden md:flex space-x-8 font-semibold text-gray-800">

    {/* Ссылки */}
    <div className="flex items-center space-x-10 text-lg font-medium">
      <Link 
        to="/" 
        className="hover:text-indigo-200 transition duration-200 px-4 py-2 rounded-lg hover:bg-white/10"
      >
        Пользователи
      </Link>
      <Link 
        to="/products" 
        className="hover:text-indigo-200 transition duration-200 px-4 py-2 rounded-lg hover:bg-white/10"
      >
        Товары
      </Link>
    </div>
</nav>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/products" element={<ProductsPage />} />
      </Routes>
    </div>
  );
}