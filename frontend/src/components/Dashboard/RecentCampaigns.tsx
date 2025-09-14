import React, { useState, useEffect } from 'react';
import { Campaign } from '../../types/campaign';
import { campaignService } from '../../services/campaignService';
import { Eye, MousePointer, TrendingUp, MoreVertical } from 'lucide-react';
import './RecentCampaigns.css';

const RecentCampaigns: React.FC = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const data = await campaignService.getCampaigns({ limit: 5 });
        setCampaigns(data.campaigns);
      } catch (error) {
        console.error('Error fetching campaigns:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#10b981';
      case 'paused': return '#f59e0b';
      case 'finished': return '#6b7280';
      case 'cancelled': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Activa';
      case 'paused': return 'Pausada';
      case 'finished': return 'Finalizada';
      case 'cancelled': return 'Cancelada';
      case 'draft': return 'Borrador';
      default: return status;
    }
  };

  if (loading) {
    return (
      <div className="recent-campaigns">
        <h3>Campañas Recientes</h3>
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Cargando campañas...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="recent-campaigns">
      <div className="recent-campaigns-header">
        <h3>Campañas Recientes</h3>
        <button className="view-all-btn">Ver todas</button>
      </div>

      <div className="campaigns-list">
        {campaigns.length === 0 ? (
          <div className="empty-state">
            <p>No hay campañas disponibles</p>
          </div>
        ) : (
          campaigns.map((campaign) => (
            <div key={campaign.id} className="campaign-item">
              <div className="campaign-info">
                <h4 className="campaign-name">{campaign.name}</h4>
                <p className="campaign-description">{campaign.description}</p>
                <div className="campaign-metrics">
                  <div className="metric">
                    <Eye size={16} />
                    <span>{campaign.stats?.views || campaign.views_count || 0}</span>
                  </div>
                  <div className="metric">
                    <MousePointer size={16} />
                    <span>{campaign.stats?.clicks || campaign.clicks_count || 0}</span>
                  </div>
                  <div className="metric">
                    <TrendingUp size={16} />
                    <span>{campaign.stats?.conversions || campaign.conversions_count || 0}</span>
                  </div>
                </div>
              </div>
              
              <div className="campaign-actions">
                <div 
                  className="campaign-status"
                  style={{ backgroundColor: getStatusColor(campaign.status) + '20', color: getStatusColor(campaign.status) }}
                >
                  {getStatusText(campaign.status)}
                </div>
                <button className="campaign-menu-btn">
                  <MoreVertical size={16} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default RecentCampaigns;
