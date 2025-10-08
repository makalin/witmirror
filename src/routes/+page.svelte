<script lang="ts">
  import { onMount } from 'svelte';
  import { Mirror, Sparkles, Send, RotateCcw, Copy, Check, Settings, BarChart3, LogIn } from 'lucide-svelte';
  import { authStore } from '$lib/auth';
  import { goto } from '$app/navigation';
  
  let inputText = '';
  let wisdomResponse = '';
  let isAnalyzing = false;
  let isGenerating = false;
  let copied = false;
  let analysisResult: any = null;
  let user: any = null;
  let isAuthenticated = false;
  let selectedStyle = 'classic';
  let selectedPlatform = 'general';
  let selectedAiProvider = 'openai';
  
  const exampleComments = [
    "This screams AI slop.",
    "You clearly don't know what you're talking about.",
    "This is the dumbest thing I've ever read.",
    "Your opinion is worthless.",
    "This is complete garbage."
  ];
  
  onMount(() => {
    authStore.subscribe((state) => {
      isAuthenticated = state.isAuthenticated;
      user = state.user;
    });
  });

  async function analyzeAndGenerate() {
    if (!inputText.trim()) return;
    
    isAnalyzing = true;
    isGenerating = true;
    wisdomResponse = '';
    
    try {
      // Professional API call with advanced options
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: inputText,
          platform: selectedPlatform,
          style: selectedStyle,
          ai_provider: selectedAiProvider
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        analysisResult = data.analysis;
        wisdomResponse = data.wisdom;
      } else {
        // Fallback for demo
        wisdomResponse = generateFallbackWisdom(inputText);
      }
    } catch (error) {
      console.error('Error:', error);
      wisdomResponse = generateFallbackWisdom(inputText);
    } finally {
      isAnalyzing = false;
      isGenerating = false;
    }
  }
  
  function generateFallbackWisdom(text: string): string {
    const wisdomOptions = [
      "The mirror often blames the face it reflects.",
      "Politeness is free; rudeness always collects interest.",
      "A gentle word turns away wrath, but harsh words stir up anger.",
      "The wise speak because they have something to say; fools speak because they have to say something.",
      "When you point a finger at others, three fingers point back at you.",
      "The empty vessel makes the loudest sound.",
      "Wisdom is the reward for a lifetime of listening when you would have preferred to talk.",
      "The best way to win an argument is to avoid it.",
      "Kindness is a language that the deaf can hear and the blind can see.",
      "The tongue has no bones, but it can break hearts."
    ];
    
    return wisdomOptions[Math.floor(Math.random() * wisdomOptions.length)];
  }
  
  function useExample(example: string) {
    inputText = example;
  }
  
  async function copyToClipboard() {
    if (wisdomResponse) {
      await navigator.clipboard.writeText(wisdomResponse);
      copied = true;
      setTimeout(() => copied = false, 2000);
    }
  }
  
  function reset() {
    inputText = '';
    wisdomResponse = '';
    analysisResult = null;
    isAnalyzing = false;
    isGenerating = false;
  }
</script>

<svelte:head>
  <title>WitMirror — Turn Negativity into Wisdom</title>
  <meta name="description" content="Detect rude comments and respond with clever, proverb-style wisdom. Turn negativity into enlightenment." />
</svelte:head>

<div class="max-w-4xl mx-auto px-4 py-8">
  <!-- Hero Section -->
  <div class="text-center mb-12">
    <div class="inline-flex items-center justify-center w-16 h-16 bg-wisdom-100 rounded-full mb-6">
      <Mirror class="w-8 h-8 text-wisdom-600" />
    </div>
    <h1 class="text-4xl font-bold text-wisdom-900 mb-4">
      Turn Negativity into Wisdom
    </h1>
    <p class="text-xl text-wisdom-700 max-w-2xl mx-auto">
      WitMirror detects rude or negative comments and responds with clever, proverb-style wisdom. 
      Instead of arguing, reflect their tone back with calm wit.
    </p>
  </div>

  <!-- Main Interface -->
  <div class="bg-white rounded-2xl shadow-xl p-8 mb-8">
    <div class="space-y-6">
      <!-- Input Section -->
      <div>
        <label for="comment-input" class="block text-sm font-medium text-wisdom-900 mb-3">
          Paste the negative comment you'd like to reflect:
        </label>
        <div class="relative">
          <textarea
            id="comment-input"
            bind:value={inputText}
            placeholder="Enter a rude or negative comment here..."
            class="w-full h-32 px-4 py-3 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent resize-none"
            disabled={isAnalyzing || isGenerating}
          ></textarea>
          {#if isAnalyzing}
            <div class="absolute top-3 right-3">
              <div class="animate-spin w-5 h-5 border-2 border-wisdom-500 border-t-transparent rounded-full"></div>
            </div>
          {/if}
        </div>
      </div>

      <!-- Advanced Options -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label class="block text-sm font-medium text-wisdom-700 mb-2">Wisdom Style</label>
          <select
            bind:value={selectedStyle}
            class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            disabled={isAnalyzing || isGenerating}
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
          <label class="block text-sm font-medium text-wisdom-700 mb-2">Platform</label>
          <select
            bind:value={selectedPlatform}
            class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            disabled={isAnalyzing || isGenerating}
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
          <label class="block text-sm font-medium text-wisdom-700 mb-2">AI Provider</label>
          <select
            bind:value={selectedAiProvider}
            class="w-full px-3 py-2 border border-wisdom-300 rounded-lg focus:ring-2 focus:ring-wisdom-500 focus:border-transparent"
            disabled={isAnalyzing || isGenerating}
          >
            <option value="openai">OpenAI GPT-4</option>
            <option value="anthropic">Anthropic Claude</option>
            <option value="ollama">Ollama (Local)</option>
            <option value="fallback">Fallback</option>
          </select>
        </div>
      </div>

      <!-- Example Comments -->
      <div>
        <p class="text-sm font-medium text-wisdom-700 mb-3">Try these examples:</p>
        <div class="flex flex-wrap gap-2">
          {#each exampleComments as example}
            <button
              on:click={() => useExample(example)}
              class="px-3 py-1 text-sm bg-wisdom-100 text-wisdom-700 rounded-full hover:bg-wisdom-200 transition-colors"
              disabled={isAnalyzing || isGenerating}
            >
              "{example}"
            </button>
          {/each}
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3">
        <button
          on:click={analyzeAndGenerate}
          disabled={!inputText.trim() || isAnalyzing || isGenerating}
          class="flex items-center gap-2 px-6 py-3 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Sparkles class="w-4 h-4" />
          {isAnalyzing || isGenerating ? 'Reflecting...' : 'Reflect Wisdom'}
        </button>
        
        {#if wisdomResponse || inputText}
          <button
            on:click={reset}
            class="flex items-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <RotateCcw class="w-4 h-4" />
            Reset
          </button>
        {/if}
      </div>
    </div>
  </div>

  <!-- Wisdom Response -->
  {#if wisdomResponse}
    <div class="bg-gradient-to-br from-wisdom-50 to-wisdom-100 rounded-2xl shadow-xl p-8 wisdom-reveal">
      <div class="text-center">
        <div class="inline-flex items-center justify-center w-12 h-12 bg-wisdom-200 rounded-full mb-4">
          <Sparkles class="w-6 h-6 text-wisdom-700" />
        </div>
        <h3 class="text-lg font-semibold text-wisdom-900 mb-4">Your Wisdom Response</h3>
        
        <div class="bg-white rounded-xl p-6 shadow-sm mb-6">
          <blockquote class="text-xl wisdom-text text-wisdom-800 italic">
            "{wisdomResponse}"
          </blockquote>
        </div>
        
        <button
          on:click={copyToClipboard}
          class="flex items-center gap-2 mx-auto px-4 py-2 bg-wisdom-600 text-white rounded-lg hover:bg-wisdom-700 transition-colors"
        >
          {#if copied}
            <Check class="w-4 h-4" />
            Copied!
          {:else}
            <Copy class="w-4 h-4" />
            Copy Response
          {/if}
        </button>
      </div>
    </div>
  {/if}

  <!-- Features Section -->
  <div class="grid md:grid-cols-3 gap-6 mt-16">
    <div class="text-center p-6 bg-white rounded-xl shadow-sm">
      <div class="w-12 h-12 bg-wisdom-100 rounded-lg flex items-center justify-center mx-auto mb-4">
        <Sparkles class="w-6 h-6 text-wisdom-600" />
      </div>
      <h3 class="font-semibold text-wisdom-900 mb-2">Tone Detection</h3>
      <p class="text-sm text-wisdom-600">AI-powered sentiment analysis detects sarcasm, hostility, and negativity.</p>
    </div>
    
    <div class="text-center p-6 bg-white rounded-xl shadow-sm">
      <div class="w-12 h-12 bg-wisdom-100 rounded-lg flex items-center justify-center mx-auto mb-4">
        <Mirror class="w-6 h-6 text-wisdom-600" />
      </div>
      <h3 class="font-semibold text-wisdom-900 mb-2">Proverb Generator</h3>
      <p class="text-sm text-wisdom-600">Crafts original, wise phrases inspired by world proverbs and modern wit.</p>
    </div>
    
    <div class="text-center p-6 bg-white rounded-xl shadow-sm">
      <div class="w-12 h-12 bg-wisdom-100 rounded-lg flex items-center justify-center mx-auto mb-4">
        <Send class="w-6 h-6 text-wisdom-600" />
      </div>
      <h3 class="font-semibold text-wisdom-900 mb-2">Smart Replies</h3>
      <p class="text-sm text-wisdom-600">Context-aware responses that fit platform tone and style.</p>
    </div>
  </div>
</div>
