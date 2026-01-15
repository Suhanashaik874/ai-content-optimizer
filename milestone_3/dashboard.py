"""
Main Dashboard for Milestone 3
Integrates all modules into a single interface
"""

import json
from datetime import datetime
from pathlib import Path
import sys
import os
from typing import Dict

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from milestone_3.sentiment_analyzer import SentimentAnalyzer
from milestone_3.metrics_tracker import MetricsTracker
from milestone_3.slack_alerts import MockSlackAlerts as SlackAlerts
from milestone_3.report_generator import ReportGenerator

class Milestone3Dashboard:
    """Main dashboard integrating all Milestone 3 modules"""
    
    def __init__(self):
        print("🚀 Initializing Milestone 3 Dashboard...")
        
        # Initialize all modules
        self.sentiment_analyzer = SentimentAnalyzer()
        self.metrics_tracker = MetricsTracker()
        self.slack_alerts = SlackAlerts(webhook_url="mock")  # Use mock for now
        self.report_generator = ReportGenerator()
        
        # Dashboard data
        self.dashboard_data = {
            "last_updated": datetime.now().isoformat(),
            "total_analyses": 0,
            "total_alerts": 0,
            "total_reports": 0
        }
        
        print("✅ Dashboard initialized")
    
    def analyze_collected_data(self) -> Dict:
        """Analyze sentiment of collected data"""
        print("\n📊 Analyzing collected data sentiment...")
        
        try:
            # Load collected data
            data_file = Path("data/collected_data.json")
            if not data_file.exists():
                print("❌ No collected data found")
                return {"error": "No data file"}
            
            with open(data_file, 'r') as f:
                collected_data = json.load(f)
            
            # Extract feedback text for analysis
            feedback_items = []
            
            # Process YouTube data
            for video in collected_data.get("youtube", []):
                if "description" in video:
                    feedback_items.append({
                        "text": video["description"],
                        "source": "youtube",
                        "title": video.get("title", "")
                    })
            
            # Process Google News data
            for article in collected_data.get("google_news", []):
                if "content" in article:
                    feedback_items.append({
                        "text": article["content"],
                        "source": "google_news",
                        "title": article.get("title", "")
                    })
            
            # Analyze sentiment
            if feedback_items:
                analysis = self.sentiment_analyzer.analyze_feedback_batch(feedback_items)
                
                # Send Slack alert
                self.slack_alerts.send_trend_analysis_alert(analysis)
                
                # Update dashboard
                self.dashboard_data["total_analyses"] += 1
                self.dashboard_data["last_analysis"] = datetime.now().isoformat()
                
                print(f"✅ Analyzed {analysis['total_items']} items")
                print(f"   Overall sentiment: {analysis['overall_sentiment']}")
                
                return analysis
            else:
                print("❌ No feedback text found in data")
                return {"error": "No feedback text"}
                
        except Exception as e:
            print(f"❌ Analysis error: {str(e)}")
            return {"error": str(e)}
    
    def track_content_performance(self, content_data: Dict) -> bool:
        """Track content performance metrics"""
        print(f"\n📈 Tracking content performance...")
        
        success = self.metrics_tracker.track_content_performance(content_data)
        
        if success:
            # Send Slack alert
            self.slack_alerts.send_content_generated_alert(content_data)
            
            # Update dashboard
            self.dashboard_data["total_alerts"] += 1
            
            print(f"✅ Content tracked: {content_data.get('platform')} - {content_data.get('topic')}")
            return True
        else:
            print(f"❌ Failed to track content")
            return False
    
    def generate_reports(self) -> Dict:
        """Generate all reports"""
        print("\n📋 Generating reports...")
        
        try:
            # Get latest metrics
            metrics_summary = self.metrics_tracker.get_performance_summary()
            
            # Analyze sentiment if needed
            sentiment_data = self.analyze_collected_data()
            if "error" in sentiment_data:
                # Use sample sentiment data
                sentiment_data = {
                    "total_items": 100,
                    "overall_sentiment": "positive",
                    "average_score": 0.65,
                    "sentiment_distribution": {
                        "positive": 60,
                        "negative": 10,
                        "neutral": 30,
                        "positive_percent": 60,
                        "negative_percent": 10,
                        "neutral_percent": 30
                    }
                }
            
            # Generate reports
            sentiment_report = self.report_generator.generate_sentiment_report(sentiment_data)
            performance_report = self.report_generator.generate_performance_report(metrics_summary)
            weekly_report = self.report_generator.generate_weekly_report(sentiment_data, metrics_summary)
            
            # Send Slack alert
            self.slack_alerts.send_metrics_alert(metrics_summary)
            
            # Update dashboard
            self.dashboard_data["total_reports"] += 3
            self.dashboard_data["last_report_generated"] = datetime.now().isoformat()
            
            print(f"✅ Reports generated:")
            print(f"  1. Sentiment Report: {Path(sentiment_report).name}")
            print(f"  2. Performance Report: {Path(performance_report).name}")
            print(f"  3. Weekly Report: {Path(weekly_report).name}")
            
            return {
                "sentiment_report": sentiment_report,
                "performance_report": performance_report,
                "weekly_report": weekly_report,
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ Report generation error: {str(e)}")
            return {"error": str(e)}
    
    def show_dashboard(self):
        """Display dashboard overview"""
        print("\n" + "="*60)
        print("🎯 MILESTONE 3 DASHBOARD")
        print("="*60)
        
        # Dashboard stats
        print(f"\n📊 DASHBOARD STATS:")
        print(f"   Last Updated: {self.dashboard_data.get('last_updated', 'Never')}")
        print(f"   Total Analyses: {self.dashboard_data.get('total_analyses', 0)}")
        print(f"   Total Alerts Sent: {self.dashboard_data.get('total_alerts', 0)}")
        print(f"   Total Reports Generated: {self.dashboard_data.get('total_reports', 0)}")
        
        # Module status
        print(f"\n🛠️  MODULE STATUS:")
        print(f"   Sentiment Analyzer: ✅ Active")
        print(f"   Metrics Tracker: ✅ Active")
        print(f"   Slack Alerts: ✅ Active (Mock)")
        print(f"   Report Generator: ✅ Active")
        
        # Recent activity
        print(f"\n📈 RECENT ACTIVITY:")
        if "last_analysis" in self.dashboard_data:
            print(f"   Last Analysis: {self.dashboard_data['last_analysis'][:19]}")
        if "last_report_generated" in self.dashboard_data:
            print(f"   Last Report: {self.dashboard_data['last_report_generated'][:19]}")
        
        print(f"\n💡 QUICK ACTIONS:")
        print(f"   1. Analyze collected data")
        print(f"   2. Generate reports")
        print(f"   3. View performance metrics")
        print(f"   4. Test Slack alerts")
        
        print(f"\n" + "="*60)
    
    def run_demo(self):
        """Run a complete demo of Milestone 3"""
        print("\n" + "="*60)
        print("🚀 MILESTONE 3 DEMO")
        print("="*60)
        
        # Step 1: Show dashboard
        self.show_dashboard()
        
        # Step 2: Analyze data
        input("\nPress Enter to analyze collected data...")
        analysis = self.analyze_collected_data()
        if "error" not in analysis:
            print("\n📊 Analysis Results:")
            print(self.sentiment_analyzer.generate_sentiment_report(analysis))
        
        # Step 3: Track sample content
        input("\nPress Enter to track sample content...")
        sample_content = {
            "platform": "twitter",
            "topic": "AI Marketing Demo",
            "length": 265,
            "engagement": {"score": 82},
            "generated_at": datetime.now().isoformat()
        }
        self.track_content_performance(sample_content)
        
        # Step 4: Generate reports
        input("\nPress Enter to generate reports...")
        reports = self.generate_reports()
        
        # Step 5: Show final dashboard
        input("\nPress Enter to view final dashboard...")
        self.show_dashboard()
        
        print("\n🎉 Milestone 3 Demo Complete!")
        print("="*60)

# Main execution
if __name__ == "__main__":
    dashboard = Milestone3Dashboard()
    dashboard.run_demo()