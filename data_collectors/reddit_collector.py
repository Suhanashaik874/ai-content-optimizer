"""
Collect 50 posts from Reddit (using sample data)
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict
from config.settings import KEYWORDS, ITEMS_PER_SOURCE

class RedditCollector:
    """Collect Reddit posts (sample data)"""
    
    def __init__(self):
        print("📱 Using sample Reddit data (API not available)")
    
    def collect(self) -> List[Dict]:
        """Collect 50 Reddit posts (sample data)"""
        print("📱 Collecting Reddit data...")
        
        posts = []
        subreddits = [
            "marketing", "digital_marketing", "socialmedia", 
            "content_marketing", "SEO", "PPC"
        ]
        
        post_types = [
        ("Question", "How do I...", 15, 8),
        ("Success Story", "I increased...", 250, 75),
        ("Discussion", "What's your opinion on...", 120, 25),
        ("Guide", "Complete guide to...", 450, 60),
        ("News", "Latest update about...", 80, 15)
       ]
        
        for i in range(ITEMS_PER_SOURCE):
            subreddit = random.choice(subreddits)
            ptype, title_base, upvotes_base, comments_base = random.choice(post_types)
            keyword = random.choice(KEYWORDS)
            
            # Random date in last 7 days
            days_ago = random.randint(0, 7)
            post_date = datetime.now() - timedelta(days=days_ago)
            
            posts.append({
                "title": f"{title_base} {keyword}?",
                "url": f"https://reddit.com/r/{subreddit}/sample{i}",
                "subreddit": subreddit,
                "published_at": post_date.isoformat(),
                "content": f"Discussion about {keyword} in the context of {ptype.lower()}...",
                "keyword": keyword,
                "platform": "reddit",
                "collected_at": datetime.now().isoformat(),
                "engagement_metrics": {
                    "upvotes": upvotes_base + random.randint(-20, 50),
                    "comments": comments_base + random.randint(-5, 20),
                    "awards": random.randint(0, 3),
                    "score": random.randint(50, 1000),
                    "sentiment": random.choice(["positive", "neutral", "controversial"])
                }
            })
        
        print(f"✅ Collected {len(posts)} Reddit posts (sample data)")
        return posts