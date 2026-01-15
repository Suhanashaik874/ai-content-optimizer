#!/usr/bin/env python3
"""
QUICK FIX for Groq model issue
"""

import os
import sys

print("🔧 Applying quick fix for Groq model deprecation...")

# 1. Create the new content generator
new_code = '''"""
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
                        "content": f"Topic: {topic}\\nPlatform: {platform}\\nMake it engaging and data-driven."
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
'''

# Save the new file
with open("simple_content_generator.py", "w") as f:
    f.write(new_code)

print("✅ Created simple_content_generator.py")

# 2. Update main.py to use it
try:
    with open("main.py", "r") as f:
        main_content = f.read()
    
    # Find and replace the import
    if "from milestone_2.content_generator import ContentGenerator" in main_content:
        main_content = main_content.replace(
            "from milestone_2.content_generator import ContentGenerator",
            "from simple_content_generator import ContentGenerator"
        )
        print("✅ Updated main.py imports")
    elif "from content_generator import ContentGenerator" in main_content:
        main_content = main_content.replace(
            "from content_generator import ContentGenerator",
            "from simple_content_generator import ContentGenerator"
        )
        print("✅ Updated main.py imports")
    else:
        print("⚠️  Could not find import in main.py")
        print("   Manually change the import in main.py to:")
        print("   from simple_content_generator import ContentGenerator")
    
    with open("main.py", "w") as f:
        f.write(main_content)

except Exception as e:
    print(f"❌ Error updating main.py: {e}")

print("\n🎉 Fix applied!")
print("\nNow run:")
print("python main.py")
print("\nChoose Option 2 to generate content!")