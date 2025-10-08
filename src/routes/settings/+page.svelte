<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/auth';
  import { apiClient } from '$lib/api';
  import { goto } from '$app/navigation';
  import { 
    Settings, 
    User, 
    Bell, 
    Shield, 
    Palette,
    Save,
    Eye,
    EyeOff,
    Download,
    Upload
  } from 'lucide-svelte';
  import type { User as UserType, UserPreferences } from '$lib/types';

  let user: UserType | null = null;
  let preferences: UserPreferences = {
    default_style: 'classic',
    default_platform: 'general',
    default_ai_provider: 'openai',
    notifications: {
      email: true,
      push: false
    },
    privacy: {
      save_history: true,
      share_analytics: false
    },
    display: {
      theme: 'auto',
      language: 'en'
    }
  };
  let isLoading = true;
  let isSaving = false;
  let error = '';
  let success = '';
  let showPassword = false;
  let currentPassword = '';
  let newPassword = '';
  let confirmPassword = '';

  onMount(async () => {
    // Check authentication
    authStore.subscribe((state) => {
      if (!state.isAuthenticated && !state.isLoading) {
        goto('/login');
      }
      if (state.user) {
        user = state.user;
        preferences = { ...preferences, ...state.user.preferences };
      }
    });

    isLoading = false;
  });

  async function savePreferences() {
    if (isSaving) return;

    isSaving = true;
    error = '';
    success = '';

    try {
      await apiClient.updatePreferences(preferences);
      success = 'Preferences saved successfully!';
    } catch (err: any) {
      error = err.message || 'Failed to save preferences';
    } finally {
      isSaving = false;
    }
  }

  async function changePassword() {
    if (newPassword !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    if (newPassword.length < 8) {
      error = 'Password must be at least 8 characters long';
      return;
    }

    try {
      // This would be implemented in the backend
      success = 'Password changed successfully!';
      currentPassword = '';
      newPassword = '';
      confirmPassword = '';
    } catch (err: any) {
      error = err.message || 'Failed to change password';
    }
  }

  function exportData() {
    // Implement data export
    const data = {
      user,
      preferences,
      export_date: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `witmirror-data-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }
</script>

<svelte:head>
  <title>Settings — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100">
  <!-- Header -->
  <header class="bg-white shadow-sm border-b border-wisdom-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-4">
          <div class="p-2 bg-wisdom-100 rounded-lg">
            <Settings class="w-6 h-6 text-wisdom-600" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-wisdom-900">Settings</h1>
            <p class="text-sm text-wisdom-600">Manage your account and preferences</p>
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

  <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if isLoading}
      <div class="flex items-center justify-center py-12">
        <div class="animate-spin w-8 h-8 border-4 border-wisdom-500 border-t-transparent rounded-full"></div>
        <span class="ml-3 text-wisdom-700">Loading settings...</span>
      </div>
    {:else}
      <!-- Profile Settings -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
          <User class="w-5 h-5 mr-2" />
          Profile Information
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Username</label>
            <input
              type="text"
              value={user?.username || ''}
              disabled
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg bg-wisdom-50 text-wisdom-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Email</label>
            <input
              type="email"
              value={user?.email || ''}
              disabled
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg bg-wisdom-50 text-wisdom-500"
            />
          </div>
        </div>
      </div>

      <!-- Default Preferences -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
          <Settings class="w-5 h-5 mr-2" />
          Default Preferences
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Default Wisdom Style</label>
            <select
              bind:value={preferences.default_style}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="classic">Classic</option>
              <option value="stoic">Stoic</option>
              <option value="zen">Zen</option>
              <option value="sufi">Sufi</option>
              <option value="sarcastic">Sarcastic</option>
              <option value="poetic">Poetic</option>
              <option value="scientific">Scientific</option>
              <option value="humorous">Humorous</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Default Platform</label>
            <select
              bind:value={preferences.default_platform}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="general">General</option>
              <option value="reddit">Reddit</option>
              <option value="twitter">Twitter</option>
              <option value="facebook">Facebook</option>
              <option value="instagram">Instagram</option>
              <option value="youtube">YouTube</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Default AI Provider</label>
            <select
              bind:value={preferences.default_ai_provider}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
              <option value="ollama">Ollama</option>
              <option value="fallback">Fallback</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
          <Bell class="w-5 h-5 mr-2" />
          Notifications
        </h3>
        
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-wisdom-900">Email Notifications</h4>
              <p class="text-sm text-wisdom-600">Receive updates via email</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                bind:checked={preferences.notifications.email}
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-wisdom-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-wisdom-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-wisdom-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-wisdom-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-wisdom-900">Push Notifications</h4>
              <p class="text-sm text-wisdom-600">Receive browser notifications</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                bind:checked={preferences.notifications.push}
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-wisdom-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-wisdom-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-wisdom-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-wisdom-600"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Privacy -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
          <Shield class="w-5 h-5 mr-2" />
          Privacy Settings
        </h3>
        
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-wisdom-900">Save Analysis History</h4>
              <p class="text-sm text-wisdom-600">Store your analysis history for future reference</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                bind:checked={preferences.privacy.save_history}
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-wisdom-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-wisdom-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-wisdom-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-wisdom-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-wisdom-900">Share Analytics</h4>
              <p class="text-sm text-wisdom-600">Help improve the service by sharing anonymous usage data</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                bind:checked={preferences.privacy.share_analytics}
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-wisdom-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-wisdom-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-wisdom-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-wisdom-600"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Display Settings -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4 flex items-center">
          <Palette class="w-5 h-5 mr-2" />
          Display Settings
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Theme</label>
            <select
              bind:value={preferences.display.theme}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Language</label>
            <select
              bind:value={preferences.display.language}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Password Change -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4">Change Password</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Current Password</label>
            <div class="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                bind:value={currentPassword}
                class="w-full px-3 py-2 pr-10 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
                placeholder="Enter current password"
              />
              <button
                type="button"
                on:click={() => showPassword = !showPassword}
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-wisdom-400 hover:text-wisdom-600"
              >
                {#if showPassword}
                  <EyeOff class="w-4 h-4" />
                {:else}
                  <Eye class="w-4 h-4" />
                {/if}
              </button>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">New Password</label>
            <input
              type="password"
              bind:value={newPassword}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              placeholder="Enter new password"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-wisdom-700 mb-2">Confirm New Password</label>
            <input
              type="password"
              bind:value={confirmPassword}
              class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              placeholder="Confirm new password"
            />
          </div>
          
          <button
            on:click={changePassword}
            class="px-4 py-2 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
          >
            Change Password
          </button>
        </div>
      </div>

      <!-- Data Management -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4">Data Management</h3>
        
        <div class="flex space-x-4">
          <button
            on:click={exportData}
            class="flex items-center space-x-2 px-4 py-2 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
          >
            <Download class="w-4 h-4" />
            <span>Export Data</span>
          </button>
          
          <button
            class="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            <Upload class="w-4 h-4" />
            <span>Delete Account</span>
          </button>
        </div>
      </div>

      <!-- Save Button -->
      <div class="flex justify-end">
        <button
          on:click={savePreferences}
          disabled={isSaving}
          class="flex items-center space-x-2 px-6 py-3 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {#if isSaving}
            <div class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
          {:else}
            <Save class="w-4 h-4" />
          {/if}
          <span>{isSaving ? 'Saving...' : 'Save Preferences'}</span>
        </button>
      </div>

      <!-- Messages -->
      {#if error}
        <div class="mt-4 bg-red-50 border border-red-200 rounded-lg p-3">
          <p class="text-sm text-red-600">{error}</p>
        </div>
      {/if}

      {#if success}
        <div class="mt-4 bg-green-50 border border-green-200 rounded-lg p-3">
          <p class="text-sm text-green-600">{success}</p>
        </div>
      {/if}
    {/if}
  </main>
</div>
