#!/usr/bin/env python3
"""
MAIN PROGRAM - Complete Marketing Content System
Collects data → Analyzes trends → Generates content
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add project to path
sys.path.append(str(Path(__file__).parent))

def main():
    """Main program flow"""
    print("\n" + "="*60)
    print("🎯 AI MARKETING CONTENT OPTIMIZER")
    print("="*60)
    print("\nThis system will:")
    print("1. 📥 Collect 50 items each from YouTube, Google News, Reddit")
    print("2. 📊 Analyze trends and patterns")
    print("3. 🤖 Generate data-driven content")
    print("4. 💾 Store everything in Google Sheets")
    print("="*60)
    
    # Check API keys
    from config.settings import GROQ_API_KEY
    if GROQ_API_KEY == "":
        print("\n⚠️  WARNING: Set your Groq API key in config/settings.py")
        print("Get free key from: https://console.groq.com")
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. 🔄 Collect & Analyze Data")
        print("2. 🤖 Generate Content")
        print("3. 📊 View Trends")
        print("4. 💾 Save to Google Sheets")
        print("5. 🚪 Exit")
        print("="*60)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            collect_and_analyze()
        elif choice == "2":
            generate_content_menu()
        elif choice == "3":
            view_trends()
        elif choice == "4":
            save_to_sheets()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

def collect_and_analyze():
    """Collect data and analyze trends"""
    print("\n" + "="*60)
    print("📥 COLLECTING DATA FROM ALL SOURCES")
    print("="*60)
    
    all_data = {}
    
    try:
        # 1. Collect from Google News
        print("\n1. Collecting from Google News...")
        from data_collectors.google_news_collector import GoogleNewsCollector
        news_collector = GoogleNewsCollector()
        news_data = news_collector.collect()
        all_data["google_news"] = news_data
        
        # 2. Collect from YouTube
        print("\n2. Collecting from YouTube...")
        from data_collectors.youtube_collector import YouTubeCollector
        youtube_collector = YouTubeCollector()
        youtube_data = youtube_collector.collect()
        all_data["youtube"] = youtube_data
        
        # 3. Collect from Reddit (sample data)
        print("\n3. Collecting from Reddit...")
        from data_collectors.reddit_collector import RedditCollector
        reddit_collector = RedditCollector()
        reddit_data = reddit_collector.collect()
        all_data["reddit"] = reddit_data
        
        # Save collected data locally
        with open("data/collected_data.json", "w") as f:
            json.dump(all_data, f, indent=2, default=str)
        print("\n✅ Data saved to data/collected_data.json")
        
        # 4. Analyze trends
        print("\n" + "="*60)
        print("📊 ANALYZING TRENDS")
        print("="*60)
        
        from trend_analyzer import TrendAnalyzer
        analyzer = TrendAnalyzer(all_data)
        insights = analyzer.analyze()
        
        # Save insights
        with open("data/trend_insights.json", "w") as f:
            json.dump(insights, f, indent=2, default=str)
        
        # Show recommendations
        print("\n" + "="*60)
        print("💡 ACTIONABLE INSIGHTS")
        print("="*60)
        
        recommendations = analyzer.get_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        print(f"\n✅ Analysis saved to data/trend_insights.json")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure all required packages are installed")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def generate_content_menu():
    """Generate content based on trends"""
    print("\n" + "="*60)
    print("🤖 GENERATE DATA-DRIVEN CONTENT")
    print("="*60)
    
    try:
        # Load insights
        with open("data/trend_insights.json", "r") as f:
            insights = json.load(f)
        
        # Get topic from user
        topic = input("\nEnter topic (or press Enter for 'digital marketing'): ").strip()
        if not topic:
            topic = "digital marketing"
        
        # Select platform
        print("\nSelect platform:")
        print("1. Twitter (280 chars)")
        print("2. LinkedIn (3000 chars)")
        print("3. Instagram (2200 chars)")
        print("4. Blog (2000 chars)")
        
        choice = input("\nEnter choice (1-4): ").strip()
        platforms = {
            "1": "twitter",
            "2": "linkedin", 
            "3": "instagram",
            "4": "blog"
        }
        platform = platforms.get(choice, "twitter")
        
        # Generate content
        from content_generator_new import ContentGeneratorNew
        generator = ContentGeneratorNew()
        
        print(f"\n🚀 Generating {platform} content about '{topic}'...")
        result = generator.generate(topic, platform, insights)
        
        if result["success"]:
            print("\n" + "="*60)
            print("✨ GENERATED CONTENT")
            print("="*60)
            print(f"\n{result['content']}")
            print("\n" + "="*60)
            print(f"📏 Length: {result['length']} characters")
            print(f"🎯 Platform: {result['platform']}")
            print(f"📊 Insights used: {len(result['insights_used'])}")
            
            # Save content
            save = input("\n💾 Save this content? (y/n): ").lower()
            if save == 'y':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"results/content_{topic.replace(' ', '_')}_{timestamp}.json"
                with open(filename, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"✅ Saved to {filename}")
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            
    except FileNotFoundError:
        print("❌ No trend data found. Run 'Collect & Analyze Data' first.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def view_trends():
    """View analyzed trends"""
    print("\n" + "="*60)
    print("📊 VIEW TREND INSIGHTS")
    print("="*60)
    
    try:
        with open("data/trend_insights.json", "r") as f:
            insights = json.load(f)
        
        # Show key insights
        print("\n📈 BEST POSTING TIMES:")
        for platform, times in insights.get("best_posting_times", {}).items():
            if times.get("peak_hours"):
                print(f"  • {platform}: Post at {times['best_time_range']}")
        
        print("\n🔥 VIRAL CONTENT PATTERNS:")
        viral_keywords = insights.get("viral_content_patterns", {}).get("common_keywords_in_viral", [])
        if viral_keywords:
            print(f"  • Top keywords: {', '.join(viral_keywords[:5])}")
        
        print("\n📊 ENGAGEMENT INSIGHTS:")
        engagement = insights.get("engagement_insights", {})
        for platform, stats in engagement.items():
            if "avg_views" in stats:
                print(f"  • {platform}: {stats['avg_views']:,} avg views")
            elif "avg_upvotes" in stats:
                print(f"  • {platform}: {stats['avg_upvotes']:,} avg upvotes")
        
        print(f"\n✅ Loaded insights from data/trend_insights.json")
        
    except FileNotFoundError:
        print("❌ No trend data found. Run 'Collect & Analyze Data' first.")

def save_to_sheets():
    """Save data to Google Sheets (Fixed version)"""
    print("\n" + "="*60)
    print("💾 SAVE TO GOOGLE SHEETS (FIXED)")
    print("="*60)
    print("\n⚠️  Note: Google Sheets has quota limits")
    print("   We'll upload 30 items per platform with delays")
    print("="*60)
    
    try:
        # Load collected data
        with open("data/collected_data.json", "r", encoding='utf-8') as f:
            all_data = json.load(f)
        
        # Initialize fixed Google Sheets handler
        from google_sheets_fixed import GoogleSheetsFixed
        sheets_handler = GoogleSheetsFixed()
        
        if not sheets_handler.client:
            print("❌ Google Sheets authentication failed")
            print("\nCheck:")
            print("1. SERVICE_ACCOUNT_FILE in config/settings.py")
            print("2. Google Sheets ID is correct")
            print("3. Service account has edit permissions")
            return
        
        # Ensure we have at least 30 items per platform
        print("\n📊 Checking data counts:")
        for platform, data in all_data.items():
            count = len(data) if data else 0
            print(f"  {platform}: {count} items")
            
            if count < 30:
                print(f"  ⚠️  Need {30-count} more items")
                # You might want to generate more sample data here
        
        # Upload data (30 items per platform)
        print("\n" + "="*60)
        print("📤 STARTING UPLOAD")
        print("="*60)
        
        success = sheets_handler.upload_all_data(all_data, items_per_sheet=30)
        
        if success:
            print("\n🎉 Google Sheets upload completed!")
            print("\nCheck your Google Sheets:")
            print("1. Open your spreadsheet")
            print("2. You should see tabs: google_news, youtube, reddit")
            print("3. Each tab has 30 items of data")
        else:
            print("\n⚠️  Upload had some issues")
            print("Check the backup folder for local copies")
        
    except FileNotFoundError:
        print("❌ No data found. Run 'Collect & Analyze Data' first.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")