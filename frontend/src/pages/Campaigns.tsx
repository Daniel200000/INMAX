import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { Plus, Search, Filter, MoreVertical, Eye, Edit, Trash2 } from 'lucide-react';
import { Campaign, CampaignFilters } from '../types/campaign';
import { campaignService } from '../services/campaignService';
import CampaignCard from '../components/Campaigns/CampaignCard';
import './Campaigns.css';

const Campaigns: React.FC = () => {
  const { t } = useTranslation();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<CampaignFilters>({});
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchCampaigns();
  }, [filters]);

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const data = await campaignService.getCampaigns(filters);
      setCampaigns(data.campaigns);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setFilters({ ...filters, search: searchTerm });
  };

  const handleStatusFilter = (status: string) => {
    setFilters({ ...filters, status: status === 'all' ? undefined : status });
  };

  const handleCampaignDeleted = () => {
    fetchCampaigns(); // Refresh the campaigns list
  };

  const getStatusCounts = () => {
    const counts = {
      all: campaigns.length,
      active: campaigns.filter(c => c.status === 'active').length,
      paused: campaigns.filter(c => c.status === 'paused').length,
      finished: campaigns.filter(c => c.status === 'finished').length,
      draft: campaigns.filter(c => c.status === 'draft').length,
    };
    return counts;
  };

  const statusCounts = getStatusCounts();

  if (loading) {
    return (
      <div className="campaigns-loading">
        <div className="loading-spinner"></div>
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  return (
    <div className="campaigns">
      <div className="campaigns-header">
        <div className="campaigns-title">
          <h1>{t('campaigns.title')}</h1>
          <p>{t('campaigns.subtitle')}</p>
        </div>
        <Link to="/campaigns/create" className="create-campaign-btn">
          <Plus size={20} />
          {t('campaigns.newCampaign')}
        </Link>
      </div>

      <div className="campaigns-filters">
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-container">
            <Search size={20} className="search-icon" />
            <input
              type="text"
              placeholder={t('campaigns.searchPlaceholder')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
        </form>

        <div className="status-filters">
          {[
            { key: 'all', label: t('campaigns.filters.all'), count: statusCounts.all },
            { key: 'active', label: t('campaigns.filters.active'), count: statusCounts.active },
            { key: 'paused', label: t('campaigns.filters.paused'), count: statusCounts.paused },
            { key: 'finished', label: t('campaigns.filters.finished'), count: statusCounts.finished },
            { key: 'draft', label: t('campaigns.filters.draft'), count: statusCounts.draft },
          ].map(({ key, label, count }) => (
            <button
              key={key}
              className={`status-filter ${filters.status === key || (key === 'all' && !filters.status) ? 'active' : ''}`}
              onClick={() => handleStatusFilter(key)}
            >
              {label}
              <span className="status-count">{count}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="campaigns-grid">
        {campaigns.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <Plus size={48} />
            </div>
            <h3>{t('campaigns.empty.title')}</h3>
            <p>{t('campaigns.empty.subtitle')}</p>
            <Link to="/campaigns/create" className="create-first-btn">
              {t('campaigns.empty.createFirst')}
            </Link>
          </div>
        ) : (
          campaigns.map((campaign) => (
            <CampaignCard 
              key={campaign.id} 
              campaign={campaign} 
              onCampaignDeleted={handleCampaignDeleted}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Campaigns;
