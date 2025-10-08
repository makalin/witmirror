<script lang="ts">
  import { onMount } from 'svelte';
  import { apiClient } from '$lib/api';
  import { authStore } from '$lib/auth';
  import { goto } from '$app/navigation';
  import { 
    Shield, 
    Users, 
    BarChart3, 
    Settings,
    Activity,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Clock,
    Database
  } from 'lucide-svelte';
  import type { User, ApiStats } from '$lib/types';

  let users: User[] = [];
  let analyses: any[] = [];
  let stats: ApiStats | null = null;
  let isLoading = true;
  let error = '';
  let currentTab = 'overview';

  onMount(async () => {
    // Check authentication and admin status
    authStore.subscribe((state) => {
      if (!state.isAuthenticated && !state.isLoading) {
        goto('/login');
      } else if (state.user && !state.user.is_admin) {
        goto('/dashboard');
      }
    });

    await loadAdminData();
  });

  async function loadAdminData() {
    try {
      isLoading = true;
      const [usersData, analysesData, statsData] = await Promise.all([
        apiClient.getUsers(0, 50),
        apiClient.getAllAnalyses(0, 50),
        apiClient.getAnalyticsSummary()
      ]);
      
      users = usersData.users;
      analyses = analysesData.analyses;
      stats = statsData;
    } catch (err: any) {
      error = err.message || 'Failed to load admin data';
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
  <title>Admin Dashboard — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100">
  <!-- Header -->
  <header class="bg-white shadow-sm border-b border-wisdom-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-red-100 rounded-lg">
            <Shield class="w-6 h-6 text-red-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-wisdom-900">Admin Dashboard</h1>
            <p class="text-sm text-wisdom-600">System administration and monitoring</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <button
            on:click={() => goto('/dashboard')}
            class="px-4 py-2 text-wisdom-600 hover:text-wisdom-900 hover:bg-wisdom-100 rounded-lg transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if isLoading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
        <span class="ml-3 text-wisdom-700">Loading admin data...</span>
      </div>
    {:else if error}
      <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <div class="text-red-600 mb-2">⚠️</div>
        <h3 class="font-semibold text-red-900 mb-2">Error Loading Admin Data</h3>
        <p class="text-red-700">{error}</p>
      </div>
    {:else}
      <!-- Tab Navigation -->
      <div class="mb-8">
        <nav class="flex space-x-8">
          <button
            on:click={() => currentTab = 'overview'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentTab === 'overview' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Overview
          </button>
          <button
            on:click={() => currentTab = 'users'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentTab === 'users' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Users
          </button>
          <button
            on:click={() => currentTab = 'analyses'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentTab === 'analyses' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Analyses
          </button>
          <button
            on:click={() => currentTab = 'system'}
            class="py-2 px-1 border-b-2 font-medium text-sm {currentTab === 'system' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            System
          </button>
        </nav>
      </div>

      <!-- Overview Tab -->
      {#if currentTab === 'overview'}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
                <Users class="w-5 h-5 text-wisdom-600" />
              </div>
              <span class="text-2xl font-bold text-wisdom-800">{users.length}</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Total Users</h3>
            <p class="text-sm text-wisdom-600">Registered accounts</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Activity class="w-5 h-5 text-green-600" />
              </div>
              <span class="text-2xl font-bold text-green-600">{stats ? formatNumber(stats.total_requests) : '0'}</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Total Requests</h3>
            <p class="text-sm text-wisdom-600">All time analyses</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <CheckCircle class="w-5 h-5 text-blue-600" />
              </div>
              <span class="text-2xl font-bold text-blue-600">{stats ? Math.round(stats.success_rate) : 0}%</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Success Rate</h3>
            <p class="text-sm text-wisdom-600">System reliability</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Clock class="w-5 h-5 text-purple-600" />
              </div>
              <span class="text-2xl font-bold text-purple-600">{stats ? stats.avg_processing_time : 0}ms</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Avg Response Time</h3>
            <p class="text-sm text-wisdom-600">Performance metric</p>
          </div>
        </div>

        <!-- System Status -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <Database class="w-5 h-5 mr-2" />
              System Status
            </h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">API Status</span>
                <div class="flex items-center space-x-2">
                  <CheckCircle class="w-4 h-4 text-green-500" />
                  <span class="text-sm text-green-600">Operational</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Database</span>
                <div class="flex items-center space-x-2">
                  <CheckCircle class="w-4 h-4 text-green-500" />
                  <span class="text-sm text-green-600">Connected</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">AI Services</span>
                <div class="flex items-center space-x-2">
                  <CheckCircle class="w-4 h-4 text-green-500" />
                  <span class="text-sm text-green-600">Available</span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <BarChart3 class="w-5 h-5 mr-2" />
              Recent Activity
            </h3>
            <div class="space-y-3">
              {#each analyses.slice(0, 5) as analysis}
                <div class="flex items-center justify-between py-2 border-b border-wisdom-100 last:border-b-0">
                  <div class="flex-1">
                    <p class="text-sm text-wisdom-700 truncate">{analysis.original_text.substring(0, 50)}...</p>
                    <p class="text-xs text-wisdom-500">{formatDate(analysis.created_at)}</p>
                  </div>
                  <div class="ml-4">
                    <span class="px-2 py-1 text-xs rounded-full {analysis.sentiment === 'negative' ? 'bg-red-100 text-red-600' : analysis.sentiment === 'positive' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}">
                      {analysis.sentiment}
                    </span>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        </div>
      {/if}

      <!-- Users Tab -->
      {#if currentTab === 'users'}
        <div class="bg-white rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-wisdom-200">
            <h3 class="text-lg font-semibold text-wisdom-900">User Management</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-wisdom-200">
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">User</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Email</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Status</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Role</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Joined</th>
                </tr>
              </thead>
              <tbody>
                {#each users as user}
                  <tr class="border-b border-wisdom-100">
                    <td class="py-3 px-6">
                      <div class="flex items-center space-x-3">
                        <div class="w-8 h-8 bg-wisdom-100 rounded-full flex items-center justify-center">
                          <span class="text-sm font-semibold text-wisdom-600">{user.username.charAt(0).toUpperCase()}</span>
                        </div>
                        <span class="text-wisdom-700">{user.username}</span>
                      </div>
                    </td>
                    <td class="py-3 px-6 text-wisdom-700">{user.email}</td>
                    <td class="py-3 px-6">
                      <span class="px-2 py-1 text-xs rounded-full {user.is_active ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}">
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td class="py-3 px-6">
                      <span class="px-2 py-1 text-xs rounded-full {user.is_admin ? 'bg-purple-100 text-purple-600' : 'bg-gray-100 text-gray-600'}">
                        {user.is_admin ? 'Admin' : 'User'}
                      </span>
                    </td>
                    <td class="py-3 px-6 text-wisdom-700">{formatDate(user.created_at)}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      {/if}

      <!-- Analyses Tab -->
      {#if currentTab === 'analyses'}
        <div class="bg-white rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-wisdom-200">
            <h3 class="text-lg font-semibold text-wisdom-900">Recent Analyses</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-wisdom-200">
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Text</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Sentiment</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Platform</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Model</th>
                  <th class="text-left py-3 px-6 font-semibold text-wisdom-900">Time</th>
                </tr>
              </thead>
              <tbody>
                {#each analyses as analysis}
                  <tr class="border-b border-wisdom-100">
                    <td class="py-3 px-6">
                      <p class="text-wisdom-700 text-sm max-w-xs truncate">{analysis.original_text}</p>
                    </td>
                    <td class="py-3 px-6">
                      <span class="px-2 py-1 text-xs rounded-full {analysis.sentiment === 'negative' ? 'bg-red-100 text-red-600' : analysis.sentiment === 'positive' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}">
                        {analysis.sentiment}
                      </span>
                    </td>
                    <td class="py-3 px-6 text-wisdom-700 capitalize">{analysis.platform}</td>
                    <td class="py-3 px-6 text-wisdom-700 text-sm">{analysis.model_used}</td>
                    <td class="py-3 px-6 text-wisdom-700">{formatDate(analysis.created_at)}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      {/if}

      <!-- System Tab -->
      {#if currentTab === 'system'}
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <Settings class="w-5 h-5 mr-2" />
              System Configuration
            </h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Rate Limiting</span>
                <span class="text-sm text-wisdom-600">100 req/hour</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Max Bulk Requests</span>
                <span class="text-sm text-wisdom-600">50 per batch</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Token Expiry</span>
                <span class="text-sm text-wisdom-600">30 minutes</span>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
              <AlertTriangle class="w-5 h-5 mr-2" />
              System Alerts
            </h3>
            <div class="space-y-3">
              <div class="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                <CheckCircle class="w-4 h-4 text-green-500" />
                <span class="text-sm text-green-700">All systems operational</span>
              </div>
              <div class="flex items-center space-x-3 p-3 bg-yellow-50 rounded-lg">
                <AlertTriangle class="w-4 h-4 text-yellow-500" />
                <span class="text-sm text-yellow-700">High request volume detected</span>
              </div>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </main>
</div>
