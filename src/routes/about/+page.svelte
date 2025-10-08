<script lang="ts">
  import { Brain, Heart, Shield, Lightbulb } from 'lucide-svelte';
</script>

<svelte:head>
  <title>About WitMirror — Philosophy & Features</title>
  <meta name="description" content="Learn about WitMirror's philosophy of turning negativity into wisdom through AI-powered reflection." />
</svelte:head>

<div class="max-w-4xl mx-auto px-4 py-8">
  <!-- Hero Section -->
  <div class="text-center mb-12">
    <h1 class="text-4xl font-bold text-wisdom-900 mb-4">
      About WitMirror
    </h1>
    <p class="text-xl text-wisdom-700 max-w-2xl mx-auto">
      Understanding the philosophy behind turning negativity into wisdom
    </p>
  </div>

  <!-- Philosophy Section -->
  <div class="bg-white rounded-2xl shadow-xl p-8 mb-8">
    <div class="flex items-start gap-4 mb-6">
      <div class="w-12 h-12 bg-wisdom-100 rounded-lg flex items-center justify-center flex-shrink-0">
        <Heart class="w-6 h-6 text-wisdom-600" />
      </div>
      <div>
        <h2 class="text-2xl font-bold text-wisdom-900 mb-3">Our Philosophy</h2>
        <p class="text-wisdom-700 leading-relaxed">
          WitMirror believes that wisdom always wins over noise. Instead of fighting trolls, 
          we enlighten them. When someone is rude or negative, the best response isn't to match 
          their energy—it's to reflect their behavior back with calm, thoughtful wisdom that 
          reveals the emptiness of their words.
        </p>
      </div>
    </div>
    
    <blockquote class="border-l-4 border-wisdom-500 pl-6 py-4 bg-wisdom-50 rounded-r-lg">
      <p class="text-lg wisdom-text text-wisdom-800 italic">
        "When a wise man points at the moon, the fool looks at the finger."
      </p>
      <cite class="text-sm text-wisdom-600 mt-2 block">— Ancient Proverb</cite>
    </blockquote>
  </div>

  <!-- How It Works -->
  <div class="bg-gradient-to-br from-wisdom-50 to-wisdom-100 rounded-2xl shadow-xl p-8 mb-8">
    <h2 class="text-2xl font-bold text-wisdom-900 mb-6 text-center">How WitMirror Works</h2>
    
    <div class="grid md:grid-cols-2 gap-8">
      <div class="space-y-6">
        <div class="flex items-start gap-4">
          <div class="w-8 h-8 bg-wisdom-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
          <div>
            <h3 class="font-semibold text-wisdom-900 mb-2">Tone Detection</h3>
            <p class="text-sm text-wisdom-700">
              Our AI analyzes the sentiment, intent, and emotional tone of the comment to identify 
              negativity, sarcasm, or hostility.
            </p>
          </div>
        </div>
        
        <div class="flex items-start gap-4">
          <div class="w-8 h-8 bg-wisdom-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
          <div>
            <h3 class="font-semibold text-wisdom-900 mb-2">Wisdom Generation</h3>
            <p class="text-sm text-wisdom-700">
              Based on the analysis, we craft an original proverb or wise saying that reflects 
              the commenter's behavior back to them with elegance.
            </p>
          </div>
        </div>
      </div>
      
      <div class="space-y-6">
        <div class="flex items-start gap-4">
          <div class="w-8 h-8 bg-wisdom-600 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
          <div>
            <h3 class="font-semibold text-wisdom-900 mb-2">Context Awareness</h3>
            <p class="text-sm text-wisdom-700">
              The response is tailored to fit the platform and context, whether it's Reddit, 
              Twitter, or a comment section.
            </p>
          </div>
        </div>
        
        <div class="flex items-start gap-4">
          <div class="w-8 h-8 bg-wisdom-600 text-white rounded-full flex items-center justify-center text-sm font-bold">4</div>
          <div>
            <h3 class="font-semibold text-wisdom-900 mb-2">Mirror Effect</h3>
            <p class="text-sm text-wisdom-700">
              The wisdom response subtly mirrors the commenter's tone back to them, 
              revealing their behavior through calm reflection.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Features Grid -->
  <div class="grid md:grid-cols-2 gap-6 mb-8">
    <div class="bg-white rounded-xl shadow-sm p-6">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
          <Brain class="w-5 h-5 text-wisdom-600" />
        </div>
        <h3 class="font-semibold text-wisdom-900">AI-Powered Analysis</h3>
      </div>
      <p class="text-sm text-wisdom-700">
        Advanced sentiment analysis and intent detection to identify negative patterns 
        in online communication.
      </p>
    </div>
    
    <div class="bg-white rounded-xl shadow-sm p-6">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
          <Lightbulb class="w-5 h-5 text-wisdom-600" />
        </div>
        <h3 class="font-semibold text-wisdom-900">Original Wisdom</h3>
      </div>
      <p class="text-sm text-wisdom-700">
        Generate unique, contextually appropriate proverbs and wise sayings 
        inspired by world wisdom traditions.
      </p>
    </div>
    
    <div class="bg-white rounded-xl shadow-sm p-6">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
          <Shield class="w-5 h-5 text-wisdom-600" />
        </div>
        <h3 class="font-semibold text-wisdom-900">Peaceful Response</h3>
      </div>
      <p class="text-sm text-wisdom-700">
        Turn confrontational situations into opportunities for enlightenment 
        and positive discourse.
      </p>
    </div>
    
    <div class="bg-white rounded-xl shadow-sm p-6">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 bg-wisdom-100 rounded-lg flex items-center justify-center">
          <Brain class="w-5 h-5 text-wisdom-600" />
        </div>
        <h3 class="font-semibold text-wisdom-900">Smart Adaptation</h3>
      </div>
      <p class="text-sm text-wisdom-700">
        Responses adapt to different platforms and communication styles 
        for maximum impact and appropriateness.
      </p>
    </div>
  </div>

  <!-- Roadmap -->
  <div class="bg-wisdom-900 text-white rounded-2xl shadow-xl p-8">
    <h2 class="text-2xl font-bold mb-6 text-center">Coming Soon</h2>
    
    <div class="grid md:grid-cols-2 gap-6">
      <div>
        <h3 class="font-semibold mb-3">Browser Extension</h3>
        <p class="text-wisdom-300 text-sm mb-4">
          Highlight any comment online and get instant wisdom responses. 
          Available for Chrome and Firefox.
        </p>
        <div class="flex items-center gap-2 text-wisdom-400 text-sm">
          <div class="w-2 h-2 bg-wisdom-500 rounded-full"></div>
          In Development
        </div>
      </div>
      
      <div>
        <h3 class="font-semibold mb-3">Wisdom Styles</h3>
        <p class="text-wisdom-300 text-sm mb-4">
          Choose from different wisdom traditions: Sufi, Stoic, Zen, 
          or Sarcastic responses.
        </p>
        <div class="flex items-center gap-2 text-wisdom-400 text-sm">
          <div class="w-2 h-2 bg-wisdom-500 rounded-full"></div>
          Planned
        </div>
      </div>
    </div>
  </div>
</div>
