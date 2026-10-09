import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Search from './pages/Search';
import AddData from './pages/AddData';
import ML from './pages/ML';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <BrowserRouter>
      <nav className="bg-gray-800 text-white p-4">
        <div className="flex gap-4">
          <Link to="/">Dashboard</Link>
          <Link to="/search">Search</Link>
          <Link to="/add">Add Data</Link>
          <Link to="/ml">ML</Link>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/search" element={<Search />} />
        <Route path="/add" element={<AddData />} />
        <Route path="/ml" element={<ML />} />
      </Routes>
    </BrowserRouter>
  );
}
