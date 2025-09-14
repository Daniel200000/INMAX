import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './PerformanceChart.css';

const PerformanceChart: React.FC = () => {
  // Datos de ejemplo para el gráfico
  const data = [
    { name: 'Ene', views: 4000, clicks: 2400, conversions: 240 },
    { name: 'Feb', views: 3000, clicks: 1398, conversions: 221 },
    { name: 'Mar', views: 2000, clicks: 9800, conversions: 229 },
    { name: 'Abr', views: 2780, clicks: 3908, conversions: 200 },
    { name: 'May', views: 1890, clicks: 4800, conversions: 218 },
    { name: 'Jun', views: 2390, clicks: 3800, conversions: 250 },
    { name: 'Jul', views: 3490, clicks: 4300, conversions: 210 },
  ];

  return (
    <div className="performance-chart">
      <div className="chart-header">
        <h3>Rendimiento de Campañas</h3>
        <div className="chart-legend">
          <div className="legend-item">
            <div className="legend-color views"></div>
            <span>Vistas</span>
          </div>
          <div className="legend-item">
            <div className="legend-color clicks"></div>
            <span>Clicks</span>
          </div>
          <div className="legend-item">
            <div className="legend-color conversions"></div>
            <span>Conversiones</span>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="name" 
              stroke="#64748b"
              fontSize={12}
            />
            <YAxis 
              stroke="#64748b"
              fontSize={12}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="views" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="clicks" 
              stroke="#8b5cf6" 
              strokeWidth={2}
              dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="conversions" 
              stroke="#10b981" 
              strokeWidth={2}
              dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PerformanceChart;
