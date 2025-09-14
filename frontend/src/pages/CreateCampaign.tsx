import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { ArrowLeft, Save, Eye } from 'lucide-react';
import { CampaignCreate } from '../types/campaign';
import { campaignService } from '../services/campaignService';
import './CreateCampaign.css';

const CreateCampaign: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CampaignCreate>();

  const onSubmit = async (data: CampaignCreate) => {
    try {
      setLoading(true);
      await campaignService.createCampaign(data);
      navigate('/campaigns');
    } catch (error) {
      console.error('Error creating campaign:', error);
    } finally {
      setLoading(false);
    }
  };

  const channels = [
    { value: 'social_media', label: 'Redes Sociales' },
    { value: 'display', label: 'Display' },
    { value: 'search', label: 'Búsqueda' },
    { value: 'video', label: 'Video' },
    { value: 'mobile', label: 'Móvil' },
    { value: 'email', label: 'Email' },
  ];

  const priorities = [
    { value: 'low', label: 'Baja' },
    { value: 'medium', label: 'Media' },
    { value: 'high', label: 'Alta' },
    { value: 'urgent', label: 'Urgente' },
  ];

  return (
    <div className="create-campaign">
      <div className="create-campaign-header">
        <button 
          className="back-btn"
          onClick={() => navigate('/campaigns')}
        >
          <ArrowLeft size={20} />
          Volver
        </button>
        <div className="header-content">
          <h1>Nueva Campaña</h1>
          <p>Crea una nueva campaña publicitaria</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="campaign-form">
        <div className="form-sections">
          <div className="form-section">
            <h3>Información Básica</h3>
            
            <div className="form-group">
              <label htmlFor="name">Nombre de la Campaña *</label>
              <input
                type="text"
                id="name"
                {...register('name', { required: 'El nombre es requerido' })}
                className={errors.name ? 'error' : ''}
                placeholder="Ej: Campaña Black Friday 2024"
              />
              {errors.name && (
                <span className="error-message">{errors.name.message}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="description">Descripción</label>
              <textarea
                id="description"
                {...register('description')}
                rows={4}
                placeholder="Describe el objetivo y detalles de la campaña..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="channel">Canal *</label>
                <select
                  id="channel"
                  {...register('channel', { required: 'El canal es requerido' })}
                  className={errors.channel ? 'error' : ''}
                >
                  <option value="">Selecciona un canal</option>
                  {channels.map((channel) => (
                    <option key={channel.value} value={channel.value}>
                      {channel.label}
                    </option>
                  ))}
                </select>
                {errors.channel && (
                  <span className="error-message">{errors.channel.message}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="priority">Prioridad</label>
                <select
                  id="priority"
                  {...register('priority')}
                >
                  {priorities.map((priority) => (
                    <option key={priority.value} value={priority.value}>
                      {priority.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Presupuesto y Fechas</h3>
            
            <div className="form-group">
              <label htmlFor="budget">Presupuesto *</label>
              <div className="input-with-symbol">
                <span className="symbol">$</span>
                <input
                  type="number"
                  id="budget"
                  {...register('budget', { 
                    required: 'El presupuesto es requerido',
                    min: { value: 1, message: 'El presupuesto debe ser mayor a 0' }
                  })}
                  className={errors.budget ? 'error' : ''}
                  placeholder="10000"
                />
              </div>
              {errors.budget && (
                <span className="error-message">{errors.budget.message}</span>
              )}
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
                {errors.start_date && (
                  <span className="error-message">{errors.start_date.message}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="end_date">Fecha de Fin *</label>
                <input
                  type="date"
                  id="end_date"
                  {...register('end_date', { required: 'La fecha de fin es requerida' })}
                  className={errors.end_date ? 'error' : ''}
                />
                {errors.end_date && (
                  <span className="error-message">{errors.end_date.message}</span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="preview-btn"
            onClick={() => {/* TODO: Implement preview */}}
          >
            <Eye size={20} />
            Vista Previa
          </button>
          
          <button
            type="submit"
            className="save-btn"
            disabled={loading}
          >
            <Save size={20} />
            {loading ? 'Creando...' : 'Crear Campaña'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateCampaign;
