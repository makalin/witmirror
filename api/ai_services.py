import openai
import os
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import requests
from dataclasses import dataclass

@dataclass
class AIProvider:
    name: str
    api_key: str
    base_url: Optional[str] = None
    model: str = "gpt-4"
    max_tokens: int = 100
    temperature: float = 0.7

class AIServiceManager:
    def __init__(self):
        self.providers = {}
        self.setup_providers()
    
    def setup_providers(self):
        """Setup AI providers"""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            self.providers["openai"] = AIProvider(
                name="OpenAI",
                api_key=os.getenv("OPENAI_API_KEY"),
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "100")),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
            )
        
        # Anthropic Claude
        if os.getenv("ANTHROPIC_API_KEY"):
            self.providers["anthropic"] = AIProvider(
                name="Anthropic",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
                max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "100"))
            )
        
        # Local LLM (Ollama)
        if os.getenv("OLLAMA_BASE_URL"):
            self.providers["ollama"] = AIProvider(
                name="Ollama",
                api_key="",  # Ollama doesn't require API key
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                model=os.getenv("OLLAMA_MODEL", "llama2"),
                max_tokens=int(os.getenv("OLLAMA_MAX_TOKENS", "100"))
            )
    
    def generate_wisdom(self, text: str, style: str = "classic", provider: str = "openai") -> Tuple[str, float, str]:
        """Generate wisdom response using specified provider"""
        start_time = time.time()
        
        try:
            if provider == "openai" and "openai" in self.providers:
                return self._generate_with_openai(text, style)
            elif provider == "anthropic" and "anthropic" in self.providers:
                return self._generate_with_anthropic(text, style)
            elif provider == "ollama" and "ollama" in self.providers:
                return self._generate_with_ollama(text, style)
            else:
                # Fallback to OpenAI or first available provider
                if "openai" in self.providers:
                    return self._generate_with_openai(text, style)
                else:
                    return self._get_fallback_wisdom(text, style)
        except Exception as e:
            print(f"Error generating wisdom with {provider}: {e}")
            return self._get_fallback_wisdom(text, style)
        finally:
            processing_time = time.time() - start_time
    
    def _generate_with_openai(self, text: str, style: str) -> Tuple[str, float, str]:
        """Generate wisdom using OpenAI"""
        openai.api_key = self.providers["openai"].api_key
        
        prompt = self._build_prompt(text, style)
        
        response = openai.ChatCompletion.create(
            model=self.providers["openai"].model,
            messages=[
                {"role": "system", "content": "You are WitMirror, a wise AI that turns negativity into enlightenment through elegant proverbs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.providers["openai"].max_tokens,
            temperature=self.providers["openai"].temperature
        )
        
        wisdom = response.choices[0].message.content.strip()
        return wisdom, 0.95, "openai"
    
    def _generate_with_anthropic(self, text: str, style: str) -> Tuple[str, float, str]:
        """Generate wisdom using Anthropic Claude"""
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.providers["anthropic"].api_key)
        prompt = self._build_prompt(text, style)
        
        response = client.messages.create(
            model=self.providers["anthropic"].model,
            max_tokens=self.providers["anthropic"].max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        wisdom = response.content[0].text.strip()
        return wisdom, 0.9, "anthropic"
    
    def _generate_with_ollama(self, text: str, style: str) -> Tuple[str, float, str]:
        """Generate wisdom using local Ollama"""
        url = f"{self.providers['ollama'].base_url}/api/generate"
        prompt = self._build_prompt(text, style)
        
        payload = {
            "model": self.providers["ollama"].model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": self.providers["ollama"].max_tokens
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        wisdom = result.get("response", "").strip()
        return wisdom, 0.8, "ollama"
    
    def _build_prompt(self, text: str, style: str) -> str:
        """Build prompt for AI generation"""
        style_prompts = {
            "classic": "Respond with a classic proverb or wise saying",
            "stoic": "Respond with Stoic philosophy wisdom",
            "zen": "Respond with Zen Buddhist wisdom",
            "sufi": "Respond with Sufi mystical wisdom",
            "sarcastic": "Respond with witty, slightly sarcastic wisdom",
            "poetic": "Respond with poetic, lyrical wisdom",
            "scientific": "Respond with scientifically-informed wisdom",
            "humorous": "Respond with light-hearted, humorous wisdom"
        }
        
        prompt = f"""
        You are WitMirror, an AI that turns negativity into wisdom.
        
        Original comment: "{text}"
        
        {style_prompts.get(style, style_prompts['classic'])} that reflects this person's behavior back to them with calm, elegant wisdom.
        
        Requirements:
        - Keep it under 20 words
        - Use elegant, timeless language
        - Don't be preachy or condescending
        - Make it feel like ancient wisdom
        - Subtly mirror their tone back to them
        - Be contextually appropriate
        
        Respond with ONLY the wisdom saying, no quotes or attribution.
        """
        
        return prompt
    
    def _get_fallback_wisdom(self, text: str, style: str) -> Tuple[str, float, str]:
        """Fallback wisdom responses"""
        wisdom_database = {
            "classic": [
                "The mirror often blames the face it reflects.",
                "Politeness is free; rudeness always collects interest.",
                "A gentle word turns away wrath, but harsh words stir up anger.",
                "The wise speak because they have something to say; fools speak because they have to say something.",
                "When you point a finger at others, three fingers point back at you."
            ],
            "stoic": [
                "The best revenge is not to be like your enemy.",
                "You have power over your mind - not outside events. Realize this, and you will find strength.",
                "The obstacle is the way.",
                "How long are you going to wait before you demand the best for yourself?",
                "Waste no more time arguing what a good man should be. Be one."
            ],
            "zen": [
                "Before enlightenment, chop wood, carry water. After enlightenment, chop wood, carry water.",
                "The moon does not fight. It attacks no one. It does not worry. It does not try to crush others.",
                "If you understand, things are just as they are; if you do not understand, things are just as they are.",
                "The mind is everything. What you think you become.",
                "Peace comes from within. Do not seek it without."
            ],
            "sufi": [
                "The wound is the place where the Light enters you.",
                "Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.",
                "Be like a tree and let the dead leaves drop.",
                "The minute I heard my first love story, I started looking for you, not knowing how blind that was.",
                "What you seek is seeking you."
            ],
            "sarcastic": [
                "The empty vessel makes the loudest sound.",
                "Some people are like clouds. When they disappear, it's a brighter day.",
                "The problem with common sense is that it's not very common.",
                "I'm not arguing, I'm just explaining why I'm right.",
                "The best way to appreciate your job is to imagine yourself without one."
            ]
        }
        
        import random
        wisdom_list = wisdom_database.get(style, wisdom_database["classic"])
        wisdom = random.choice(wisdom_list)
        return wisdom, 0.5, "fallback"
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        return list(self.providers.keys())
    
    def get_provider_info(self, provider: str) -> Optional[Dict]:
        """Get information about a specific provider"""
        if provider in self.providers:
            p = self.providers[provider]
            return {
                "name": p.name,
                "model": p.model,
                "max_tokens": p.max_tokens,
                "temperature": p.temperature
            }
        return None

# Global AI service manager
ai_service = AIServiceManager()
