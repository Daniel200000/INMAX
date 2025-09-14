import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Campaign } from '../../types/campaign';
import { campaignService } from '../../services/campaignService';
import { Eye, MousePointer, TrendingUp, MoreVertical, Calendar, DollarSign, Edit, Trash2 } from 'lucide-react';
import './CampaignCard.css';

interface CampaignCardProps {
  campaign: Campaign;
  onCampaignDeleted?: () => void;
}

const CampaignCard: React.FC<CampaignCardProps> = ({ campaign, onCampaignDeleted }) => {
  const [showMenu, setShowMenu] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const navigate = useNavigate();
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#10b981';
      case 'paused': return '#f59e0b';
      case 'finished': return '#6b7280';
      case 'cancelled': return '#ef4444';
      case 'draft': return '#8b5cf6';
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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return '#ef4444';
      case 'high': return '#f59e0b';
      case 'medium': return '#3b82f6';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const calculateCTR = () => {
    if (campaign.views_count === 0) return 0;
    return ((campaign.clicks_count / campaign.views_count) * 100).toFixed(2);
  };

  const calculateConversionRate = () => {
    if (campaign.clicks_count === 0) return 0;
    return ((campaign.conversions_count / campaign.clicks_count) * 100).toFixed(2);
  };

  const handleDelete = async () => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta campaña?')) {
      try {
        setIsDeleting(true);
        await campaignService.deleteCampaign(campaign.id);
        if (onCampaignDeleted) {
          onCampaignDeleted();
        }
      } catch (error) {
        console.error('Error deleting campaign:', error);
        alert('Error al eliminar la campaña');
      } finally {
        setIsDeleting(false);
        setShowMenu(false);
      }
    }
  };

  const handleView = () => {
    navigate(`/campaigns/${campaign.id}`);
  };

  const handleEdit = () => {
    navigate(`/campaigns/${campaign.id}/edit`);
  };

  return (
    <div className="campaign-card">
      <div className="campaign-card-header">
        <div className="campaign-title-section">
          <h3 className="campaign-name">{campaign.name}</h3>
          <div className="campaign-badges">
            <span 
              className="campaign-status"
              style={{ 
                backgroundColor: getStatusColor(campaign.status) + '20', 
                color: getStatusColor(campaign.status) 
              }}
            >
              {getStatusText(campaign.status)}
            </span>
            <span 
              className="campaign-priority"
              style={{ 
                backgroundColor: getPriorityColor(campaign.priority) + '20', 
                color: getPriorityColor(campaign.priority) 
              }}
            >
              {campaign.priority.toUpperCase()}
            </span>
          </div>
        </div>
        <div className="campaign-menu-container">
          <button 
            className="campaign-menu-btn"
            onClick={() => setShowMenu(!showMenu)}
          >
            <MoreVertical size={16} />
          </button>
          {showMenu && (
            <div className="campaign-menu-dropdown">
              <button onClick={handleView} className="menu-item">
                <Eye size={16} />
                Ver Detalles
              </button>
              <button onClick={handleEdit} className="menu-item">
                <Edit size={16} />
                Editar
              </button>
              <button 
                onClick={handleDelete} 
                className="menu-item delete-item"
                disabled={isDeleting}
              >
                <Trash2 size={16} />
                {isDeleting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          )}
        </div>
      </div>

      {campaign.description && (
        <p className="campaign-description">{campaign.description}</p>
      )}

      <div className="campaign-details">
        <div className="campaign-detail">
          <Calendar size={16} />
          <span>{formatDate(campaign.start_date)} - {formatDate(campaign.end_date)}</span>
        </div>
        <div className="campaign-detail">
          <DollarSign size={16} />
          <span>${campaign.budget.toLocaleString()}</span>
        </div>
      </div>

      <div className="campaign-metrics">
        <div className="metric">
          <div className="metric-icon">
            <Eye size={16} />
          </div>
          <div className="metric-content">
            <span className="metric-value">{campaign.views_count.toLocaleString()}</span>
            <span className="metric-label">Vistas</span>
          </div>
        </div>
        
        <div className="metric">
          <div className="metric-icon">
            <MousePointer size={16} />
          </div>
          <div className="metric-content">
            <span className="metric-value">{campaign.clicks_count.toLocaleString()}</span>
            <span className="metric-label">Clicks</span>
          </div>
        </div>
        
        <div className="metric">
          <div className="metric-icon">
            <TrendingUp size={16} />
          </div>
          <div className="metric-content">
            <span className="metric-value">{campaign.conversions_count.toLocaleString()}</span>
            <span className="metric-label">Conversiones</span>
          </div>
        </div>
      </div>

      <div className="campaign-stats">
        <div className="stat">
          <span className="stat-label">CTR</span>
          <span className="stat-value">{calculateCTR()}%</span>
        </div>
        <div className="stat">
          <span className="stat-label">Conversión</span>
          <span className="stat-value">{calculateConversionRate()}%</span>
        </div>
      </div>

      <div className="campaign-actions">
        <button onClick={handleView} className="action-btn view-btn">
          <Eye size={16} />
          Ver
        </button>
        <button onClick={handleEdit} className="action-btn edit-btn">
          <Edit size={16} />
          Editar
        </button>
      </div>
    </div>
  );
};

export default CampaignCard;
