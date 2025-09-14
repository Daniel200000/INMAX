import React from 'react';
import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Megaphone, 
  BarChart3, 
  Settings, 
  Users,
  MapPin,
  FileText
} from 'lucide-react';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  const { t } = useTranslation();
  
  const menuItems = [
    { path: '/', icon: LayoutDashboard, label: t('navigation.dashboard') },
    { path: '/campaigns', icon: Megaphone, label: t('navigation.campaigns') },
    { path: '/analytics', icon: BarChart3, label: 'Analíticas' },
    { path: '/locations', icon: MapPin, label: 'Ubicaciones' },
    { path: '/media', icon: FileText, label: 'Medios' },
    { path: '/users', icon: Users, label: 'Usuarios' },
    { path: '/settings', icon: Settings, label: t('navigation.settings') },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>INMAX AVISADORES</h2>
        <p>Módulo de Campañas</p>
      </div>
      
      <nav className="sidebar-nav">
        <ul className="nav-list">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.path} className="nav-item">
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `nav-link ${isActive ? 'active' : ''}`
                  }
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
