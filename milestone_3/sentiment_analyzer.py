"""
Sentiment Analysis System
Analyzes audience sentiment from collected data
"""

import re
from typing import Dict, List, Tuple
from collections import Counter

class SentimentAnalyzer:
    """Analyze sentiment from content and comments"""
    
    def __init__(self):
        # Sentiment word banks
        self.positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'best',
            'love', 'like', 'happy', 'awesome', 'fantastic', 'brilliant',
            'perfect', 'outstanding', 'impressive', 'helpful', 'useful',
            'valuable', 'effective', 'successful', 'improved', 'better'
        ]
        
        self.negative_words = [
            'bad', 'poor', 'terrible', 'awful', 'worst', 'hate',
            'dislike', 'unhappy', 'angry', 'sad', 'disappointed',
            'frustrated', 'useless', 'waste', 'broken', 'failed',
            'problem', 'issue', 'difficult', 'hard', 'confusing'
        ]
        
        self.neutral_words = [
            'okay', 'fine', 'average', 'normal', 'standard',
            'regular', 'usual', 'typical', 'moderate', 'neutral'
        ]
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text
        
        Returns: {
            'sentiment': 'positive/negative/neutral',
            'score': -1 to 1,
            'confidence': 0 to 1,
            'keywords': list of detected words
        }
        """
        if not text or not isinstance(text, str):
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0,
                'keywords': []
            }
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Count sentiment words
        pos_count = sum(1 for word in words if word in self.positive_words)
        neg_count = sum(1 for word in words if word in self.negative_words)
        neu_count = sum(1 for word in words if word in self.neutral_words)
        
        # Calculate score (-1 to 1)
        total = pos_count + neg_count + neu_count
        if total > 0:
            score = (pos_count - neg_count) / total
            confidence = total / len(words) if words else 0
        else:
            score = 0.0
            confidence = 0.0
        
        # Determine sentiment
        if score > 0.1:
            sentiment = 'positive'
        elif score < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Get keywords found
        keywords = []
        for word in words:
            if word in self.positive_words + self.negative_words + self.neutral_words:
                keywords.append(word)
        
        return {
            'sentiment': sentiment,
            'score': round(score, 3),
            'confidence': round(confidence, 3),
            'keywords': list(set(keywords))[:5]  # Unique keywords, max 5
        }
    
    def analyze_feedback_batch(self, feedback_list: List[Dict]) -> Dict:
        """
        Analyze batch of feedback items
        
        feedback_list: List of dicts with 'text' key
        Returns: Aggregated sentiment analysis
        """
        results = []
        total_pos = 0
        total_neg = 0
        total_neu = 0
        
        for item in feedback_list:
            if isinstance(item, dict) and 'text' in item:
                analysis = self.analyze_text(item['text'])
                results.append(analysis)
                
                if analysis['sentiment'] == 'positive':
                    total_pos += 1
                elif analysis['sentiment'] == 'negative':
                    total_neg += 1
                else:
                    total_neu += 1
        
        if not results:
            return {
                'total_items': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                'overall_sentiment': 'neutral',
                'average_score': 0.0
            }
        
        # Calculate overall
        total = len(results)
        overall_sentiment = self._get_overall_sentiment(total_pos, total_neg, total_neu, total)
        avg_score = sum(r['score'] for r in results) / total
        
        return {
            'total_items': total,
            'sentiment_distribution': {
                'positive': total_pos,
                'negative': total_neg,
                'neutral': total_neu,
                'positive_percent': round((total_pos / total) * 100, 1),
                'negative_percent': round((total_neg / total) * 100, 1),
                'neutral_percent': round((total_neu / total) * 100, 1)
            },
            'overall_sentiment': overall_sentiment,
            'average_score': round(avg_score, 3),
            'sample_analysis': results[:3]  # First 3 for reference
        }
    
    def _get_overall_sentiment(self, pos: int, neg: int, neu: int, total: int) -> str:
        """Determine overall sentiment from distribution"""
        if total == 0:
            return 'neutral'
        
        pos_percent = (pos / total) * 100
        neg_percent = (neg / total) * 100
        
        if pos_percent > 60:
            return 'very_positive'
        elif pos_percent > 40:
            return 'positive'
        elif neg_percent > 60:
            return 'very_negative'
        elif neg_percent > 40:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_youtube_comments(self, video_data: Dict) -> Dict:
        """Specialized analysis for YouTube comments"""
        if 'engagement_metrics' not in video_data:
            return {'error': 'No engagement data'}
        
        # Simulate comment analysis (in real app, would fetch actual comments)
        comments = [
            {"text": "Great video! Very helpful", "author": "User1"},
            {"text": "Thanks for the information", "author": "User2"},
            {"text": "Could be better with more examples", "author": "User3"}
        ]
        
        return self.analyze_feedback_batch(comments)
    
    def generate_sentiment_report(self, analysis_results: Dict) -> str:
        """Generate readable sentiment report"""
        report = []
        report.append("📊 SENTIMENT ANALYSIS REPORT")
        report.append("=" * 40)
        
        dist = analysis_results.get('sentiment_distribution', {})
        report.append(f"Total Items Analyzed: {analysis_results.get('total_items', 0)}")
        report.append(f"Overall Sentiment: {analysis_results.get('overall_sentiment', 'neutral').replace('_', ' ').title()}")
        report.append(f"Average Sentiment Score: {analysis_results.get('average_score', 0.0)}")
        report.append("")
        report.append("📈 Distribution:")
        report.append(f"  Positive: {dist.get('positive', 0)} ({dist.get('positive_percent', 0)}%)")
        report.append(f"  Negative: {dist.get('negative', 0)} ({dist.get('negative_percent', 0)}%)")
        report.append(f"  Neutral:  {dist.get('neutral', 0)} ({dist.get('neutral_percent', 0)}%)")
        
        return "\n".join(report)

# Test function
def test_sentiment_analyzer():
    """Test the sentiment analyzer"""
    analyzer = SentimentAnalyzer()
    
    # Test single text
    test_text = "This is a great product! I love it. Very helpful."
    result = analyzer.analyze_text(test_text)
    print(f"Test 1 - Single Text:")
    print(f"  Sentiment: {result['sentiment']}")
    print(f"  Score: {result['score']}")
    print(f"  Keywords: {result['keywords']}")
    
    # Test batch
    feedback = [
        {"text": "Amazing content, very useful!"},
        {"text": "It was okay, nothing special"},
        {"text": "Terrible experience, very disappointed"}
    ]
    
    batch_result = analyzer.analyze_feedback_batch(feedback)
    print(f"\nTest 2 - Batch Analysis:")
    print(analyzer.generate_sentiment_report(batch_result))

if __name__ == "__main__":
    test_sentiment_analyzer()