import { Campaign, CampaignCreate, CampaignUpdate } from '../types/campaign';

const CAMPAIGNS_KEY = 'inmax_campaigns';
const DASHBOARD_CONFIG_KEY = 'inmax_dashboard_config';

export interface DashboardConfig {
  widgets: {
    totalCampaigns: boolean;
    activeCampaigns: boolean;
    totalViews: boolean;
    conversions: boolean;
    totalSpend: boolean;
    totalClicks: boolean;
  };
  charts: {
    performanceChart: boolean;
    conversionChart: boolean;
    spendChart: boolean;
  };
  layout: 'grid' | 'list';
}

export const defaultDashboardConfig: DashboardConfig = {
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
};

// Campaign Management
export const getCampaigns = (): Campaign[] => {
  try {
    const campaigns = localStorage.getItem(CAMPAIGNS_KEY);
    return campaigns ? JSON.parse(campaigns) : [];
  } catch (error) {
    console.error('Error loading campaigns:', error);
    return [];
  }
};

export const saveCampaigns = (campaigns: Campaign[]): void => {
  try {
    localStorage.setItem(CAMPAIGNS_KEY, JSON.stringify(campaigns));
  } catch (error) {
    console.error('Error saving campaigns:', error);
  }
};

export const addCampaign = (campaignData: CampaignCreate): Campaign => {
  const campaigns = getCampaigns();
  const newCampaign: Campaign = {
    id: Date.now().toString(),
    ...campaignData,
    status: 'draft',
    user_id: '1', // Mock user ID
    priority: campaignData.priority || 'medium',
    target_locations: campaignData.target_locations || [],
    media_files: campaignData.media_files || [],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    views_count: 0,
    clicks_count: 0,
    conversions_count: 0,
    stats: {
      views: 0,
      clicks: 0,
      conversions: 0,
      spend: 0,
    },
  };
  
  campaigns.push(newCampaign);
  saveCampaigns(campaigns);
  return newCampaign;
};

export const updateCampaign = (id: string, updates: CampaignUpdate): Campaign | null => {
  const campaigns = getCampaigns();
  const index = campaigns.findIndex(c => c.id === id);
  
  if (index === -1) return null;
  
  campaigns[index] = {
    ...campaigns[index],
    ...updates,
    updated_at: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  
  saveCampaigns(campaigns);
  return campaigns[index];
};

export const deleteCampaign = (id: string): boolean => {
  const campaigns = getCampaigns();
  const filteredCampaigns = campaigns.filter(c => c.id !== id);
  
  if (filteredCampaigns.length === campaigns.length) return false;
  
  saveCampaigns(filteredCampaigns);
  return true;
};

export const getCampaignById = (id: string): Campaign | null => {
  const campaigns = getCampaigns();
  return campaigns.find(c => c.id === id) || null;
};

// Dashboard Configuration
export const getDashboardConfig = (): DashboardConfig => {
  try {
    const config = localStorage.getItem(DASHBOARD_CONFIG_KEY);
    return config ? JSON.parse(config) : defaultDashboardConfig;
  } catch (error) {
    console.error('Error loading dashboard config:', error);
    return defaultDashboardConfig;
  }
};

export const saveDashboardConfig = (config: DashboardConfig): void => {
  try {
    localStorage.setItem(DASHBOARD_CONFIG_KEY, JSON.stringify(config));
  } catch (error) {
    console.error('Error saving dashboard config:', error);
  }
};

// Real-time stats calculation
export const calculateRealStats = () => {
  const campaigns = getCampaigns();
  
  const totalCampaigns = campaigns.length;
  const activeCampaigns = campaigns.filter(c => c.status === 'active').length;
  
  const totalViews = campaigns.reduce((sum, c) => sum + (c.stats?.views || c.views_count || 0), 0);
  const totalClicks = campaigns.reduce((sum, c) => sum + (c.stats?.clicks || c.clicks_count || 0), 0);
  const totalConversions = campaigns.reduce((sum, c) => sum + (c.stats?.conversions || c.conversions_count || 0), 0);
  const totalSpend = campaigns.reduce((sum, c) => sum + (c.stats?.spend || c.budget || 0), 0);
  
  // Calculate percentage changes (mock for now, in real app would compare with previous period)
  const calculatePercentageChange = (current: number) => {
    const previous = Math.max(0, current - Math.floor(Math.random() * current * 0.3));
    return previous > 0 ? Math.round(((current - previous) / previous) * 100) : 0;
  };
  
  return {
    totalCampaigns: {
      value: totalCampaigns,
      change: calculatePercentageChange(totalCampaigns),
    },
    activeCampaigns: {
      value: activeCampaigns,
      change: calculatePercentageChange(activeCampaigns),
    },
    totalViews: {
      value: totalViews,
      change: calculatePercentageChange(totalViews),
    },
    totalClicks: {
      value: totalClicks,
      change: calculatePercentageChange(totalClicks),
    },
    conversions: {
      value: totalConversions,
      change: calculatePercentageChange(totalConversions),
    },
    totalSpend: {
      value: totalSpend,
      change: calculatePercentageChange(totalSpend),
    },
  };
};
