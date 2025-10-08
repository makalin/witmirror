import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

interface AnalysisRequest {
  text: string;
}

interface AnalysisResponse {
  analysis: {
    sentiment: 'negative' | 'neutral' | 'positive';
    confidence: number;
    detected_emotions: string[];
    toxicity_score: number;
  };
  wisdom: string;
}

// Fallback wisdom responses for demo purposes
const wisdomDatabase = [
  "The mirror often blames the face it reflects.",
  "Politeness is free; rudeness always collects interest.",
  "A gentle word turns away wrath, but harsh words stir up anger.",
  "The wise speak because they have something to say; fools speak because they have to say something.",
  "When you point a finger at others, three fingers point back at you.",
  "The empty vessel makes the loudest sound.",
  "Wisdom is the reward for a lifetime of listening when you would have preferred to talk.",
  "The best way to win an argument is to avoid it.",
  "Kindness is a language that the deaf can hear and the blind can see.",
  "The tongue has no bones, but it can break hearts.",
  "A soft answer turns away wrath, but a harsh word stirs up anger.",
  "The wise find pleasure in water; the virtuous find pleasure in hills.",
  "When you are right, you have no need to be angry; when you are wrong, you have no right to be angry.",
  "The greatest victory is that which requires no battle.",
  "He who knows others is wise; he who knows himself is enlightened.",
  "The best time to plant a tree was 20 years ago. The second best time is now.",
  "In the end, we will remember not the words of our enemies, but the silence of our friends.",
  "Be the change you wish to see in the world.",
  "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.",
  "When you have nothing to say, say nothing."
];

function analyzeText(text: string) {
  const lowerText = text.toLowerCase();
  
  // Simple sentiment analysis
  const negativeWords = [
    'stupid', 'dumb', 'idiot', 'moron', 'garbage', 'trash', 'worthless', 
    'hate', 'terrible', 'awful', 'horrible', 'disgusting', 'pathetic',
    'sucks', 'suck', 'screams', 'slop', 'dumbest', 'worst', 'hate'
  ];
  
  const toxicWords = [
    'kill', 'die', 'death', 'murder', 'violence', 'attack', 'destroy'
  ];
  
  const sarcasticIndicators = [
    'obviously', 'clearly', 'surely', 'of course', 'naturally'
  ];
  
  let sentiment: 'negative' | 'neutral' | 'positive' = 'neutral';
  let confidence = 0.5;
  let detectedEmotions: string[] = [];
  let toxicityScore = 0;
  
  // Check for negative sentiment
  const negativeCount = negativeWords.filter(word => lowerText.includes(word)).length;
  const toxicCount = toxicWords.filter(word => lowerText.includes(word)).length;
  const sarcasticCount = sarcasticIndicators.filter(word => lowerText.includes(word)).length;
  
  if (negativeCount > 0 || toxicCount > 0) {
    sentiment = 'negative';
    confidence = Math.min(0.9, 0.5 + (negativeCount * 0.1) + (toxicCount * 0.2));
    
    if (negativeCount > 0) detectedEmotions.push('anger', 'contempt');
    if (toxicCount > 0) {
      detectedEmotions.push('hostility', 'aggression');
      toxicityScore = Math.min(1.0, toxicCount * 0.3);
    }
    if (sarcasticCount > 0) detectedEmotions.push('sarcasm');
  }
  
  // Check for positive sentiment
  const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like'];
  const positiveCount = positiveWords.filter(word => lowerText.includes(word)).length;
  
  if (positiveCount > negativeCount && positiveCount > 0) {
    sentiment = 'positive';
    confidence = Math.min(0.9, 0.5 + (positiveCount * 0.1));
    detectedEmotions.push('joy', 'satisfaction');
  }
  
  return {
    sentiment,
    confidence,
    detected_emotions: detectedEmotions,
    toxicity_score: toxicityScore
  };
}

function generateWisdom(analysis: any, originalText: string): string {
  // For demo purposes, return a random wisdom response
  // In production, this would use AI to generate contextually appropriate wisdom
  const randomIndex = Math.floor(Math.random() * wisdomDatabase.length);
  return wisdomDatabase[randomIndex];
}

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { text }: AnalysisRequest = await request.json();
    
    if (!text || text.trim().length === 0) {
      return json({ error: 'Text is required' }, { status: 400 });
    }
    
    // Analyze the text
    const analysis = analyzeText(text);
    
    // Generate wisdom response
    const wisdom = generateWisdom(analysis, text);
    
    const response: AnalysisResponse = {
      analysis,
      wisdom
    };
    
    return json(response);
    
  } catch (error) {
    console.error('Error analyzing text:', error);
    return json({ error: 'Internal server error' }, { status: 500 });
  }
};
