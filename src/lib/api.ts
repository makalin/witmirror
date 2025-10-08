import type { AnalysisRequest, WisdomResponse, ApiStats, User } from './types';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Authentication
  async login(username: string, password: string) {
    return this.request<{ access_token: string; token_type: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async register(username: string, email: string, password: string) {
    return this.request<{ access_token: string; token_type: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  async getCurrentUser() {
    return this.request<User>('/auth/me');
  }

  async updatePreferences(preferences: Record<string, any>) {
    return this.request<User>('/auth/preferences', {
      method: 'PUT',
      body: JSON.stringify({ preferences }),
    });
  }

  // Analysis
  async analyzeComment(request: AnalysisRequest): Promise<WisdomResponse> {
    return this.request<WisdomResponse>('/analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async bulkAnalyze(texts: string[], platform: string = 'general', style: string = 'classic', ai_provider: string = 'openai') {
    return this.request<{ results: any[]; total: number; successful: number }>('/bulk/analyze', {
      method: 'POST',
      body: JSON.stringify({ texts, platform, style, ai_provider }),
    });
  }

  // Analytics
  async getAnalyticsSummary() {
    return this.request<ApiStats>('/analytics/summary');
  }

  async getDailyAnalytics(days: number = 30) {
    return this.request<any[]>('/analytics/daily', {
      method: 'GET',
    });
  }

  async getUserAnalytics(userId: number) {
    return this.request<any>(`/analytics/user/${userId}`);
  }

  async getTrendingEmotions(days: number = 7) {
    return this.request<any[]>('/analytics/trending');
  }

  // AI Providers
  async getAiProviders() {
    return this.request<{ providers: string[]; details: Record<string, any> }>('/ai/providers');
  }

  // Admin
  async getUsers(skip: number = 0, limit: number = 100) {
    return this.request<{ users: User[]; total: number }>(`/admin/users?skip=${skip}&limit=${limit}`);
  }

  async getAllAnalyses(skip: number = 0, limit: number = 100) {
    return this.request<{ analyses: any[]; total: number }>(`/admin/analyses?skip=${skip}&limit=${limit}`);
  }

  // Export
  async exportAnalytics(startDate?: string, endDate?: string, format: string = 'json') {
    return this.request<{ data: any; format: string }>('/export/analytics', {
      method: 'POST',
      body: JSON.stringify({ start_date: startDate, end_date: endDate, format }),
    });
  }

  // Health
  async healthCheck() {
    return this.request<{ status: string; timestamp: string; version: string }>('/health');
  }

  // Wisdom Styles
  async getWisdomStyles() {
    return this.request<any[]>('/wisdom/styles');
  }

  async getStyleTemplates(style: string) {
    return this.request<any[]>(`/wisdom/styles/${style}`);
  }

  async getStyleExamples(style: string) {
    return this.request<{ style: string; examples: string[] }>(`/wisdom/styles/${style}/examples`);
  }

  // Integrations
  async getRedditComments(subreddit: string, limit: number = 10) {
    return this.request<any[]>(`/integrations/reddit/${subreddit}?limit=${limit}`);
  }

  async getTwitterMentions(username: string, count: number = 10) {
    return this.request<any[]>(`/integrations/twitter/${username}?count=${count}`);
  }

  async analyzeSocialSentiment(platform: string, query: string, limit: number = 50) {
    return this.request<any>('/integrations/social-sentiment', {
      method: 'POST',
      body: JSON.stringify({ platform, query, limit }),
    });
  }

  async createDiscordWebhook(webhookUrl: string) {
    return this.request<any>('/integrations/discord/webhook', {
      method: 'POST',
      body: JSON.stringify({ webhook_url: webhookUrl }),
    });
  }

  async getIntegrationStats() {
    return this.request<any>('/integrations/stats');
  }

  // Comment History
  async getCommentHistory(limit: number = 50, offset: number = 0) {
    return this.request<any[]>(`/history?limit=${limit}&offset=${offset}`);
  }

  async getHistoryStats() {
    return this.request<any>('/history/stats');
  }

  async searchHistory(query: string, filters: any = {}) {
    return this.request<any[]>('/history/search', {
      method: 'POST',
      body: JSON.stringify({ query, filters }),
    });
  }

  async getFavoriteResponses(limit: number = 10) {
    return this.request<any[]>(`/history/favorites?limit=${limit}`);
  }

  async getTrendingTopics(days: number = 30) {
    return this.request<any[]>(`/history/trending?days=${days}`);
  }

  async exportHistory(format: string = 'json') {
    return this.request<any>(`/history/export?format=${format}`);
  }

  async deleteAnalysis(analysisId: number) {
    return this.request<{ success: boolean }>(`/history/${analysisId}`, {
      method: 'DELETE',
    });
  }

  async bulkDeleteAnalyses(analysisIds: number[]) {
    return this.request<{ deleted_count: number }>('/history/bulk', {
      method: 'DELETE',
      body: JSON.stringify({ analysis_ids: analysisIds }),
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);

// Legacy functions for backward compatibility
export async function analyzeComment(request: AnalysisRequest): Promise<WisdomResponse> {
  return apiClient.analyzeComment(request);
}

export async function getStats(): Promise<ApiStats> {
  return apiClient.getAnalyticsSummary();
}

export async function healthCheck(): Promise<boolean> {
  try {
    const response = await apiClient.healthCheck();
    return response.status === 'healthy';
  } catch {
    return false;
  }
}