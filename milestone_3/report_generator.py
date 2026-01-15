"""
Automated Report Generator
Generate PDF/HTML reports from analysis data
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ReportGenerator:
    """Generate automated reports from analysis data"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_sentiment_report(self, sentiment_data: Dict, filename: str = None) -> str:
        """Generate sentiment analysis report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sentiment_report_{timestamp}.txt"
        
        filepath = self.reports_dir / filename
        
        # Extract data
        total_items = sentiment_data.get("total_items", 0)
        overall = sentiment_data.get("overall_sentiment", "neutral")
        dist = sentiment_data.get("sentiment_distribution", {})
        
        # Create report
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("SENTIMENT ANALYSIS REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary
        report_lines.append("📊 SUMMARY")
        report_lines.append(f"Total Items Analyzed: {total_items}")
        report_lines.append(f"Overall Sentiment: {overall.replace('_', ' ').title()}")
        report_lines.append(f"Average Score: {sentiment_data.get('average_score', 0.0)}")
        report_lines.append("")
        
        # Distribution
        report_lines.append("📈 DISTRIBUTION")
        report_lines.append(f"Positive: {dist.get('positive', 0)} ({dist.get('positive_percent', 0)}%)")
        report_lines.append(f"Negative: {dist.get('negative', 0)} ({dist.get('negative_percent', 0)}%)")
        report_lines.append(f"Neutral:  {dist.get('neutral', 0)} ({dist.get('neutral_percent', 0)}%)")
        report_lines.append("")
        
        # Insights
        report_lines.append("💡 INSIGHTS")
        if overall == "very_positive":
            report_lines.append("• Audience response is overwhelmingly positive")
            report_lines.append("• Content strategy is working effectively")
            report_lines.append("• Consider scaling successful approaches")
        elif overall == "positive":
            report_lines.append("• Generally positive audience sentiment")
            report_lines.append("• Continue current content strategy")
            report_lines.append("• Monitor for any negative trends")
        elif overall == "very_negative":
            report_lines.append("• ❌ Immediate attention needed")
            report_lines.append("• Significant negative sentiment detected")
            report_lines.append("• Review content strategy and audience targeting")
        elif overall == "negative":
            report_lines.append("• Negative sentiment detected")
            report_lines.append("• Consider content adjustments")
            report_lines.append("• Analyze specific pain points")
        else:
            report_lines.append("• Neutral audience sentiment")
            report_lines.append("• Opportunity to increase engagement")
            report_lines.append("• Test different content approaches")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("End of Report")
        
        # Save report
        report_content = "\n".join(report_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Sentiment report saved: {filepath}")
        return str(filepath)
    
    def generate_performance_report(self, metrics_data: Dict, filename: str = None) -> str:
        """Generate performance metrics report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.txt"
        
        filepath = self.reports_dir / filename
        
        # Create report
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("PERFORMANCE METRICS REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overview
        report_lines.append("📊 OVERVIEW")
        report_lines.append(f"Total Content Tracked: {metrics_data.get('total_content_tracked', 0)}")
        report_lines.append(f"Platforms Used: {', '.join(metrics_data.get('platforms_used', []))}")
        report_lines.append(f"Overall Status: {metrics_data.get('overall_status', 'N/A')}")
        report_lines.append("")
        
        # Platform Statistics
        platform_stats = metrics_data.get('platform_statistics', {})
        if platform_stats:
            report_lines.append("🖥️ PLATFORM STATISTICS")
            for platform, stats in platform_stats.items():
                report_lines.append(f"\n{platform.upper()}:")
                report_lines.append(f"  • Total Posts: {stats.get('total_content', 0)}")
                report_lines.append(f"  • Avg Length: {stats.get('avg_length', 0):.0f} chars")
                if stats.get('last_posted'):
                    report_lines.append(f"  • Last Posted: {stats['last_posted'][:10]}")
            report_lines.append("")
        
        # Recent Trends
        trends = metrics_data.get('recent_trends', {})
        if trends:
            report_lines.append("📈 RECENT TRENDS (7 Days)")
            report_lines.append(f"  Content Created: {trends.get('total_content', 0)}")
            report_lines.append(f"  Avg Engagement: {trends.get('average_engagement', 0)}%")
            report_lines.append(f"  Performance: {trends.get('performance_rating', 'N/A')}")
            report_lines.append("")
            
            # Top Topics
            top_topics = trends.get('top_topics', {})
            if top_topics:
                report_lines.append("🔥 TOP TOPICS")
                for topic, count in list(top_topics.items())[:5]:
                    report_lines.append(f"  • {topic}: {count} posts")
                report_lines.append("")
        
        # Recommendations
        report_lines.append("🎯 RECOMMENDATIONS")
        
        total_content = metrics_data.get('total_content_tracked', 0)
        if total_content == 0:
            report_lines.append("• Start generating content to track performance")
        elif total_content < 10:
            report_lines.append("• Continue content generation to gather more data")
            report_lines.append("• Experiment with different content formats")
        elif total_content < 50:
            report_lines.append("• Good content volume, focus on quality")
            report_lines.append("• Analyze which topics perform best")
            report_lines.append("• Optimize posting times based on engagement")
        else:
            report_lines.append("• Excellent content volume")
            report_lines.append("• Consider A/B testing different approaches")
            report_lines.append("• Scale successful content strategies")
            report_lines.append("• Explore new platforms for expansion")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("End of Report")
        
        # Save report
        report_content = "\n".join(report_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Performance report saved: {filepath}")
        return str(filepath)
    
    def generate_weekly_report(self, 
                               sentiment_data: Dict,
                               metrics_data: Dict,
                               filename: str = None) -> str:
        """Generate comprehensive weekly report"""
        if not filename:
            week_start = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
            week_end = datetime.now().strftime("%Y%m%d")
            filename = f"weekly_report_{week_start}_{week_end}.txt"
        
        filepath = self.reports_dir / filename
        
        # Create comprehensive report
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("WEEKLY ANALYTICS REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Period: {datetime.now().strftime('%Y-%m-%d')}")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("📋 EXECUTIVE SUMMARY")
        report_lines.append(f"Content Generated: {metrics_data.get('total_content_tracked', 0)}")
        report_lines.append(f"Audience Sentiment: {sentiment_data.get('overall_sentiment', 'neutral').replace('_', ' ').title()}")
        report_lines.append("")
        
        # Section 1: Sentiment Analysis
        report_lines.append("1. AUDIENCE SENTIMENT ANALYSIS")
        report_lines.append("-" * 40)
        dist = sentiment_data.get("sentiment_distribution", {})
        report_lines.append(f"Positive Feedback: {dist.get('positive_percent', 0)}%")
        report_lines.append(f"Negative Feedback: {dist.get('negative_percent', 0)}%")
        report_lines.append(f"Neutral Feedback: {dist.get('neutral_percent', 0)}%")
        report_lines.append("")
        
        # Section 2: Performance Metrics
        report_lines.append("2. PERFORMANCE METRICS")
        report_lines.append("-" * 40)
        report_lines.append(f"Total Activities: {metrics_data.get('total_content_tracked', 0)}")
        
        platform_stats = metrics_data.get('platform_statistics', {})
        if platform_stats:
            report_lines.append("\nPlatform Breakdown:")
            for platform, stats in platform_stats.items():
                report_lines.append(f"  {platform.upper()}: {stats.get('total_content', 0)} posts")
        report_lines.append("")
        
        # Section 3: Key Insights
        report_lines.append("3. KEY INSIGHTS & RECOMMENDATIONS")
        report_lines.append("-" * 40)
        
        # Insights based on data
        sentiment_score = sentiment_data.get('average_score', 0)
        if sentiment_score > 0.3:
            report_lines.append("• Strong positive audience reception")
            report_lines.append("• Current strategy is effective")
        elif sentiment_score > 0:
            report_lines.append("• Generally positive feedback")
            report_lines.append("• Room for improvement in engagement")
        elif sentiment_score < -0.3:
            report_lines.append("• ❌ Negative sentiment requires attention")
            report_lines.append("• Immediate strategy review recommended")
        else:
            report_lines.append("• Neutral audience response")
            report_lines.append("• Opportunity to enhance content appeal")
        
        report_lines.append("")
        report_lines.append("4. NEXT WEEK'S FOCUS")
        report_lines.append("-" * 40)
        report_lines.append("• Continue tracking performance metrics")
        report_lines.append("• Monitor sentiment trends daily")
        report_lines.append("• Experiment with 2-3 new content approaches")
        report_lines.append("• Review and optimize posting schedule")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("Report generated by Marketing Content Optimizer")
        
        # Save report
        report_content = "\n".join(report_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Weekly report saved: {filepath}")
        return str(filepath)

# Import timedelta for weekly reports
from datetime import timedelta

# Test function
def test_report_generator():
    """Test report generator"""
    generator = ReportGenerator()
    
    # Sample data
    sentiment_data = {
        "total_items": 150,
        "overall_sentiment": "positive",
        "average_score": 0.45,
        "sentiment_distribution": {
            "positive": 80,
            "negative": 20,
            "neutral": 50,
            "positive_percent": 53.3,
            "negative_percent": 13.3,
            "neutral_percent": 33.3
        }
    }
    
    metrics_data = {
        "total_content_tracked": 45,
        "platforms_used": ["twitter", "linkedin"],
        "platform_statistics": {
            "twitter": {
                "total_content": 30,
                "avg_length": 245,
                "last_posted": "2024-11-25T10:30:00"
            },
            "linkedin": {
                "total_content": 15,
                "avg_length": 890,
                "last_posted": "2024-11-24T14:20:00"
            }
        },
        "recent_trends": {
            "total_content": 12,
            "average_engagement": 68.5,
            "performance_rating": "Good",
            "top_topics": {
                "AI Marketing": 5,
                "Social Media": 4,
                "Content Strategy": 3
            }
        }
    }
    
    # Generate reports
    print("Testing Report Generator...")
    sentiment_report = generator.generate_sentiment_report(sentiment_data)
    performance_report = generator.generate_performance_report(metrics_data)
    weekly_report = generator.generate_weekly_report(sentiment_data, metrics_data)
    
    print(f"\n✅ Reports generated:")
    print(f"  1. {sentiment_report}")
    print(f"  2. {performance_report}")
    print(f"  3. {weekly_report}")

if __name__ == "__main__":
    test_report_generator()