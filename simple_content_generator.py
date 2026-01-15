"""
Content Generator with Working Groq Models
"""

from openai import OpenAI
from typing import Dict, List
from config.settings import GROQ_API_KEY, PLATFORM_LIMITS

class ContentGenerator:
    """Generate content using working Groq models"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
    
    def generate(self, topic: str, platform: str, insights: Dict) -> Dict:
        """Generate content with working model"""
        try:
            # USE THIS WORKING MODEL
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # WORKING MODEL
                messages=[
                    {
                        "role": "system",
                        "content": f"Create a {platform} post about {topic}"
                    },
                    {
                        "role": "user",
                        "content": f"Topic: {topic}\nPlatform: {platform}\nMake it engaging and data-driven."
                    }
                ],
                max_tokens=PLATFORM_LIMITS.get(platform, 300),
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "content": content,
                "topic": topic,
                "platform": platform,
                "length": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"Twitter post about {topic}: Trends show growth in this area. #Marketing #{topic.replace(' ', '')}"
            }
