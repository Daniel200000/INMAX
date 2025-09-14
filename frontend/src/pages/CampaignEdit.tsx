import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { ArrowLeft, Save, X } from 'lucide-react';
import { Campaign, CampaignUpdate } from '../types/campaign';
import { campaignService } from '../services/campaignService';
import './CampaignEdit.css';

const CampaignEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const { register, handleSubmit, formState: { errors }, reset } = useForm<CampaignUpdate>();

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
      reset({
        name: data.name,
        description: data.description || '',
        budget: data.budget,
        channel: data.channel,
        start_date: data.start_date.split('T')[0],
        end_date: data.end_date.split('T')[0],
        priority: data.priority,
      });
    } catch (error) {
      console.error('Error fetching campaign:', error);
      navigate('/campaigns');
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (data: CampaignUpdate) => {
    try {
      setSaving(true);
      await campaignService.updateCampaign(id!, data);
      navigate(`/campaigns/${id}`);
    } catch (error) {
      console.error('Error updating campaign:', error);
      alert('Error al actualizar la campaña');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="campaign-edit-loading">
        <div className="loading-spinner"></div>
        <p>Cargando campaña...</p>
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="campaign-edit-error">
        <h2>Campaña no encontrada</h2>
        <p>La campaña que buscas no existe o ha sido eliminada.</p>
        <button onClick={() => navigate('/campaigns')} className="back-btn">
          Volver a Campañas
        </button>
      </div>
    );
  }

  return (
    <div className="campaign-edit">
      <div className="campaign-edit-header">
        <button onClick={() => navigate(`/campaigns/${id}`)} className="back-button">
          <ArrowLeft size={20} />
          Volver
        </button>
        
        <h1>Editar Campaña</h1>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="campaign-edit-form">
        <div className="form-section">
          <h2>Información Básica</h2>
          
          <div className="form-group">
            <label htmlFor="name">Nombre de la Campaña *</label>
            <input
              type="text"
              id="name"
              {...register('name', { required: 'El nombre es requerido' })}
              className={errors.name ? 'error' : ''}
            />
            {errors.name && <span className="error-message">{errors.name.message}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="description">Descripción</label>
            <textarea
              id="description"
              {...register('description')}
              rows={4}
              placeholder="Describe el objetivo de la campaña..."
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="budget">Presupuesto *</label>
              <input
                type="number"
                id="budget"
                {...register('budget', { 
                  required: 'El presupuesto es requerido',
                  min: { value: 1, message: 'El presupuesto debe ser mayor a 0' }
                })}
                className={errors.budget ? 'error' : ''}
              />
              {errors.budget && <span className="error-message">{errors.budget.message}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="channel">Canal *</label>
              <select
                id="channel"
                {...register('channel', { required: 'El canal es requerido' })}
                className={errors.channel ? 'error' : ''}
              >
                <option value="">Seleccionar canal</option>
                <option value="facebook">Facebook</option>
                <option value="instagram">Instagram</option>
                <option value="google">Google Ads</option>
                <option value="twitter">Twitter</option>
                <option value="linkedin">LinkedIn</option>
                <option value="youtube">YouTube</option>
              </select>
              {errors.channel && <span className="error-message">{errors.channel.message}</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_date">Fecha de Inicio *</label>
              <input
                type="date"
                id="start_date"
                {...register('start_date', { required: 'La fecha de inicio es requerida' })}
                className={errors.start_date ? 'error' : ''}
              />
              {errors.start_date && <span className="error-message">{errors.start_date.message}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="end_date">Fecha de Fin *</label>
              <input
                type="date"
                id="end_date"
                {...register('end_date', { required: 'La fecha de fin es requerida' })}
                className={errors.end_date ? 'error' : ''}
              />
              {errors.end_date && <span className="error-message">{errors.end_date.message}</span>}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="priority">Prioridad *</label>
            <select
              id="priority"
              {...register('priority', { required: 'La prioridad es requerida' })}
              className={errors.priority ? 'error' : ''}
            >
              <option value="">Seleccionar prioridad</option>
              <option value="low">Baja</option>
              <option value="medium">Media</option>
              <option value="high">Alta</option>
              <option value="urgent">Urgente</option>
            </select>
            {errors.priority && <span className="error-message">{errors.priority.message}</span>}
          </div>
        </div>

        <div className="form-actions">
          <button 
            type="button" 
            onClick={() => navigate(`/campaigns/${id}`)}
            className="cancel-button"
          >
            <X size={16} />
            Cancelar
          </button>
          <button 
            type="submit" 
            className="save-button"
            disabled={saving}
          >
            <Save size={16} />
            {saving ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CampaignEdit;
