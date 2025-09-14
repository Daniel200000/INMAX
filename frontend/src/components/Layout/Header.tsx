import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import LanguageSelector from '../Common/LanguageSelector';
import { Bell, Search, User, LogOut } from 'lucide-react';
import './Header.css';

const Header: React.FC = () => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="header">
      <div className="header-left">
        <div className="search-container">
          <Search size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Buscar campañas, ubicaciones..."
            className="search-input"
          />
        </div>
      </div>
      
      <div className="header-right">
        <LanguageSelector />
        
        <button className="notification-btn">
          <Bell size={20} />
          <span className="notification-badge">3</span>
        </button>
        
        <div className="user-menu">
          <div className="user-info">
            <div className="user-avatar">
              <User size={20} />
            </div>
            <div className="user-details">
              <span className="user-name">{user?.name || 'Usuario'}</span>
              <span className="user-role">{user?.role || 'user'}</span>
            </div>
          </div>
          
          <button className="logout-btn" onClick={handleLogout}>
            <LogOut size={16} />
            Cerrar Sesión
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
