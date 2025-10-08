<script lang="ts">
  import { onMount } from 'svelte';
  import { apiClient } from '$lib/api';
  import { authStore } from '$lib/auth';
  import { goto } from '$app/navigation';
  import { 
    Link, 
    MessageSquare, 
    Twitter, 
    Reddit,
    Discord,
    BarChart3,
    Settings,
    Plus,
    ExternalLink,
    TrendingUp,
    Users
  } from 'lucide-svelte';

  let integrations: any = null;
  let redditComments: any[] = [];
  let twitterMentions: any[] = [];
  let socialSentiment: any = null;
  let isLoading = true;
  let error = '';
  let activeTab = 'overview';
  let subredditQuery = 'technology';
  let twitterQuery = 'witmirror';
  let sentimentPlatform = 'reddit';
  let sentimentQuery = 'technology';

  onMount(async () => {
    // Check authentication
    authStore.subscribe((state) => {
      if (!state.isAuthenticated && !state.isLoading) {
        goto('/login');
      }
    });

    await loadIntegrations();
  });

  async function loadIntegrations() {
    try {
      isLoading = true;
      const [statsData] = await Promise.all([
        apiClient.getIntegrationStats()
      ]);
      
      integrations = statsData;
    } catch (err: any) {
      error = err.message || 'Failed to load integrations';
    } finally {
      isLoading = false;
    }
  }

  async function loadRedditComments() {
    try {
      const comments = await apiClient.getRedditComments(subredditQuery, 10);
      redditComments = comments;
    } catch (err: any) {
      error = err.message || 'Failed to load Reddit comments';
    }
  }

  async function loadTwitterMentions() {
    try {
      const mentions = await apiClient.getTwitterMentions(twitterQuery, 10);
      twitterMentions = mentions;
    } catch (err: any) {
      error = err.message || 'Failed to load Twitter mentions';
    }
  }

  async function analyzeSocialSentiment() {
    try {
      const analysis = await apiClient.analyzeSocialSentiment(sentimentPlatform, sentimentQuery, 50);
      socialSentiment = analysis;
    } catch (err: any) {
      error = err.message || 'Failed to analyze social sentiment';
    }
  }

  function formatDate(timestamp: number) {
    return new Date(timestamp * 1000).toLocaleDateString();
  }

  function getSentimentColor(sentiment: string) {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }
</script>

<svelte:head>
  <title>Integrations — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100">
  <!-- Header -->
  <header class="bg-white shadow-sm border-b border-wisdom-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-wisdom-100 rounded-lg">
            <Link class="w-6 h-6 text-wisdom-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-wisdom-900">API Integrations</h1>
            <p class="text-sm text-wisdom-600">Connect with social media platforms and external services</p>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if isLoading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
        <span class="ml-3 text-wisdom-700">Loading integrations...</span>
      </div>
    {:else if error}
      <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <div class="text-red-600 mb-2">⚠️</div>
        <h3 class="font-semibold text-red-900 mb-2">Error Loading Integrations</h3>
        <p class="text-red-700">{error}</p>
      </div>
    {:else}
      <!-- Integration Stats -->
      {#if integrations}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
                <MessageSquare class="w-5 h-5 text-wisdom-600" />
              </div>
              <span class="text-2xl font-bold text-wisdom-800">{integrations.total_analyses}</span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Total Analyses</h3>
            <p class="text-sm text-wisdom-600">Through integrations</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <Reddit class="w-5 h-5 text-orange-600" />
              </div>
              <span class="text-2xl font-bold text-orange-600">
                {integrations.platform_usage.reddit || 0}
              </span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Reddit</h3>
            <p class="text-sm text-wisdom-600">Comments analyzed</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Twitter class="w-5 h-5 text-blue-600" />
              </div>
              <span class="text-2xl font-bold text-blue-600">
                {integrations.platform_usage.twitter || 0}
              </span>
            </div>
            <h3 class="font-semibold text-wisdom-900 mb-1">Twitter</h3>
            <p class="text-sm text-wisdom-600">Mentions analyzed</p>
          </div>
        </div>
      {/if}

      <!-- Tab Navigation -->
      <div class="mb-8">
        <nav class="flex space-x-8">
          <button
            on:click={() => activeTab = 'overview'}
            class="py-2 px-1 border-b-2 font-medium text-sm {activeTab === 'overview' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Overview
          </button>
          <button
            on:click={() => activeTab = 'reddit'}
            class="py-2 px-1 border-b-2 font-medium text-sm {activeTab === 'reddit' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Reddit
          </button>
          <button
            on:click={() => activeTab = 'twitter'}
            class="py-2 px-1 border-b-2 font-medium text-sm {activeTab === 'twitter' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Twitter
          </button>
          <button
            on:click={() => activeTab = 'sentiment'}
            class="py-2 px-1 border-b-2 font-medium text-sm {activeTab === 'sentiment' ? 'border-wisdom-500 text-wisdom-600' : 'border-transparent text-wisdom-500 hover:text-wisdom-700 hover:border-wisdom-300'}"
          >
            Sentiment Analysis
          </button>
        </nav>
      </div>

      <!-- Overview Tab -->
      {#if activeTab === 'overview'}
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Available Integrations -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4">Available Integrations</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 border border-wisdom-200 rounded-lg">
                <div class="flex items-center space-x-3">
                  <Reddit class="w-6 h-6 text-orange-600" />
                  <div>
                    <h4 class="font-medium text-wisdom-900">Reddit API</h4>
                    <p class="text-sm text-wisdom-600">Analyze Reddit comments and posts</p>
                  </div>
                </div>
                <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-600">Active</span>
              </div>
              
              <div class="flex items-center justify-between p-4 border border-wisdom-200 rounded-lg">
                <div class="flex items-center space-x-3">
                  <Twitter class="w-6 h-6 text-blue-600" />
                  <div>
                    <h4 class="font-medium text-wisdom-900">Twitter API</h4>
                    <p class="text-sm text-wisdom-600">Analyze tweets and mentions</p>
                  </div>
                </div>
                <span class="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-600">Setup Required</span>
              </div>
              
              <div class="flex items-center justify-between p-4 border border-wisdom-200 rounded-lg">
                <div class="flex items-center space-x-3">
                  <Discord class="w-6 h-6 text-indigo-600" />
                  <div>
                    <h4 class="font-medium text-wisdom-900">Discord Webhooks</h4>
                    <p class="text-sm text-wisdom-600">Send wisdom to Discord channels</p>
                  </div>
                </div>
                <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-600">Active</span>
              </div>
            </div>
          </div>

          <!-- Integration Status -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-wisdom-900 mb-4">Integration Status</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Reddit API</span>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span class="text-sm text-green-600">Connected</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Twitter API</span>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <span class="text-sm text-yellow-600">Setup Required</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-wisdom-700">Discord Webhooks</span>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span class="text-sm text-green-600">Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      {/if}

      <!-- Reddit Tab -->
      {#if activeTab === 'reddit'}
        <div class="bg-white rounded-xl shadow-sm p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-wisdom-900">Reddit Integration</h3>
            <div class="flex items-center space-x-4">
              <input
                type="text"
                bind:value={subredditQuery}
                placeholder="Enter subreddit name"
                class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              />
              <button
                on:click={loadRedditComments}
                class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
              >
                Load Comments
              </button>
            </div>
          </div>
          
          {#if redditComments.length > 0}
            <div class="space-y-4">
              {#each redditComments as comment}
                <div class="border border-wisdom-200 rounded-lg p-4">
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex items-center space-x-2">
                      <span class="text-sm text-wisdom-600">u/{comment.author}</span>
                      <span class="text-sm text-wisdom-500">•</span>
                      <span class="text-sm text-wisdom-500">{comment.score} points</span>
                    </div>
                    <span class="text-xs text-wisdom-500">{formatDate(comment.created_utc)}</span>
                  </div>
                  <p class="text-wisdom-900 mb-3">{comment.text}</p>
                  <div class="flex items-center space-x-2">
                    <span class="px-2 py-1 text-xs rounded-full bg-orange-100 text-orange-600">
                      r/{comment.subreddit}
                    </span>
                    <button class="text-sm text-wisdom-600 hover:text-wisdom-800">
                      Analyze with WitMirror →
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {:else}
            <div class="text-center py-8">
              <Reddit class="w-12 h-12 text-wisdom-400 mx-auto mb-4" />
              <p class="text-wisdom-600">Enter a subreddit name and click "Load Comments" to get started</p>
            </div>
          {/if}
        </div>
      {/if}

      <!-- Twitter Tab -->
      {#if activeTab === 'twitter'}
        <div class="bg-white rounded-xl shadow-sm p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-wisdom-900">Twitter Integration</h3>
            <div class="flex items-center space-x-4">
              <input
                type="text"
                bind:value={twitterQuery}
                placeholder="Enter username or hashtag"
                class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              />
              <button
                on:click={loadTwitterMentions}
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Load Mentions
              </button>
            </div>
          </div>
          
          {#if twitterMentions.length > 0}
            <div class="space-y-4">
              {#each twitterMentions as mention}
                <div class="border border-wisdom-200 rounded-lg p-4">
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex items-center space-x-2">
                      <span class="text-sm text-wisdom-600">@{mention.author}</span>
                    </div>
                    <span class="text-xs text-wisdom-500">{formatDate(mention.created_at)}</span>
                  </div>
                  <p class="text-wisdom-900 mb-3">{mention.text}</p>
                  <div class="flex items-center space-x-2">
                    <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-600">
                      Twitter
                    </span>
                    <button class="text-sm text-wisdom-600 hover:text-wisdom-800">
                      Analyze with WitMirror →
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {:else}
            <div class="text-center py-8">
              <Twitter class="w-12 h-12 text-wisdom-400 mx-auto mb-4" />
              <p class="text-wisdom-600">Enter a username or hashtag and click "Load Mentions" to get started</p>
            </div>
          {/if}
        </div>
      {/if}

      <!-- Sentiment Analysis Tab -->
      {#if activeTab === 'sentiment'}
        <div class="bg-white rounded-xl shadow-sm p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-wisdom-900">Social Media Sentiment Analysis</h3>
            <div class="flex items-center space-x-4">
              <select
                bind:value={sentimentPlatform}
                class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              >
                <option value="reddit">Reddit</option>
                <option value="twitter">Twitter</option>
              </select>
              <input
                type="text"
                bind:value={sentimentQuery}
                placeholder="Enter search query"
                class="px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              />
              <button
                on:click={analyzeSocialSentiment}
                class="px-4 py-2 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
              >
                Analyze Sentiment
              </button>
            </div>
          </div>
          
          {#if socialSentiment}
            <div class="space-y-6">
              <!-- Sentiment Overview -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="text-center p-4 bg-green-50 rounded-lg">
                  <div class="text-2xl font-bold text-green-600">{socialSentiment.sentiment_distribution.positive || 0}</div>
                  <div class="text-sm text-green-700">Positive</div>
                </div>
                <div class="text-center p-4 bg-red-50 rounded-lg">
                  <div class="text-2xl font-bold text-red-600">{socialSentiment.sentiment_distribution.negative || 0}</div>
                  <div class="text-sm text-red-700">Negative</div>
                </div>
                <div class="text-center p-4 bg-gray-50 rounded-lg">
                  <div class="text-2xl font-bold text-gray-600">{socialSentiment.sentiment_distribution.neutral || 0}</div>
                  <div class="text-sm text-gray-700">Neutral</div>
                </div>
              </div>

              <!-- Recommended Responses -->
              {#if socialSentiment.recommended_responses.length > 0}
                <div>
                  <h4 class="font-semibold text-wisdom-900 mb-3">Recommended Wisdom Responses</h4>
                  <div class="space-y-3">
                    {#each socialSentiment.recommended_responses as response}
                      <div class="border border-wisdom-200 rounded-lg p-4">
                        <p class="text-wisdom-900 mb-2 font-medium">"{response.original_text}"</p>
                        <p class="text-wisdom-700 italic">"{response.wisdom_response}"</p>
                      </div>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>
          {:else}
            <div class="text-center py-8">
              <BarChart3 class="w-12 h-12 text-wisdom-400 mx-auto mb-4" />
              <p class="text-wisdom-600">Select a platform and enter a search query to analyze sentiment</p>
            </div>
          {/if}
        </div>
      {/if}
    {/if}
  </main>
</div>
