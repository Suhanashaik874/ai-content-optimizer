"""
Slack Alerts System
Send notifications to Slack for important events
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

class SlackAlerts:
    """Send alerts and notifications to Slack"""
    
    def __init__(self, webhook_url: str = None):
        """
        Initialize with Slack webhook URL
        
        Get webhook URL from: 
        Slack App → Incoming Webhooks → Add to Channel
        """
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
        
        if self.enabled:
            print("✅ Slack alerts enabled")
        else:
            print("⚠️  Slack alerts disabled (no webhook URL)")
    
    def send_alert(self, message: str, alert_type: str = "info") -> bool:
        """
        Send alert to Slack
        
        alert_type: info, success, warning, error
        Returns: True if successful
        """
        if not self.enabled or not self.webhook_url:
            print(f"[Slack] {alert_type.upper()}: {message}")
            return False
        
        # Alert colors
        colors = {
            "info": "#36a64f",      # Green
            "success": "#2eb67d",   # Bright Green
            "warning": "#ecb22e",   # Yellow
            "error": "#e01e5a"      # Red
        }
        
        # Create payload
        payload = {
            "text": f"🚨 *Marketing Content Alert*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{alert_type.upper()} Alert*\n{message}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
                        }
                    ]
                }
            ],
            "attachments": [
                {
                    "color": colors.get(alert_type, "#36a64f"),
                    "fields": []
                }
            ]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Slack alert sent: {alert_type}")
                return True
            else:
                print(f"❌ Slack error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Slack connection error: {str(e)}")
            return False
    
    def send_content_generated_alert(self, content_data: Dict) -> bool:
        """Send alert when new content is generated"""
        if not self.enabled:
            return False
        
        platform = content_data.get("platform", "unknown")
        topic = content_data.get("topic", "unknown topic")
        length = content_data.get("length", 0)
        
        message = f"""
🎯 *New Content Generated!*

*Platform:* {platform.upper()}
*Topic:* {topic}
*Length:* {length} characters
*Status:* ✅ Ready to publish

_Content has been optimized with data insights_
"""
        
        return self.send_alert(message, "success")
    
    def send_trend_analysis_alert(self, analysis_results: Dict) -> bool:
        """Send alert when trend analysis is complete"""
        if not self.enabled:
            return False
        
        total_items = analysis_results.get("total_items", 0)
        overall_sentiment = analysis_results.get("overall_sentiment", "neutral")
        
        message = f"""
📊 *Trend Analysis Complete*

*Items Analyzed:* {total_items}
*Overall Sentiment:* {overall_sentiment.replace('_', ' ').title()}
*Status:* 📈 Insights ready

_Check dashboard for detailed analysis_
"""
        
        return self.send_alert(message, "info")
    
    def send_metrics_alert(self, metrics_summary: Dict) -> bool:
        """Send alert with performance metrics"""
        if not self.enabled:
            return False
        
        total_content = metrics_summary.get("total_content_tracked", 0)
        platforms = len(metrics_summary.get("platforms_used", []))
        
        message = f"""
📈 *Weekly Performance Report*

*Content Tracked:* {total_content} posts
*Platforms Active:* {platforms}
*Status:* 📊 Report generated

_Download full report for detailed insights_
"""
        
        return self.send_alert(message, "info")
    
    def send_error_alert(self, error_message: str, context: str = "") -> bool:
        """Send error alert"""
        if not self.enabled:
            return False
        
        message = f"""
❌ *System Error*

*Error:* {error_message}
*Context:* {context if context else 'General error'}
*Status:* ⚠️ Attention needed

_Check logs for detailed error information_
"""
        
        return self.send_alert(message, "error")
    
    def send_daily_summary(self, daily_stats: Dict) -> bool:
        """Send daily summary alert"""
        if not self.enabled:
            return False
        
        content_generated = daily_stats.get("content_generated", 0)
        data_collected = daily_stats.get("data_collected", 0)
        alerts_sent = daily_stats.get("alerts_sent", 0)
        
        message = f"""
📋 *Daily Summary - {datetime.now().strftime('%Y-%m-%d')}*

*Content Generated:* {content_generated}
*Data Collected:* {data_collected} items
*Alerts Sent:* {alerts_sent}
*Status:* 📅 Day complete

_System running smoothly_ 🚀
"""
        
        return self.send_alert(message, "info")

# Mock Slack for testing (without actual webhook)
class MockSlackAlerts(SlackAlerts):
    """Mock version for testing without real Slack"""
    
    def send_alert(self, message: str, alert_type: str = "info") -> bool:
        print(f"\n[SLACK MOCK] {alert_type.upper()} ALERT")
        print("-" * 40)
        print(message)
        print("-" * 40)
        return True

# Test function
def test_slack_alerts():
    """Test Slack alerts system"""
    
    # Use mock for testing
    slack = MockSlackAlerts(webhook_url="mock")
    
    # Test different alert types
    print("Testing Slack Alerts System...")
    
    # Content generated alert
    content_data = {
        "platform": "twitter",
        "topic": "AI Marketing Trends",
        "length": 280,
        "success": True
    }
    slack.send_content_generated_alert(content_data)
    
    # Trend analysis alert
    trend_data = {
        "total_items": 150,
        "overall_sentiment": "very_positive",
        "average_score": 0.75
    }
    slack.send_trend_analysis_alert(trend_data)
    
    # Metrics alert
    metrics_data = {
        "total_content_tracked": 45,
        "platforms_used": ["twitter", "linkedin", "blog"],
        "overall_status": "Active"
    }
    slack.send_metrics_alert(metrics_data)
    
    print("\n✅ Slack alerts test complete")

if __name__ == "__main__":
    test_slack_alerts()