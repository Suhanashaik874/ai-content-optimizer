"""
Integration script to connect Milestone 3 with existing system
"""

import sys
from pathlib import Path

# Add to path
sys.path.append(str(Path(__file__).parent))

def integrate_with_main():
    """Add Milestone 3 features to main.py"""
    
    print("🔧 Integrating Milestone 3 with main system...")
    
    # Create milestone_3 directory
    milestone3_dir = Path("milestone_3")
    milestone3_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_file = milestone3_dir / "__init__.py"
    init_file.touch()
    
    print("✅ Milestone 3 directory created")
    
    # Instructions for modifying main.py
    print("\n📝 To add Milestone 3 to main.py, add these options:")
    print("""
    In main.py's menu, add:
    
    print("6. 📊 Milestone 3 Dashboard")
    print("7. 🎭 Sentiment Analysis")
    print("8. 📈 Performance Metrics")
    print("9. 🔔 Slack Alerts")
    print("10. 📋 Generate Reports")
    
    Then handle these choices:
    
    elif choice == "6":
        from milestone_3.dashboard import Milestone3Dashboard
        dashboard = Milestone3Dashboard()
        dashboard.show_dashboard()
        input("Press Enter to continue...")
    
    elif choice == "7":
        from milestone_3.dashboard import Milestone3Dashboard
        dashboard = Milestone3Dashboard()
        dashboard.analyze_collected_data()
        input("Press Enter to continue...")
    
    elif choice == "8":
        from milestone_3.metrics_tracker import MetricsTracker
        tracker = MetricsTracker()
        print(tracker.generate_metrics_report())
        input("Press Enter to continue...")
    
    elif choice == "9":
        from milestone_3.slack_alerts import MockSlackAlerts
        slack = MockSlackAlerts(webhook_url="mock")
        slack.send_alert("Test alert from main system", "info")
        input("Press Enter to continue...")
    
    elif choice == "10":
        from milestone_3.dashboard import Milestone3Dashboard
        dashboard = Milestone3Dashboard()
        dashboard.generate_reports()
        input("Press Enter to continue...")
    """)
    
    print("\n🎉 Integration instructions ready!")
    print("\nTo test Milestone 3 standalone, run:")
    print("python milestone_3/dashboard.py")

if __name__ == "__main__":
    integrate_with_main()