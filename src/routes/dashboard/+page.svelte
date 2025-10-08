<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/auth';
  import { apiClient } from '$lib/api';
  import { goto } from '$app/navigation';
  import { 
    BarChart3, 
    TrendingUp, 
    Users, 
    Brain, 
    Settings, 
    LogOut,
    Sparkles,
    Activity,
    Clock,
    Zap
  } from 'lucide-svelte';
  import type { ApiStats, User } from '$lib/types';

  let user: User | null = null;
  let stats: ApiStats | null = null;
  let isLoading = true;
  let error = '';

  onMount(async () => {
    // Check authentication
    authStore.subscribe((state) => {
      if (!state.isAuthenticated && !state.isLoading) {
        goto('/login');
      }
      if (state.user) {
        user = state.user;
      }
    });

    // Load dashboard data
    try {
      const [statsData] = await Promise.all([
        apiClient.getAnalyticsSummary()
      ]);
      stats = statsData;
    } catch (err: any) {
      error = err.message || 'Failed to load dashboard data';
    } finally {
      isLoading = false;
    }
  });

  function logout() {
    authStore.logout();
    goto('/');
  }
</script>

<svelte:head>
  <title>Dashboard — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100">
  <!-- Header -->
  <header class="bg-white shadow-sm border-b border-wisdom-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-wisdom-100 rounded-lg">
            <Brain class="w-6 h-6 text-wisdom-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-wisdom-900">WitMirror Pro</h1>
            <p class="text-sm text-wisdom-600">Welcome back, {user?.username}</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <button
            on:click={() => goto('/settings')}
            class="p-2 text-wisdom-600 hover:text-wisdom-900 hover:bg-wisdom-100 rounded-lg transition-colors"
            title="Settings"
          >
            <Settings class="w-5 h-5" />
          </button>
          <button
            on:click={logout}
            class="p-2 text-wisdom-600 hover:text-wisdom-900 hover:bg-wisdom-100 rounded-lg transition-colors"
            title="Logout"
          >
            <LogOut class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if isLoading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
        <span class="ml-3 text-wisdom-700">Loading dashboard...</span>
      </div>
    {:else if error}
      <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <div class="text-red-600 mb-2">⚠️</div>
        <h3 class="font-semibold text-red-900 mb-2">Error Loading Dashboard</h3>
        <p class="text-red-700">{error}</p>
      </div>
    {:else}
      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <a
          href="/"
          class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow border border-wisdom-200"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
              <Sparkles class="w-5 h-5 text-wisdom-600" />
            </div>
            <h3 class="font-semibold text-wisdom-900">Generate Wisdom</h3>
          </div>
          <p class="text-sm text-wisdom-600">Analyze comments and generate wise responses</p>
        </a>

        <a
          href="/analytics"
          class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow border border-wisdom-200"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
              <BarChart3 class="w-5 h-5 text-wisdom-600" />
            </div>
            <h3 class="font-semibold text-wisdom-900">Analytics</h3>
          </div>
          <p class="text-sm text-wisdom-600">View detailed usage statistics and insights</p>
        </a>

        <a
          href="/history"
          class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow border border-wisdom-200"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
              <Clock class="w-5 h-5 text-wisdom-600" />
            </div>
            <h3 class="font-semibold text-wisdom-900">History</h3>
          </div>
          <p class="text-sm text-wisdom-600">View your analysis history and saved responses</p>
        </a>
      </div>

      <!-- Stats Overview -->
      {#if stats}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
                <Activity class="w-5 h-5 text-wisdom-600" />
              </div>
              <span class="text-2xl font-bold text-wisdom-800">{stats.total_requests.toLocaleString()}</span>
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
                <Users class="w-5 h-5 text-purple-600" />
              </div>
              <span class="text-2xl font-bold text-purple-600">
                {Object.keys(stats.sentiment_distribution).length}
              </span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Sentiment Types</h3>
            <p class="text-sm text-wisdom-600">Detected emotions</p>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-semibold text-wisdom-900 mb-4">Platform Usage</h3>
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
      {/if}
    {/if}
  </main>
</div>
