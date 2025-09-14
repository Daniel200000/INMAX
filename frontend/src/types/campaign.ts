export interface Campaign {
  id: string;
  name: string;
  description?: string;
  budget: number;
  demographics?: Record<string, any>;
  channel: string;
  start_date: string;
  end_date: string;
  user_id: string;
  status: 'draft' | 'active' | 'paused' | 'finished' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  target_locations: GeoLocation[];
  media_files: string[];
  created_at: string;
  updated_at: string;
  createdAt?: string; // Para compatibilidad con localStorage
  updatedAt?: string; // Para compatibilidad con localStorage
  views_count: number;
  clicks_count: number;
  conversions_count: number;
  stats?: CampaignStats; // Para estadísticas en tiempo real
}

export interface CampaignCreate {
  name: string;
  description?: string;
  budget: number;
  demographics?: Record<string, any>;
  channel: string;
  start_date: string;
  end_date: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  target_locations?: GeoLocation[];
  media_files?: string[];
}

export interface CampaignUpdate {
  name?: string;
  description?: string;
  budget?: number;
  demographics?: Record<string, any>;
  channel?: string;
  start_date?: string;
  end_date?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  target_locations?: GeoLocation[];
  media_files?: string[];
}

export interface GeoLocation {
  type: 'point' | 'polygon' | 'circle' | 'country' | 'region';
  coordinates: [number, number];
  radius?: number;
  polygon_coordinates?: [number, number][];
  country?: string;
  region?: string;
  city?: string;
  address?: string;
}

export interface CampaignStats {
  campaign_id?: string;
  views: number;
  clicks: number;
  conversions: number;
  spend: number;
  ctr?: number;
  conversion_rate?: number;
  cost_per_click?: number;
  cost_per_conversion?: number;
  total_spent?: number;
  last_updated?: string;
}

export interface CampaignFilters {
  status?: string;
  search?: string;
  start_date?: string;
  end_date?: string;
  priority?: string;
  limit?: number;
  page?: number;
}
