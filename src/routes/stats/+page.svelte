<script lang="ts">
  import { onMount } from 'svelte';
  import { BarChart3, TrendingUp, Users, Brain } from 'lucide-svelte';
  import { getStats, healthCheck } from '$lib/api';
  import type { ApiStats } from '$lib/types';

  let stats: ApiStats | null = null;
  let isHealthy = false;
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      isHealthy = await healthCheck();
      if (isHealthy) {
        stats = await getStats();
      } else {
        error = 'Backend API is not available';
      }
    } catch (err) {
      error = 'Failed to load statistics';
      console.error('Error loading stats:', err);
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head>
  <title>Statistics — WitMirror</title>
  <meta name="description" content="View usage statistics and analytics for WitMirror." />
</svelte:head>

<div class="max-w-6xl mx-auto px-4 py-8">
  <div class="text-center mb-8">
    <h1 class="text-4xl font-bold text-wisdom-900 mb-4">
      WitMirror Statistics
    </h1>
    <p class="text-xl text-wisdom-700">
      Insights into wisdom generation and usage patterns
    </p>
  </div>

  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
      <span class="ml-3 text-wisdom-700">Loading statistics...</span>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
      <div class="text-red-600 mb-2">⚠️</div>
      <h3 class="font-semibold text-red-900 mb-2">Unable to Load Statistics</h3>
      <p class="text-red-700">{error}</p>
    </div>
  {:else if stats}
    <!-- Stats Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
            <BarChart3 class="w-5 h-5 text-wisdom-600" />
          </div>
          <h3 class="font-semibold text-wisdom-900">Total Analyses</h3>
        </div>
        <p class="text-3xl font-bold text-wisdom-800">{stats.total_analyses}</p>
        <p class="text-sm text-wisdom-600">Comments processed</p>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
            <TrendingUp class="w-5 h-5 text-wisdom-600" />
          </div>
          <h3 class="font-semibold text-wisdom-900">Avg Confidence</h3>
        </div>
        <p class="text-3xl font-bold text-wisdom-800">{Math.round(stats.average_confidence * 100)}%</p>
        <p class="text-sm text-wisdom-600">Analysis accuracy</p>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
            <Users class="w-5 h-5 text-wisdom-600" />
          </div>
          <h3 class="font-semibold text-wisdom-900">Avg Toxicity</h3>
        </div>
        <p class="text-3xl font-bold text-wisdom-800">{Math.round(stats.average_toxicity * 100)}%</p>
        <p class="text-sm text-wisdom-600">Toxicity level</p>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
            <Brain class="w-5 h-5 text-wisdom-600" />
          </div>
          <h3 class="font-semibold text-wisdom-900">API Status</h3>
        </div>
        <p class="text-3xl font-bold text-green-600">Healthy</p>
        <p class="text-sm text-wisdom-600">Backend status</p>
      </div>
    </div>

    <!-- Additional Insights -->
    <div class="grid md:grid-cols-2 gap-6">
      <div class="bg-gradient-to-br from-wisdom-50 to-wisdom-100 rounded-xl p-6">
        <h3 class="font-semibold text-wisdom-900 mb-3">Wisdom Generation</h3>
        <p class="text-wisdom-700 text-sm mb-4">
          WitMirror has processed {stats.total_analyses} comments and generated 
          {stats.total_analyses} wisdom responses. The average confidence of 
          {Math.round(stats.average_confidence * 100)}% indicates reliable 
          sentiment analysis.
        </p>
        <div class="text-xs text-wisdom-600">
          Each analysis includes sentiment detection, emotion recognition, and toxicity scoring.
        </div>
      </div>

      <div class="bg-gradient-to-br from-wisdom-50 to-wisdom-100 rounded-xl p-6">
        <h3 class="font-semibold text-wisdom-900 mb-3">Toxicity Insights</h3>
        <p class="text-wisdom-700 text-sm mb-4">
          The average toxicity score of {Math.round(stats.average_toxicity * 100)}% 
          suggests that most analyzed comments contain some level of negativity, 
          which is exactly what WitMirror is designed to address.
        </p>
        <div class="text-xs text-wisdom-600">
          Higher toxicity scores indicate more hostile or aggressive language.
        </div>
      </div>
    </div>
  {/if}

  <!-- Back to Home -->
  <div class="text-center mt-8">
    <a 
      href="/" 
      class="inline-flex items-center gap-2 px-6 py-3 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
    >
      ← Back to WitMirror
    </a>
  </div>
</div>
