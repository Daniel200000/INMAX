import { Campaign, CampaignCreate, CampaignUpdate, CampaignStats, CampaignFilters } from '../types/campaign';
import { 
  getCampaigns, 
  getCampaignById, 
  addCampaign, 
  updateCampaign, 
  deleteCampaign,
  calculateRealStats 
} from './localStorage';
import api from './api';

export const campaignService = {
  async getCampaigns(filters?: CampaignFilters): Promise<{ campaigns: Campaign[]; total: number }> {
    try {
      // Try API first
      const response = await api.get('/campaigns', { params: filters });
      return response.data;
    } catch (error) {
      // Fallback to localStorage
      console.log('API not available, using localStorage');
      const allCampaigns = getCampaigns();
      
      let filteredCampaigns = allCampaigns;
      
      if (filters) {
        if (filters.status) {
          filteredCampaigns = filteredCampaigns.filter(c => c.status === filters.status);
        }
        if (filters.search) {
          const searchLower = filters.search.toLowerCase();
          filteredCampaigns = filteredCampaigns.filter(c => 
            c.name.toLowerCase().includes(searchLower) ||
            (c.description && c.description.toLowerCase().includes(searchLower))
          );
        }
      }
      
      const start = filters?.page ? (filters.page - 1) * (filters.limit || 10) : 0;
      const end = start + (filters?.limit || 10);
      
      return {
        campaigns: filteredCampaigns.slice(start, end),
        total: filteredCampaigns.length
      };
    }
  },

  async getCampaign(id: string): Promise<Campaign> {
    try {
      const response = await api.get(`/campaigns/${id}`);
      return response.data;
    } catch (error) {
      // Fallback to localStorage
      const campaign = getCampaignById(id);
      if (!campaign) {
        throw new Error('Campaign not found');
      }
      return campaign;
    }
  },

  async createCampaign(data: CampaignCreate): Promise<Campaign> {
    try {
      const response = await api.post('/campaigns', data);
      return response.data;
    } catch (error) {
      // Fallback to localStorage
      console.log('API not available, saving to localStorage');
      return addCampaign(data);
    }
  },

  async updateCampaign(id: string, data: CampaignUpdate): Promise<Campaign> {
    try {
      const response = await api.put(`/campaigns/${id}`, data);
      return response.data;
    } catch (error) {
      // Fallback to localStorage
      const updatedCampaign = updateCampaign(id, data);
      if (!updatedCampaign) {
        throw new Error('Campaign not found');
      }
      return updatedCampaign;
    }
  },

  async deleteCampaign(id: string): Promise<void> {
    try {
      await api.delete(`/campaigns/${id}`);
    } catch (error) {
      // Fallback to localStorage
      const deleted = deleteCampaign(id);
      if (!deleted) {
        throw new Error('Campaign not found');
      }
    }
  },

  async getCampaignStats(id: string): Promise<CampaignStats> {
    try {
      const response = await api.get(`/campaigns/${id}/stats`);
      return response.data;
    } catch (error) {
      // Fallback to localStorage
      const campaign = getCampaignById(id);
      if (!campaign) {
        throw new Error('Campaign not found');
      }
      return campaign.stats || {
        views: campaign.views_count || 0,
        clicks: campaign.clicks_count || 0,
        conversions: campaign.conversions_count || 0,
        spend: campaign.budget || 0,
      };
    }
  },

  async getDashboardStats(): Promise<{
    total_campaigns: number;
    active_campaigns: number;
    total_views: number;
    total_clicks: number;
    total_conversions: number;
    total_spent: number;
  }> {
    try {
      const response = await api.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      // Fallback to localStorage
      const stats = calculateRealStats();
      return {
        total_campaigns: stats.totalCampaigns.value,
        active_campaigns: stats.activeCampaigns.value,
        total_views: stats.totalViews.value,
        total_clicks: stats.totalClicks.value,
        total_conversions: stats.conversions.value,
        total_spent: stats.totalSpend.value,
      };
    }
  },
};
