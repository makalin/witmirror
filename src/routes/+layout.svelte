<script lang="ts">
  import '../app.css';
  import { Mirror, Sparkles, Brain, BarChart3, LogIn, Clock, Link } from 'lucide-svelte';
</script>

<header class="bg-white/80 backdrop-blur-sm border-b border-wisdom-200 sticky top-0 z-50">
  <div class="max-w-4xl mx-auto px-4 py-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-wisdom-100 rounded-lg">
          <Mirror class="w-6 h-6 text-wisdom-600" />
        </div>
        <div>
          <h1 class="text-xl font-bold text-wisdom-900">WitMirror</h1>
          <p class="text-sm text-wisdom-600">Turn Negativity into Wisdom</p>
        </div>
      </div>
      
      <nav class="flex items-center space-x-6">
        <a href="/" class="text-wisdom-700 hover:text-wisdom-900 transition-colors" title="Home">
          <Sparkles class="w-5 h-5" />
        </a>
        <a href="/about" class="text-wisdom-700 hover:text-wisdom-900 transition-colors" title="About">
          <Brain class="w-5 h-5" />
        </a>
        <a href="/analytics" class="text-wisdom-700 hover:text-wisdom-900 transition-colors" title="Analytics">
          <BarChart3 class="w-5 h-5" />
        </a>
        <a href="/history" class="text-wisdom-700 hover:text-wisdom-900 transition-colors" title="History">
          <Clock class="w-5 h-5" />
        </a>
        <a href="/integrations" class="text-wisdom-700 hover:text-wisdom-900 transition-colors" title="Integrations">
          <Link class="w-5 h-5" />
        </a>
        <a href="/login" class="text-wisdom-700 hover:text-wisdom-900 transition-colors" title="Login">
          <LogIn class="w-5 h-5" />
        </a>
      </nav>
    </div>
  </div>
</header>

<main class="min-h-screen">
  <slot />
</main>

<footer class="bg-wisdom-900 text-white py-8 mt-16">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <p class="text-wisdom-300 mb-2">"When a wise man points at the moon, the fool looks at the finger."</p>
    <p class="text-sm text-wisdom-400">
      WitMirror believes wisdom always wins over noise.
    </p>
  </div>
</footer>
