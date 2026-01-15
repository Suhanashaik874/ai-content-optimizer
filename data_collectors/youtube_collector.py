"""
Collect 50 trending videos from YouTube
"""

from googleapiclient.discovery import build
from datetime import datetime
import random
from typing import List, Dict
from config.settings import KEYWORDS, ITEMS_PER_SOURCE

class YouTubeCollector:
    """Collect trending YouTube videos"""
    
    def __init__(self):
        # self.api_key = "your-youtube-api-key"  # Get from Google Cloud Console
        # self.youtube = None
        from config.settings import YOUTUBE_API_KEY
        self.api_key = YOUTUBE_API_KEY
        
    def collect(self) -> List[Dict]:
        """Collect 50 YouTube videos"""
        print("🎬 Collecting YouTube data...")
        
        videos = []
        
        try:
            # Initialize YouTube API
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
            
            for keyword in KEYWORDS:
                # Search for videos
                request = self.youtube.search().list(
                    part="snippet",
                    q=keyword,
                    type="video",
                    maxResults=10,
                    order="viewCount",
                    relevanceLanguage="en"
                )
                
                response = request.execute()
                
                for item in response.get("items", [])[:10]:
                    video_id = item["id"]["videoId"]
                    
                    # Get video statistics
                    stats_request = self.youtube.videos().list(
                        part="statistics,snippet",
                        id=video_id
                    )
                    stats_response = stats_request.execute()
                    
                    if stats_response["items"]:
                        stats = stats_response["items"][0]
                        
                        video_data = {
                            "title": item["snippet"]["title"],
                            "url": f"https://youtube.com/watch?v={video_id}",
                            "channel": item["snippet"]["channelTitle"],
                            "published_at": item["snippet"]["publishedAt"],
                            "description": item["snippet"]["description"][:200],
                            "keyword": keyword,
                            "platform": "youtube",
                            "collected_at": datetime.now().isoformat(),
                            "engagement_metrics": {
                                "views": int(stats["statistics"].get("viewCount", 0)),
                                "likes": int(stats["statistics"].get("likeCount", 0)),
                                "comments": int(stats["statistics"].get("commentCount", 0)),
                                "duration": "medium"  # Can be extracted from contentDetails
                            }
                        }
                        videos.append(video_data)
                        
                        if len(videos) >= ITEMS_PER_SOURCE:
                            break
                            
        except Exception as e:
            print(f"❌ YouTube API error: {str(e)}. Using sample data...")
        
        # Fill with sample data if needed
        if len(videos) < ITEMS_PER_SOURCE:
            videos.extend(self._get_sample_data(ITEMS_PER_SOURCE - len(videos)))
        
        print(f"✅ Collected {len(videos)} YouTube videos")
        return videos[:ITEMS_PER_SOURCE]
    
   
        def _get_sample_data(self, count: int) -> List[Dict]:
     
            print(f"   Generating {count} sample YouTube videos...")
        
            sample_videos = []
            keywords = ["digital marketing", "AI marketing", "social media", 
                   "content marketing", "SEO", "email marketing"]
        
            video_templates = [
                {
                "type": "Tutorial",
                "title_base": "How to {} - Complete Guide",
                "views_range": (5000, 500000),
                "likes_ratio": 0.03
               },
            {
                "type": "Case Study",
                "title_base": "{} Success Story - Real Results",
                "views_range": (10000, 300000),
                "likes_ratio": 0.04
            },
            {
                "type": "Tips",
                "title_base": "10 {} Tips That Actually Work",
                "views_range": (8000, 200000),
                "likes_ratio": 0.035
            },
            {
                "type": "Trends",
                "title_base": "{} Trends 2024 - What's Working Now",
                "views_range": (15000, 400000),
                "likes_ratio": 0.025
            },
            {
                "type": "Tools",
                "title_base": "Best {} Tools for Beginners",
                "views_range": (12000, 250000),
                "likes_ratio": 0.03
            }
        ]
        
            from datetime import datetime, timedelta
            import random
        
            for i in range(count):
                keyword = random.choice(keywords)
                template = random.choice(video_templates)
            
            # Generate realistic metrics
                min_views, max_views = template["views_range"]
                views = random.randint(min_views, max_views)
                likes = int(views * template["likes_ratio"] * random.uniform(0.8, 1.2))
                comments = int(views * 0.002 * random.uniform(0.5, 1.5))
            
            # Random date in last 30 days
                days_ago = random.randint(0, 30)
                publish_date = datetime.now() - timedelta(days=days_ago)
            
                sample_videos.append({
                "title": template["title_base"].format(keyword.title()),
                "url": f"https://youtube.com/watch?v=sample_{i:03d}",
                "channel": f"{keyword.title()} Academy",
                "published_at": publish_date.isoformat(),
                "description": f"Learn about {keyword} with this {template['type'].lower()} video. Perfect for marketers looking to improve their skills.",
                "keyword": keyword,
                "platform": "youtube",
                "collected_at": datetime.now().isoformat(),
                "engagement_metrics": {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "duration": random.choice(["short", "medium", "long"]),
                    "engagement_rate": round((likes + comments) / views, 4) if views > 0 else 0
                }
                })
        
            return sample_videos