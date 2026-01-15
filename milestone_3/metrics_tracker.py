"""
Performance Metrics Tracker
Tracks content performance and engagement metrics
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

class MetricsTracker:
    """Track and analyze content performance metrics"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.metrics_file = self.data_dir / "performance_metrics.json"
        self._load_metrics()
    
    def _load_metrics(self):
        """Load existing metrics or initialize"""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {
                "content_performance": [],
                "platform_stats": {},
                "trend_analysis": {},
                "last_updated": datetime.now().isoformat()
            }
    
    def _save_metrics(self):
        """Save metrics to file"""
        self.metrics["last_updated"] = datetime.now().isoformat()
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def track_content_performance(self, content_data: Dict):
        """
        Track performance of generated content
        
        content_data should include:
        - platform, topic, length, engagement (if available)
        - generated_at, content_id (optional)
        """
        if not isinstance(content_data, dict):
            return False
        
        # Add tracking metadata
        tracking_entry = {
            **content_data,
            "tracked_at": datetime.now().isoformat(),
            "metrics_id": f"metric_{int(datetime.now().timestamp())}"
        }
        
        # Ensure content_performance exists
        if "content_performance" not in self.metrics:
            self.metrics["content_performance"] = []
        
        # Add to metrics
        self.metrics["content_performance"].append(tracking_entry)
        
        # Update platform stats
        platform = content_data.get("platform", "unknown")
        if platform not in self.metrics["platform_stats"]:
            self.metrics["platform_stats"][platform] = {
                "total_content": 0,
                "avg_length": 0,
                "last_posted": None
            }
        
        # Update platform statistics
        plat_stats = self.metrics["platform_stats"][platform]
        plat_stats["total_content"] += 1
        plat_stats["last_posted"] = datetime.now().isoformat()
        
        # Calculate average length
        lengths = [c.get("length", 0) for c in self.metrics["content_performance"] 
                  if c.get("platform") == platform and c.get("length")]
        if lengths:
            plat_stats["avg_length"] = sum(lengths) / len(lengths)
        
        # Save metrics
        self._save_metrics()
        return True
    
    def calculate_engagement_rate(self, views: int, interactions: int) -> float:
        """Calculate engagement rate percentage"""
        if views <= 0:
            return 0.0
        return (interactions / views) * 100
    
    def analyze_performance_trends(self, days: int = 7) -> Dict:
        """
        Analyze performance trends over specified days
        
        Returns trends and insights
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent content
        recent_content = []
        for content in self.metrics.get("content_performance", []):
            tracked_at = content.get("tracked_at", "")
            if tracked_at:
                try:
                    content_date = datetime.fromisoformat(tracked_at.replace('Z', '+00:00'))
                    if content_date >= cutoff_date:
                        recent_content.append(content)
                except:
                    continue
        
        if not recent_content:
            return {"error": "No recent content to analyze", "total": 0}
        
        # Calculate metrics
        total_content = len(recent_content)
        
        # By platform
        platform_dist = {}
        for content in recent_content:
            platform = content.get("platform", "unknown")
            platform_dist[platform] = platform_dist.get(platform, 0) + 1
        
        # Average length
        lengths = [c.get("length", 0) for c in recent_content]
        avg_length = sum(lengths) / len(lengths) if lengths else 0
        
        # Topic frequency
        topics = [c.get("topic", "unknown") for c in recent_content]
        from collections import Counter
        top_topics = Counter(topics).most_common(5)
        
        # Engagement trends (if available)
        engagement_scores = []
        for content in recent_content:
            if "engagement" in content:
                # Simple engagement score calculation
                score = content.get("engagement", {}).get("score", 0)
                engagement_scores.append(score)
        
        avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
        
        # Store trend analysis
        trend_analysis = {
            "analysis_date": datetime.now().isoformat(),
            "period_days": days,
            "total_content": total_content,
            "platform_distribution": platform_dist,
            "average_length": round(avg_length, 1),
            "top_topics": dict(top_topics),
            "average_engagement": round(avg_engagement, 2),
            "performance_rating": self._calculate_performance_rating(avg_engagement)
        }
        
        self.metrics["trend_analysis"] = trend_analysis
        self._save_metrics()
        
        return trend_analysis
    
    def _calculate_performance_rating(self, engagement_score: float) -> str:
        """Calculate performance rating"""
        if engagement_score >= 80:
            return "Excellent"
        elif engagement_score >= 60:
            return "Good"
        elif engagement_score >= 40:
            return "Average"
        else:
            return "Needs Improvement"
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary"""
        total_content = len(self.metrics.get("content_performance", []))
        
        # Platform breakdown
        platform_stats = self.metrics.get("platform_stats", {})
        
        # Recent trends
        recent_trends = self.metrics.get("trend_analysis", {})
        
        return {
            "summary_date": datetime.now().isoformat(),
            "total_content_tracked": total_content,
            "platforms_used": list(platform_stats.keys()),
            "platform_statistics": platform_stats,
            "recent_trends": recent_trends,
            "overall_status": "Active" if total_content > 0 else "Inactive"
        }
    
    def generate_metrics_report(self) -> str:
        """Generate readable metrics report"""
        summary = self.get_performance_summary()
        trends = summary.get("recent_trends", {})
        
        report = []
        report.append("📈 PERFORMANCE METRICS REPORT")
        report.append("=" * 40)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # Overview
        report.append("📊 OVERVIEW")
        report.append(f"Total Content Tracked: {summary['total_content_tracked']}")
        report.append(f"Platforms Used: {', '.join(summary['platforms_used'])}")
        report.append(f"Overall Status: {summary['overall_status']}")
        report.append("")
        
        # Platform Stats
        report.append("🖥️ PLATFORM STATISTICS")
        for platform, stats in summary.get("platform_statistics", {}).items():
            report.append(f"  {platform.upper()}:")
            report.append(f"    • Total Posts: {stats.get('total_content', 0)}")
            report.append(f"    • Avg Length: {stats.get('avg_length', 0):.0f} chars")
            report.append(f"    • Last Posted: {stats.get('last_posted', 'Never')[:10]}")
        report.append("")
        
        # Recent Trends
        if trends:
            report.append("📈 RECENT TRENDS")
            report.append(f"  Period: Last {trends.get('period_days', 7)} days")
            report.append(f"  Content Created: {trends.get('total_content', 0)}")
            report.append(f"  Avg Engagement: {trends.get('average_engagement', 0)}%")
            report.append(f"  Performance: {trends.get('performance_rating', 'N/A')}")
            report.append("")
            
            # Top topics
            top_topics = trends.get("top_topics", {})
            if top_topics:
                report.append("🔥 TOP TOPICS")
                for topic, count in list(top_topics.items())[:3]:
                    report.append(f"  • {topic}: {count} posts")
        
        return "\n".join(report)

# Test function
def test_metrics_tracker():
    """Test the metrics tracker"""
    tracker = MetricsTracker()
    
    # Sample content data
    sample_content = {
        "platform": "twitter",
        "topic": "AI Marketing",
        "length": 245,
        "generated_at": datetime.now().isoformat(),
        "engagement": {"score": 75}
    }
    
    # Track content
    success = tracker.track_content_performance(sample_content)
    print(f"Tracked content: {success}")
    
    # Analyze trends
    trends = tracker.analyze_performance_trends(7)
    print(f"\nTrend Analysis: {trends.get('total_content', 0)} items")
    
    # Generate report
    report = tracker.generate_metrics_report()
    print(f"\n{report}")

if __name__ == "__main__":
    test_metrics_tracker()