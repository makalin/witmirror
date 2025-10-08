<script lang="ts">
  import { onMount } from 'svelte';
  import { apiClient } from '$lib/api';
  import { authStore } from '$lib/auth';
  import { goto } from '$app/navigation';
  import { 
    Clock, 
    Search, 
    Filter, 
    Download, 
    Trash2, 
    Star,
    TrendingUp,
    BarChart3,
    Calendar,
    MessageSquare
  } from 'lucide-svelte';
  import type { AnalysisHistory } from '$lib/types';

  let history: AnalysisHistory[] = [];
  let stats: any = null;
  let trendingTopics: any[] = [];
  let favorites: AnalysisHistory[] = [];
  let isLoading = true;
  let error = '';
  let searchQuery = '';
  let selectedFilters = {
    sentiment: '',
    platform: '',
    style: '',
    date_from: '',
    date_to: ''
  };
  let currentView = 'all'; // 'all', 'favorites', 'trending'
  let selectedAnalyses: number[] = [];

  onMount(async () => {
    // Check authentication
    authStore.subscribe((state) => {
      if (!state.isAuthenticated && !state.isLoading) {
        goto('/login');
      }
    });

    await loadHistory();
  });

  async function loadHistory() {
    try {
      isLoading = true;
      const [historyData, statsData, trendingData, favoritesData] = await Promise.all([
        apiClient.getCommentHistory(50, 0),
        apiClient.getHistoryStats(),
        apiClient.getTrendingTopics(30),
        apiClient.getFavoriteResponses(10)
      ]);
      
      history = historyData;
      stats = statsData;
      trendingTopics = trendingData;
      favorites = favoritesData;
    } catch (err: any) {
      error = err.message || 'Failed to load history';
    } finally {
      isLoading = false;
    }
  }

  async function searchHistory() {
    try {
      const results = await apiClient.searchHistory(searchQuery, selectedFilters);
      history = results;
    } catch (err: any) {
      error = err.message || 'Search failed';
    }
  }

  async function deleteAnalysis(analysisId: number) {
    if (!confirm('Are you sure you want to delete this analysis?')) return;
    
    try {
      await apiClient.deleteAnalysis(analysisId);
      history = history.filter(h => h.id !== analysisId);
    } catch (err: any) {
      error = err.message || 'Failed to delete analysis';
    }
  }

  async function bulkDelete() {
    if (selectedAnalyses.length === 0) return;
    if (!confirm(`Delete ${selectedAnalyses.length} analyses?`)) return;
    
    try {
      await apiClient.bulkDeleteAnalyses(selectedAnalyses);
      history = history.filter(h => !selectedAnalyses.includes(h.id));
      selectedAnalyses = [];
    } catch (err: any) {
      error = err.message || 'Bulk delete failed';
    }
  }

  async function exportHistory() {
    try {
      const data = await apiClient.exportHistory('json');
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `witmirror-history-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err: any) {
      error = err.message || 'Export failed';
    }
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString();
  }

  function getSentimentColor(sentiment: string) {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }

  function toggleSelection(analysisId: number) {
    if (selectedAnalyses.includes(analysisId)) {
      selectedAnalyses = selectedAnalyses.filter(id => id !== analysisId);
    } else {
      selectedAnalyses = [...selectedAnalyses, analysisId];
    }
  }
</script>

<svelte:head>
  <title>Comment History — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100">
  <!-- Header -->
  <header class="bg-white shadow-sm border-b border-wisdom-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-wisdom-100 rounded-lg">
            <Clock class="w-6 h-6 text-wisdom-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-wisdom-900">Comment History</h1>
            <p class="text-sm text-wisdom-600">Your wisdom generation history and insights</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <button
            on:click={exportHistory}
            class="flex items-center space-x-2 px-4 py-2 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
          >
            <Download class="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if isLoading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
        <span class="ml-3 text-wisdom-700">Loading history...</span>
      </div>
    {:else if error}
      <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <div class="text-red-600 mb-2">⚠️</div>
        <h3 class="font-semibold text-red-900 mb-2">Error Loading History</h3>
        <p class="text-red-700">{error}</p>
      </div>
    {:else}
      <!-- Stats Overview -->
      {#if stats}
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
                <MessageSquare class="w-5 h-5 text-wisdom-600" />
              </div>
              <span class="text-2xl font-bold text-wisdom-800">{stats.total_analyses}</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Total Analyses</h3>
            <p class="text-sm text-wisdom-600">All time</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <BarChart3 class="w-5 h-5 text-green-600" />
              </div>
              <span class="text-2xl font-bold text-green-600">{stats.avg_confidence}%</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Avg Confidence</h3>
            <p class="text-sm text-wisdom-600">Analysis accuracy</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <TrendingUp class="w-5 h-5 text-blue-600" />
              </div>
              <span class="text-2xl font-bold text-blue-600">{stats.avg_toxicity}%</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Avg Toxicity</h3>
            <p class="text-sm text-wisdom-600">Detected negativity</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Star class="w-5 h-5 text-purple-600" />
              </div>
              <span class="text-2xl font-bold text-purple-600">{favorites.length}</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Favorites</h3>
            <p class="text-sm text-wisdom-600">High-confidence responses</p>
          </div>
        </div>
      {/if}

      <!-- Navigation Tabs -->
      <div class="mb-8">
        <nav class="flex space-x-8">
          <button
            on:click={() => currentView = 'all'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentView === 'all' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            All History ({history.length})
          </button>
          <button
            on:click={() => currentView = 'favorites'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentView === 'favorites' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Favorites ({favorites.length})
          </button>
          <button
            on:click={() => currentView = 'trending'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentView === 'trending' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Trending Topics
          </button>
        </nav>
      </div>

      <!-- Search and Filters -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <div class="relative">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-wisdom-400" />
              <input
                type="text"
                bind:value={searchQuery}
                placeholder="Search your history..."
                class="w-full pl-10 pr-4 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div class="flex gap-2">
            <select
              bind:value={selectedFilters.sentiment}
              class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="">All Sentiments</option>
              <option value="positive">Positive</option>
              <option value="negative">Negative</option>
              <option value="neutral">Neutral</option>
            </select>
            
            <select
              bind:value={selectedFilters.platform}
              class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="">All Platforms</option>
              <option value="reddit">Reddit</option>
              <option value="twitter">Twitter</option>
              <option value="general">General</option>
            </select>
            
            <button
              on:click={searchHistory}
              class="px-4 py-2 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      <!-- Content based on current view -->
      {#if currentView === 'all'}
        <!-- All History -->
        <div class="bg-white rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-wisdom-200 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-wisdom-900">All Analyses</h3>
            {#if selectedAnalyses.length > 0}
              <button
                on:click={bulkDelete}
                class="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                <Trash2 class="w-4 h-4" />
                <span>Delete Selected ({selectedAnalyses.length})</span>
              </button>
            {/if}
          </div>
          
          <div class="divide-y divide-wisdom-100">
            {#each history as analysis}
              <div class="p-6 hover:bg-wisdom-50 transition-colors">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-2">
                      <input
                        type="checkbox"
                        checked={selectedAnalyses.includes(analysis.id)}
                        on:change={() => toggleSelection(analysis.id)}
                        class="rounded border-wisdom-300"
                      />
                      <span class="text-sm text-wisdom-500">{formatDate(analysis.created_at)}</span>
                      <span class="px-2 py-1 text-xs rounded-full {getSentimentColor(analysis.sentiment)}">
                        {analysis.sentiment}
                      </span>
                      <span class="text-sm text-wisdom-600 capitalize">{analysis.platform}</span>
                    </div>
                    
                    <p class="text-wisdom-900 mb-2 font-medium">"{analysis.original_text}"</p>
                    <p class="text-wisdom-700 italic">"{analysis.wisdom_response}"</p>
                    
                    <div class="flex items-center space-x-4 mt-3 text-sm text-wisdom-600">
                      <span>Confidence: {Math.round(analysis.confidence * 100)}%</span>
                      <span>Style: {analysis.style}</span>
                      <span>Model: {analysis.model_used}</span>
                    </div>
                  </div>
                  
                  <button
                    on:click={() => deleteAnalysis(analysis.id)}
                    class="ml-4 p-2 text-red-600 hover:text-red-800 hover:bg-red-100 rounded-lg transition-colors"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {:else if currentView === 'favorites'}
        <!-- Favorites -->
        <div class="bg-white rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-wisdom-200">
            <h3 class="text-lg font-semibold text-wisdom-900">Favorite Responses</h3>
            <p class="text-sm text-wisdom-600">Your most effective wisdom responses</p>
          </div>
          
          <div class="divide-y divide-wisdom-100">
            {#each favorites as analysis}
              <div class="p-6">
                <div class="flex items-start space-x-3">
                  <Star class="w-5 h-5 text-yellow-500 mt-1" />
                  <div class="flex-1">
                    <p class="text-wisdom-900 mb-2 font-medium">"{analysis.original_text}"</p>
                    <p class="text-wisdom-700 italic mb-3">"{analysis.wisdom_response}"</p>
                    
                    <div class="flex items-center space-x-4 text-sm text-wisdom-600">
                      <span>Confidence: {Math.round(analysis.confidence * 100)}%</span>
                      <span>Style: {analysis.style}</span>
                      <span>Platform: {analysis.platform}</span>
                      <span>{formatDate(analysis.created_at)}</span>
                    </div>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {:else if currentView === 'trending'}
        <!-- Trending Topics -->
        <div class="bg-white rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-wisdom-200">
            <h3 class="text-lg font-semibold text-wisdom-900">Trending Topics</h3>
            <p class="text-sm text-wisdom-600">Most discussed topics in your analyses</p>
          </div>
          
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              {#each trendingTopics as topic}
                <div class="flex items-center justify-between p-3 bg-wisdom-50 rounded-lg">
                  <span class="text-wisdom-700">{topic.topic}</span>
                  <span class="text-sm font-semibold text-wisdom-600">{topic.frequency}</span>
                </div>
              {/each}
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </main>
</div>
