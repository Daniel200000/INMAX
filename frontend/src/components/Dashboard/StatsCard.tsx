import React from 'react';
import { LucideIcon } from 'lucide-react';
import './StatsCard.css';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  color: string;
  change?: string;
}

const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon: Icon,
  color,
  change
}) => {
  return (
    <div className="stats-card">
      <div className="stats-card-header">
        <div className="stats-icon" style={{ backgroundColor: color + '20', color }}>
          <Icon size={24} />
        </div>
        {change && (
          <span className={`stats-change ${change.startsWith('+') ? 'positive' : 'negative'}`}>
            {change}
          </span>
        )}
      </div>
      
      <div className="stats-content">
        <h3 className="stats-title">{title}</h3>
        <p className="stats-value">{value}</p>
      </div>
    </div>
  );
};

export default StatsCard;
