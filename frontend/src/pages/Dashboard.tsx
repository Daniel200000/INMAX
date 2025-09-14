import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  Megaphone, 
  Eye, 
  MousePointer, 
  TrendingUp, 
  DollarSign,
  Users,
  Settings
} from 'lucide-react';
import { calculateRealStats, getDashboardConfig, DashboardConfig } from '../services/localStorage';
import StatsCard from '../components/Dashboard/StatsCard';
import RecentCampaigns from '../components/Dashboard/RecentCampaigns';
import PerformanceChart from '../components/Dashboard/PerformanceChart';
import DashboardConfigModal from '../components/Dashboard/DashboardConfigModal';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(calculateRealStats());
  const [loading, setLoading] = useState(false);
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [dashboardConfig, setDashboardConfig] = useState<DashboardConfig>(getDashboardConfig());

  useEffect(() => {
    // Refresh stats every 30 seconds for real-time updates
    const interval = setInterval(() => {
      setStats(calculateRealStats());
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const handleConfigSave = (newConfig: DashboardConfig) => {
    setDashboardConfig(newConfig);
    setShowConfigModal(false);
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1>{t('dashboard.title')}</h1>
          <p>{t('dashboard.subtitle')}</p>
        </div>
        <button 
          className="config-button"
          onClick={() => setShowConfigModal(true)}
          title={t('dashboard.configure')}
        >
          <Settings size={20} />
          {t('dashboard.configure')}
        </button>
      </div>

      <div className="stats-grid">
        {dashboardConfig.widgets.totalCampaigns && (
          <StatsCard
            title={t('dashboard.totalCampaigns')}
            value={stats.totalCampaigns.value}
            icon={Megaphone}
            color="#667eea"
            change={`${stats.totalCampaigns.change >= 0 ? '+' : ''}${stats.totalCampaigns.change}%`}
          />
        )}
        {dashboardConfig.widgets.activeCampaigns && (
          <StatsCard
            title={t('dashboard.activeCampaigns')}
            value={stats.activeCampaigns.value}
            icon={TrendingUp}
            color="#10b981"
            change={`${stats.activeCampaigns.change >= 0 ? '+' : ''}${stats.activeCampaigns.change}%`}
          />
        )}
        {dashboardConfig.widgets.totalViews && (
          <StatsCard
            title={t('dashboard.totalViews')}
            value={stats.totalViews.value}
            icon={Eye}
            color="#3b82f6"
            change={`${stats.totalViews.change >= 0 ? '+' : ''}${stats.totalViews.change}%`}
          />
        )}
        {dashboardConfig.widgets.totalClicks && (
          <StatsCard
            title={t('dashboard.totalClicks')}
            value={stats.totalClicks.value}
            icon={MousePointer}
            color="#8b5cf6"
            change={`${stats.totalClicks.change >= 0 ? '+' : ''}${stats.totalClicks.change}%`}
          />
        )}
        {dashboardConfig.widgets.conversions && (
          <StatsCard
            title={t('dashboard.conversions')}
            value={stats.conversions.value}
            icon={Users}
            color="#f59e0b"
            change={`${stats.conversions.change >= 0 ? '+' : ''}${stats.conversions.change}%`}
          />
        )}
        {dashboardConfig.widgets.totalSpend && (
          <StatsCard
            title={t('dashboard.totalSpend')}
            value={`$${stats.totalSpend.value.toLocaleString()}`}
            icon={DollarSign}
            color="#ef4444"
            change={`${stats.totalSpend.change >= 0 ? '+' : ''}${stats.totalSpend.change}%`}
          />
        )}
      </div>

      <div className="dashboard-content">
        {dashboardConfig.charts.performanceChart && (
          <div className="chart-section">
            <PerformanceChart />
          </div>
        )}
        
        <div className="recent-section">
          <RecentCampaigns />
        </div>
      </div>

      {showConfigModal && (
        <DashboardConfigModal
          config={dashboardConfig}
          onSave={handleConfigSave}
          onClose={() => setShowConfigModal(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
