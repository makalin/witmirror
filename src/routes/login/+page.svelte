<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/auth';
  import { goto } from '$app/navigation';
  import { LogIn, User, Lock, Mail } from 'lucide-svelte';

  let username = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let isLogin = true;
  let isLoading = false;
  let error = '';
  let success = '';

  onMount(() => {
    // Redirect if already authenticated
    authStore.subscribe((state) => {
      if (state.isAuthenticated && !state.isLoading) {
        goto('/dashboard');
      }
    });
  });

  async function handleSubmit() {
    if (isLoading) return;

    error = '';
    success = '';
    isLoading = true;

    try {
      if (isLogin) {
        await authStore.login(username, password);
        success = 'Login successful! Redirecting...';
        setTimeout(() => goto('/dashboard'), 1000);
      } else {
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match');
        }
        await authStore.register(username, email, password);
        success = 'Registration successful! Redirecting...';
        setTimeout(() => goto('/dashboard'), 1000);
      }
    } catch (err: any) {
      error = err.message || 'An error occurred';
    } finally {
      isLoading = false;
    }
  }

  function toggleMode() {
    isLogin = !isLogin;
    error = '';
    success = '';
  }
</script>

<svelte:head>
  <title>{isLogin ? 'Login' : 'Register'} — WitMirror Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-wisdom-50 to-wisdom-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8">
    <div class="text-center">
      <div class="mx-auto h-12 w-12 bg-wisdom-600 rounded-full flex items-center justify-center">
        <User class="h-6 w-6 text-white" />
      </div>
      <h2 class="mt-6 text-3xl font-bold text-wisdom-900">
        {isLogin ? 'Sign in to your account' : 'Create your account'}
      </h2>
      <p class="mt-2 text-sm text-wisdom-600">
        {isLogin ? "Don't have an account?" : 'Already have an account?'}
        <button
          on:click={toggleMode}
          class="font-medium text-wisdom-600 hover:text-wisdom-500 ml-1"
        >
          {isLogin ? 'Sign up' : 'Sign in'}
        </button>
      </p>
    </div>

    <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
      <div class="space-y-4">
        {#if !isLogin}
          <div>
            <label for="email" class="block text-sm font-medium text-wisdom-700 mb-1">
              Email address
            </label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-wisdom-400" />
              <input
                id="email"
                type="email"
                bind:value={email}
                required={!isLogin}
                class="pl-10 w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>
          </div>
        {/if}

        <div>
          <label for="username" class="block text-sm font-medium text-wisdom-700 mb-1">
            Username
          </label>
          <div class="relative">
            <User class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-wisdom-400" />
            <input
              id="username"
              type="text"
              bind:value={username}
              required
              class="pl-10 w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              placeholder="Enter your username"
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-wisdom-700 mb-1">
            Password
          </label>
          <div class="relative">
            <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-wisdom-400" />
            <input
              id="password"
              type="password"
              bind:value={password}
              required
              class="pl-10 w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
              placeholder="Enter your password"
            />
          </div>
        </div>

        {#if !isLogin}
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-wisdom-700 mb-1">
              Confirm Password
            </label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-wisdom-400" />
              <input
                id="confirmPassword"
                type="password"
                bind:value={confirmPassword}
                required={!isLogin}
                class="pl-10 w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
                placeholder="Confirm your password"
              />
            </div>
          </div>
        {/if}
      </div>

      {#if error}
        <div class="bg-red-50 border border-red-200 rounded-lg p-3">
          <p class="text-sm text-red-600">{error}</p>
        </div>
      {/if}

      {#if success}
        <div class="bg-green-50 border border-green-200 rounded-lg p-3">
          <p class="text-sm text-green-600">{success}</p>
        </div>
      {/if}

      <div>
        <button
          type="submit"
          disabled={isLoading}
          class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-wisdom-600 hover:bg-wisdom-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-wisdom-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {#if isLoading}
            <div class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
          {/if}
          <LogIn class="h-4 w-4 mr-2" />
          {isLoading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
        </button>
      </div>
    </form>

    <div class="text-center">
      <a href="/" class="text-sm text-wisdom-600 hover:text-wisdom-500">
        ← Back to WitMirror
      </a>
    </div>
  </div>
</div>
