"""
COMPLETE FIX: Content Generator with Working Groq Models
"""

from openai import OpenAI
from typing import Dict, List
import json
from config.settings import GROQ_API_KEY, PLATFORM_LIMITS

class ContentGeneratorNew:
    """Generate content using working Groq models"""
    
    def __init__(self):
        # Check API key
        if not GROQ_API_KEY or GROQ_API_KEY == "your-actual-groq-api-key-here":
            print("⚠️  GROQ_API_KEY not set in config/settings.py")
            print("   Get free key from: https://console.groq.com")
        
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # WORKING GROQ MODELS (November 2024)
        self.models = [
            "llama-3.3-70b-versatile",     # Most capable
            "llama-3.2-90b-vision-preview", # Large context
            "llama-3.2-11b-vision-preview", # Balanced
            "gemma2-9b-it",                # Alternative
            "llama-3.2-3b-preview",        # Fast
            "llama-3.2-1b-preview"         # Fastest
        ]
        
        print("🤖 Content Generator initialized")
    
    def generate(self, topic: str, platform: str, insights: Dict) -> Dict:
        """
        Generate content - tries multiple models until success
        """
        print(f"\n🚀 Generating {platform} content about: {topic}")
        
        # Create prompt
        prompt = self._create_prompt(topic, platform, insights)
        print(f"📝 Created prompt ({len(prompt)} chars)")
        
        # Try each model
        for model in self.models:
            try:
                print(f"   Trying model: {model}")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert marketing content creator."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=PLATFORM_LIMITS.get(platform, 300),
                    temperature=0.7
                )
                
                content = response.choices[0].message.content.strip()
                
                print(f"   ✅ Success! Generated {len(content)} chars")
                
                return {
                    "success": True,
                    "content": content,
                    "topic": topic,
                    "platform": platform,
                    "model_used": model,
                    "length": len(content),
                    "max_length": PLATFORM_LIMITS.get(platform, 300)
                }
                
            except Exception as e:
                error_str = str(e)
                if "model_decommissioned" in error_str or "not found" in error_str:
                    print(f"   ⚠️  Model {model} not available")
                    continue
                elif "quota" in error_str.lower() or "limit" in error_str.lower():
                    print(f"   ⚠️  Quota limit for {model}")
                    continue
                else:
                    print(f"   ❌ Error with {model}: {error_str[:50]}...")
                    continue
        
        # If all models fail, use template
        print("   ⚠️  All models failed, using template")
        return {
            "success": False,
            "content": self._generate_template(topic, platform, insights),
            "topic": topic,
            "platform": platform,
            "model_used": "template",
            "length": 0
        }
    
    def _create_prompt(self, topic: str, platform: str, insights: Dict) -> str:
        """Create optimized prompt"""
        
        # Platform instructions
        platform_instructions = {
            "twitter": "Create a tweet (max 280 characters). Use 1-3 relevant hashtags. Make it engaging and shareable.",
            "linkedin": "Create a professional LinkedIn post. Share insights and encourage discussion.",
            "blog": "Create a blog post introduction. Make it informative and engaging.",
            "instagram": "Create an Instagram caption. Use emojis and be conversational."
        }
        
        # Get insights
        time_insight = self._extract_time_insight(insights, platform)
        keyword_insight = self._extract_keyword_insight(insights)
        
        prompt = f"""
        {platform_instructions.get(platform, "Create engaging marketing content")}
        
        Topic: {topic}
        
        Data Insights to incorporate:
        1. {time_insight}
        2. {keyword_insight}
        3. Content with data references performs 40% better
        
        Requirements:
        - Platform-appropriate format
        - Include relevant hashtags if suitable
        - Add a clear call-to-action
        - Reference data/trends naturally
        
        Generate the content now:
        """
        
        return prompt
    
    def _extract_time_insight(self, insights: Dict, platform: str) -> str:
        """Extract posting time insight"""
        times = insights.get("best_posting_times", {}).get(platform, {})
        if times and times.get("best_time_range"):
            return f"Best posting time: {times['best_time_range']}"
        return "Post during business hours (9 AM - 5 PM)"
    
    def _extract_keyword_insight(self, insights: Dict) -> str:
        """Extract keyword insight"""
        viral = insights.get("viral_content_patterns", {}).get("common_keywords_in_viral", [])
        if viral:
            return f"Trending keywords: {', '.join(viral[:3])}"
        return "Focus on value-driven content"
    
    def _generate_template(self, topic: str, platform: str, insights: Dict) -> str:
        """Generate template-based content"""
        
        viral_keywords = insights.get("viral_content_patterns", {}).get("common_keywords_in_viral", ["marketing", "digital", "trends"])
        
        templates = {
            "twitter": f"📈 {topic} insights!\n\nData shows {viral_keywords[0] if viral_keywords else 'marketing'} trends evolving.\n\n💡 Key takeaway: Stay updated!\n\n#{topic.replace(' ', '')} #Marketing #Data",
            "linkedin": f"Professional perspective on {topic}:\n\nRecent analysis reveals emerging patterns in {topic.lower()}. Key finding: Data-driven approaches outperform.\n\nWhat trends are you noticing?\n\n#Business #Marketing #Strategy",
            "blog": f"# {topic.title()} Trends Analysis\n\nOur data collection reveals interesting developments in {topic.lower()}. Understanding these patterns can inform better strategies.",
            "instagram": f"✨ {topic} update! 📊\n\nData insights show new trends emerging.\n\n💭 What do you think?\n\n👇 Comment below!\n\n#{topic.replace(' ', '')} #MarketingTips"
        }
        
        return templates.get(platform, f"Content about {topic} based on data analysis.")

# Test function
def test_generator():
    """Test the content generator"""
    print("\n🧪 Testing Content Generator...")
    
    # Create test insights
    test_insights = {
        "best_posting_times": {
            "twitter": {"best_time_range": "10:00 - 14:00"},
            "linkedin": {"best_time_range": "9:00 - 17:00"}
        },
        "viral_content_patterns": {
            "common_keywords_in_viral": ["digital", "marketing", "trends"]
        }
    }
    
    generator = ContentGeneratorNew()
    result = generator.generate(
        topic="AI in marketing",
        platform="twitter",
        insights=test_insights
    )
    
    if result["success"]:
        print(f"\n✅ Test successful!")
        print(f"Model used: {result['model_used']}")
        print(f"Content:\n{result['content']}")
    else:
        print(f"\n⚠️  Test failed, using template")
        print(f"Content:\n{result['content']}")
    
    return result

if __name__ == "__main__":
    test_generator()