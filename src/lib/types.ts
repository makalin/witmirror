export interface AnalysisRequest {
  text: string;
  platform?: string;
  style?: string;
  ai_provider?: string;
  user_id?: number;
}

export interface EmotionAnalysis {
  sentiment: 'negative' | 'neutral' | 'positive';
  confidence: number;
  detected_emotions: string[];
  toxicity_score: number;
}

export interface WisdomResponse {
  analysis: EmotionAnalysis;
  wisdom: string;
  style: string;
  platform: string;
  ai_provider: string;
  processing_time: number;
  model_used: string;
}

export interface ApiStats {
  total_requests: number;
  successful_requests: number;
  failed_requests: number;
  success_rate: number;
  avg_processing_time: number;
  sentiment_distribution: Record<string, number>;
  top_emotions: Record<string, number>;
  platform_usage: Record<string, number>;
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  last_login?: string;
  preferences: Record<string, any>;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface BulkAnalysisRequest {
  texts: string[];
  platform?: string;
  style?: string;
  ai_provider?: string;
}

export interface BulkAnalysisResult {
  results: Array<{
    text: string;
    analysis?: EmotionAnalysis;
    wisdom?: string;
    style?: string;
    platform?: string;
    ai_provider?: string;
    model_used?: string;
    error?: string;
  }>;
  total: number;
  successful: number;
}

export interface AiProvider {
  name: string;
  model: string;
  max_tokens: number;
  temperature: number;
}

export interface AiProvidersResponse {
  providers: string[];
  details: Record<string, AiProvider>;
}

export interface DailyAnalytics {
  date: string;
  total_requests: number;
  successful_requests: number;
  failed_requests: number;
  avg_processing_time: number;
  unique_users: number;
  top_emotions: Record<string, number>;
  platform_usage: Record<string, number>;
}

export interface UserAnalytics {
  total_analyses: number;
  avg_confidence: number;
  avg_toxicity: number;
  sentiment_distribution: Record<string, number>;
  style_preferences: Record<string, number>;
  first_analysis: string;
  last_analysis: string;
}

export interface TrendingEmotion {
  emotion: string;
  count: number;
}

export interface ExportRequest {
  start_date?: string;
  end_date?: string;
  format: 'json' | 'csv';
}

export interface ExportResponse {
  data: any;
  format: string;
}

export type WisdomStyle = 'classic' | 'stoic' | 'zen' | 'sufi' | 'sarcastic' | 'poetic' | 'scientific' | 'humorous';
export type Platform = 'reddit' | 'twitter' | 'facebook' | 'instagram' | 'youtube' | 'general';
export type AiProviderType = 'openai' | 'anthropic' | 'ollama' | 'fallback';
export type Sentiment = 'negative' | 'neutral' | 'positive';

export interface AnalysisHistory {
  id: number;
  original_text: string;
  sentiment: Sentiment;
  confidence: number;
  detected_emotions: string[];
  toxicity_score: number;
  wisdom_response: string;
  style: WisdomStyle;
  platform: Platform;
  model_used: string;
  processing_time: number;
  created_at: string;
}

export interface UserPreferences {
  default_style: WisdomStyle;
  default_platform: Platform;
  default_ai_provider: AiProviderType;
  notifications: {
    email: boolean;
    push: boolean;
  };
  privacy: {
    save_history: boolean;
    share_analytics: boolean;
  };
  display: {
    theme: 'light' | 'dark' | 'auto';
    language: string;
  };
}