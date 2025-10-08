<script lang="ts">
  import { onMount } from 'svelte';
  import { apiClient } from '$lib/api';
  import { authStore } from '$lib/auth';
  import { goto } from '$app/navigation';
  import { 
    BarChart3, 
    TrendingUp, 
    Users, 
    Brain, 
    Activity,
    Clock,
    Zap,
    PieChart,
    Calendar
  } from 'lucide-svelte';
  import type { ApiStats, DailyAnalytics, TrendingEmotion } from '$lib/types';

  let stats: ApiStats | null = null;
  let dailyStats: DailyAnalytics[] = [];
  let trendingEmotions: TrendingEmotion[] = [];
  let isLoading = true;
  let error = '';
  let selectedDays = 30;

  onMount(async () => {
    // Check authentication
    authStore.subscribe((state) => {
      if (!state.isAuthenticated && !state.isLoading) {
        goto('/login');
      }
    });

    await loadAnalytics();
  });

  async function loadAnalytics() {
    try {
      isLoading = true;
      const [summary, daily, trending] = await Promise.all([
        apiClient.getAnalyticsSummary(),
        apiClient.getDailyAnalytics(selectedDays),
        apiClient.getTrendingEmotions(7)
      ]);
      
      stats = summary;
      dailyStats = daily;
      trendingEmotions = trending;
    } catch (err: any) {
      error = err.message || 'Failed to load analytics';
    } finally {
      isLoading = false;
    }
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString();
  }

  function formatNumber(num: number) {
    return num.toLocaleString();
  }
</script>

<svelte:head>
  <title>Analytics — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100">
  <!-- Header -->
  <header class="bg-white shadow-sm border-b border-wisdom-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-wisdom-100 rounded-lg">
            <BarChart3 class="w-6 h-6 text-wisdom-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-wisdom-900">Analytics Dashboard</h1>
            <p class="text-sm text-wisdom-600">Comprehensive usage insights and metrics</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <select
            bind:value={selectedDays}
            on:change={loadAnalytics}
            class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if isLoading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
        <span class="ml-3 text-wisdom-700">Loading analytics...</span>
      </div>
    {:else if error}
      <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <div class="text-red-600 mb-2">⚠️</div>
        <h3 class="font-semibold text-red-900 mb-2">Error Loading Analytics</h3>
        <p class="text-red-700">{error}</p>
      </div>
    {:else}
      <!-- Key Metrics -->
      {#if stats}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
                <Activity class="w-5 h-5 text-wisdom-600" />
              </div>
              <span class="text-2xl font-bold text-wisdom-800">{formatNumber(stats.total_requests)}</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Total Requests</h3>
            <p class="text-sm text-wisdom-600">All time analyses</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <TrendingUp class="w-5 h-5 text-green-600" />
              </div>
              <span class="text-2xl font-bold text-green-600">{Math.round(stats.success_rate)}%</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Success Rate</h3>
            <p class="text-sm text-wisdom-600">Successful analyses</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Zap class="w-5 h-5 text-blue-600" />
              </div>
              <span class="text-2xl font-bold text-blue-600">{stats.avg_processing_time}ms</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Avg Response Time</h3>
            <p class="text-sm text-wisdom-600">Processing speed</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Brain class="w-5 h-5 text-purple-600" />
              </div>
              <span class="text-2xl font-bold text-purple-600">
                {Object.keys(stats.top_emotions).length}
              </span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Emotions Detected</h3>
            <p class="text-sm text-wisdom-600">Unique emotions</p>
          </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Sentiment Distribution -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <PieChart class="w-5 h-5 mr-2" />
              Sentiment Distribution
            </h3>
            <div class="space-y-3">
              {#each Object.entries(stats.sentiment_distribution) as [sentiment, count]}
                <div class="flex items-center justify-between">
                  <span class="text-wisdom-700 capitalize">{sentiment}</span>
                  <div class="flex items-center space-x-3">
                    <div class="w-32 bg-wisdom-100 rounded-full h-2">
                      <div 
                        class="bg-wisdom-600 h-2 rounded-full" 
                        style="width: {(count / stats.total_requests) * 100}%"
                      ></div>
                    </div>
                    <span class="text-sm text-wisdom-600 w-12 text-right">{count}</span>
                  </div>
                </div>
              {/each}
            </div>
          </div>

          <!-- Platform Usage -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <Users class="w-5 h-5 mr-2" />
              Platform Usage
            </h3>
            <div class="space-y-3">
              {#each Object.entries(stats.platform_usage) as [platform, count]}
                <div class="flex items-center justify-between">
                  <span class="text-wisdom-700 capitalize">{platform}</span>
                  <div class="flex items-center space-x-3">
                    <div class="w-32 bg-wisdom-100 rounded-full h-2">
                      <div 
                        class="bg-wisdom-600 h-2 rounded-full" 
                        style="width: {(count / stats.total_requests) * 100}%"
                      ></div>
                    </div>
                    <span class="text-sm text-wisdom-600 w-12 text-right">{count}</span>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        </div>

        <!-- Trending Emotions -->
        {#if trendingEmotions.length > 0}
          <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <TrendingUp class="w-5 h-5 mr-2" />
              Trending Emotions (Last 7 Days)
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {#each trendingEmotions.slice(0, 6) as emotion}
                <div class="flex items-center justify-between p-3 bg-wisdom-50 rounded-lg">
                  <span class="text-wisdom-700 capitalize">{emotion.emotion}</span>
                  <span class="text-sm font-semibold text-wisdom-600">{emotion.count}</span>
                </div>
              {/each}
            </div>
          </div>
        {/if}

        <!-- Daily Activity -->
        {#if dailyStats.length > 0}
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <Calendar class="w-5 h-5 mr-2" />
              Daily Activity (Last {selectedDays} Days)
            </h3>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-wisdom-200">
                    <th class="text-left py-3 px-4 font-semibold text-wisdom-900">Date</th>
                    <th class="text-right py-3 px-4 font-semibold text-wisdom-900">Requests</th>
                    <th class="text-right py-3 px-4 font-semibold text-wisdom-900">Success Rate</th>
                    <th class="text-right py-3 px-4 font-semibold text-wisdom-900">Avg Time</th>
                  </tr>
                </thead>
                <tbody>
                  {#each dailyStats.slice(0, 10) as day}
                    <tr class="border-b border-wisdom-100">
                      <td class="py-3 px-4 text-wisdom-700">{formatDate(day.date)}</td>
                      <td class="py-3 px-4 text-right text-wisdom-700">{formatNumber(day.total_requests)}</td>
                      <td class="py-3 px-4 text-right text-wisdom-700">
                        {Math.round((day.successful_requests / day.total_requests) * 100)}%
                      </td>
                      <td class="py-3 px-4 text-right text-wisdom-700">{day.avg_processing_time}ms</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        {/if}
      {/if}
    {/if}
  </main>
</div>
