import React, { useState } from 'react';
import { X, BarChart3, PieChart, TrendingUp } from 'lucide-react';
import { DashboardConfig } from '../../services/localStorage';
import './DashboardConfigModal.css';

interface DashboardConfigModalProps {
  config: DashboardConfig;
  onSave: (config: DashboardConfig) => void;
  onClose: () => void;
}

const DashboardConfigModal: React.FC<DashboardConfigModalProps> = ({
  config,
  onSave,
  onClose
}) => {
  const [localConfig, setLocalConfig] = useState<DashboardConfig>(config);

  const handleWidgetToggle = (widget: keyof DashboardConfig['widgets']) => {
    setLocalConfig(prev => ({
      ...prev,
      widgets: {
        ...prev.widgets,
        [widget]: !prev.widgets[widget]
      }
    }));
  };

  const handleChartToggle = (chart: keyof DashboardConfig['charts']) => {
    setLocalConfig(prev => ({
      ...prev,
      charts: {
        ...prev.charts,
        [chart]: !prev.charts[chart]
      }
    }));
  };

  const handleLayoutChange = (layout: 'grid' | 'list') => {
    setLocalConfig(prev => ({
      ...prev,
      layout
    }));
  };

  const handleSave = () => {
    onSave(localConfig);
  };

  const handleReset = () => {
    setLocalConfig({
      widgets: {
        totalCampaigns: true,
        activeCampaigns: true,
        totalViews: true,
        conversions: true,
        totalSpend: true,
        totalClicks: true,
      },
      charts: {
        performanceChart: true,
        conversionChart: true,
        spendChart: true,
      },
      layout: 'grid',
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Configurar Dashboard</h2>
          <button className="close-button" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="modal-body">
          <div className="config-section">
            <h3>Widgets de Métricas</h3>
            <div className="widgets-grid">
              {Object.entries(localConfig.widgets).map(([key, enabled]) => (
                <label key={key} className="widget-toggle">
                  <input
                    type="checkbox"
                    checked={enabled}
                    onChange={() => handleWidgetToggle(key as keyof DashboardConfig['widgets'])}
                  />
                  <span className="widget-label">
                    {key === 'totalCampaigns' && 'Total Campañas'}
                    {key === 'activeCampaigns' && 'Campañas Activas'}
                    {key === 'totalViews' && 'Total Vistas'}
                    {key === 'conversions' && 'Conversiones'}
                    {key === 'totalSpend' && 'Gasto Total'}
                    {key === 'totalClicks' && 'Total Clicks'}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div className="config-section">
            <h3>Gráficos</h3>
            <div className="charts-grid">
              {Object.entries(localConfig.charts).map(([key, enabled]) => (
                <label key={key} className="chart-toggle">
                  <input
                    type="checkbox"
                    checked={enabled}
                    onChange={() => handleChartToggle(key as keyof DashboardConfig['charts'])}
                  />
                  <span className="chart-label">
                    {key === 'performanceChart' && (
                      <>
                        <TrendingUp size={16} />
                        Gráfico de Rendimiento
                      </>
                    )}
                    {key === 'conversionChart' && (
                      <>
                        <PieChart size={16} />
                        Gráfico de Conversiones
                      </>
                    )}
                    {key === 'spendChart' && (
                      <>
                        <BarChart3 size={16} />
                        Gráfico de Gastos
                      </>
                    )}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div className="config-section">
            <h3>Diseño</h3>
            <div className="layout-options">
              <label className="layout-option">
                <input
                  type="radio"
                  name="layout"
                  value="grid"
                  checked={localConfig.layout === 'grid'}
                  onChange={() => handleLayoutChange('grid')}
                />
                <span>Vista de Cuadrícula</span>
              </label>
              <label className="layout-option">
                <input
                  type="radio"
                  name="layout"
                  value="list"
                  checked={localConfig.layout === 'list'}
                  onChange={() => handleLayoutChange('list')}
                />
                <span>Vista de Lista</span>
              </label>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="reset-button" onClick={handleReset}>
            Restablecer
          </button>
          <div className="action-buttons">
            <button className="cancel-button" onClick={onClose}>
              Cancelar
            </button>
            <button className="save-button" onClick={handleSave}>
              Guardar Configuración
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardConfigModal;
