import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, Trash2, Calendar, DollarSign, Eye, MousePointer, TrendingUp } from 'lucide-react';
import { Campaign } from '../types/campaign';
import { campaignService } from '../services/campaignService';
import './CampaignDetail.css';

const CampaignDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchCampaign();
    }
  }, [id]);

  const fetchCampaign = async () => {
    try {
      setLoading(true);
      const data = await campaignService.getCampaign(id!);
      setCampaign(data);
    } catch (error) {
      console.error('Error fetching campaign:', error);
      navigate('/campaigns');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta campaña?')) {
      try {
        await campaignService.deleteCampaign(id!);
        navigate('/campaigns');
      } catch (error) {
        console.error('Error deleting campaign:', error);
        alert('Error al eliminar la campaña');
      }
    }
  };

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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="campaign-detail-loading">
        <div className="loading-spinner"></div>
        <p>Cargando campaña...</p>
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="campaign-detail-error">
        <h2>Campaña no encontrada</h2>
        <p>La campaña que buscas no existe o ha sido eliminada.</p>
        <button onClick={() => navigate('/campaigns')} className="back-btn">
          Volver a Campañas
        </button>
      </div>
    );
  }

  return (
    <div className="campaign-detail">
      <div className="campaign-detail-header">
        <button onClick={() => navigate('/campaigns')} className="back-button">
          <ArrowLeft size={20} />
          Volver
        </button>
        
        <div className="campaign-actions">
          <button 
            onClick={() => navigate(`/campaigns/${campaign.id}/edit`)}
            className="edit-button"
          >
            <Edit size={16} />
            Editar
          </button>
          <button 
            onClick={handleDelete}
            className="delete-button"
          >
            <Trash2 size={16} />
            Eliminar
          </button>
        </div>
      </div>

      <div className="campaign-detail-content">
        <div className="campaign-info">
          <div className="campaign-title-section">
            <h1 className="campaign-title">{campaign.name}</h1>
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
              <span className="campaign-priority">
                {campaign.priority.toUpperCase()}
              </span>
            </div>
          </div>

          {campaign.description && (
            <div className="campaign-description">
              <h3>Descripción</h3>
              <p>{campaign.description}</p>
            </div>
          )}

          <div className="campaign-details-grid">
            <div className="detail-card">
              <Calendar size={20} />
              <div>
                <h4>Fechas</h4>
                <p>{formatDate(campaign.start_date)} - {formatDate(campaign.end_date)}</p>
              </div>
            </div>
            
            <div className="detail-card">
              <DollarSign size={20} />
              <div>
                <h4>Presupuesto</h4>
                <p>${campaign.budget.toLocaleString()}</p>
              </div>
            </div>
            
            <div className="detail-card">
              <Eye size={20} />
              <div>
                <h4>Vistas</h4>
                <p>{(campaign.stats?.views || campaign.views_count || 0).toLocaleString()}</p>
              </div>
            </div>
            
            <div className="detail-card">
              <MousePointer size={20} />
              <div>
                <h4>Clicks</h4>
                <p>{(campaign.stats?.clicks || campaign.clicks_count || 0).toLocaleString()}</p>
              </div>
            </div>
            
            <div className="detail-card">
              <TrendingUp size={20} />
              <div>
                <h4>Conversiones</h4>
                <p>{(campaign.stats?.conversions || campaign.conversions_count || 0).toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CampaignDetail;
