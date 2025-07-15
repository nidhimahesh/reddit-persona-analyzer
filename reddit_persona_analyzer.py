#!/usr/bin/env python3
"""
Reddit User Persona Generator
This script scrapes a Reddit user's profile and generates a detailed user persona.
"""

import requests
import json
import time
import re
import os
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
import argparse

@dataclass
class RedditPost:
    """Data class for Reddit posts"""
    title: str
    content: str
    subreddit: str
    score: int
    created_utc: int
    url: str
    post_type: str

class RedditScraper:
    """Reddit scraper using Reddit's JSON API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def extract_username(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL"""
        # Handle different URL formats
        if '/user/' in profile_url:
            username = profile_url.split('/user/')[1].rstrip('/')
        elif '/u/' in profile_url:
            username = profile_url.split('/u/')[1].rstrip('/')
        else:
            raise ValueError(f"Invalid Reddit profile URL: {profile_url}")
        
        return username
    
    def scrape_user_content(self, username: str, limit: int = 50) -> List[RedditPost]:
        """Scrape user's posts and comments"""
        posts = []
        
        print(f"Scraping data for user: {username}")
        
        # Get user's submitted posts
        print("Fetching user posts...")
        posts.extend(self._get_user_posts(username, limit // 2))
        
        # Get user's comments
        print("Fetching user comments...")
        posts.extend(self._get_user_comments(username, limit // 2))
        
        return posts
    
    def _get_user_posts(self, username: str, limit: int) -> List[RedditPost]:
        """Get user's submitted posts"""
        url = f"https://www.reddit.com/user/{username}/submitted.json"
        return self._fetch_content(url, limit, 'post')
    
    def _get_user_comments(self, username: str, limit: int) -> List[RedditPost]:
        """Get user's comments"""
        url = f"https://www.reddit.com/user/{username}/comments.json"
        return self._fetch_content(url, limit, 'comment')
    
    def _fetch_content(self, url: str, limit: int, content_type: str) -> List[RedditPost]:
        """Fetch content from Reddit API"""
        posts = []
        params = {'limit': min(limit, 25)}
        
        try:
            print(f"Fetching {content_type}s from: {url}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' not in data or 'children' not in data['data']:
                print(f"No data found for {content_type}s")
                return posts
            
            children = data['data']['children']
            print(f"Found {len(children)} {content_type}s")
            
            for child in children:
                if len(posts) >= limit:
                    break
                    
                item_data = child['data']
                
                if content_type == 'post':
                    # Skip deleted or removed posts
                    if item_data.get('removed_by_category') or item_data.get('title') == '[deleted]':
                        continue
                        
                    post = RedditPost(
                        title=item_data.get('title', ''),
                        content=item_data.get('selftext', ''),
                        subreddit=item_data.get('subreddit', ''),
                        score=item_data.get('score', 0),
                        created_utc=item_data.get('created_utc', 0),
                        url=f"https://reddit.com{item_data.get('permalink', '')}",
                        post_type='post'
                    )
                else:  # comment
                    # Skip deleted or removed comments
                    if item_data.get('body') in ['[deleted]', '[removed]']:
                        continue
                        
                    post = RedditPost(
                        title='',
                        content=item_data.get('body', ''),
                        subreddit=item_data.get('subreddit', ''),
                        score=item_data.get('score', 0),
                        created_utc=item_data.get('created_utc', 0),
                        url=f"https://reddit.com{item_data.get('permalink', '')}",
                        post_type='comment'
                    )
                
                # Only add if there's actual content
                if post.content.strip() or post.title.strip():
                    posts.append(post)
            
            print(f"Successfully scraped {len(posts)} {content_type}s")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {content_type}s: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for {content_type}s: {e}")
        except Exception as e:
            print(f"Unexpected error fetching {content_type}s: {e}")
        
        return posts

class SimplePersonaAnalyzer:
    """Simple persona analyzer that doesn't require OpenAI"""
    
    def analyze_user_persona(self, username: str, posts: List[RedditPost]) -> Dict:
        """Generate user persona from Reddit posts using simple analysis"""
        
        if not posts:
            return self._create_empty_persona(username)
        
        # Analyze content
        subreddits = [post.subreddit for post in posts if post.subreddit]
        subreddit_counts = {}
        for sub in subreddits:
            subreddit_counts[sub] = subreddit_counts.get(sub, 0) + 1
        
        # Get top subreddits
        top_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Analyze content themes
        all_content = []
        for post in posts:
            if post.title:
                all_content.append(post.title.lower())
            if post.content:
                all_content.append(post.content.lower())
        
        combined_text = ' '.join(all_content)
        
        # Simple keyword analysis
        interests = self._extract_interests(combined_text, top_subreddits)
        personality_traits = self._extract_personality_traits(posts)
        behavior_patterns = self._extract_behavior_patterns(posts, subreddit_counts)
        
        return {
            'username': username,
            'demographics': self._infer_demographics(combined_text, top_subreddits),
            'interests': interests,
            'personality_traits': personality_traits,
            'behavior_patterns': behavior_patterns,
            'goals_motivations': self._extract_goals(combined_text),
            'frustrations': self._extract_frustrations(combined_text),
            'online_habits': self._extract_online_habits(posts, subreddit_counts),
            'citations': self._create_citations(posts)
        }
    
    def _extract_interests(self, text: str, top_subreddits: List) -> List[str]:
        """Extract interests from text and subreddits"""
        interests = []
        
        # Add top subreddits as interests
        for sub, count in top_subreddits[:5]:
            interests.append(f"r/{sub} community")
        
        # Simple keyword matching
        interest_keywords = {
            'programming': ['code', 'python', 'javascript', 'programming', 'developer', 'software'],
            'gaming': ['game', 'gaming', 'play', 'steam', 'xbox', 'playstation'],
            'technology': ['tech', 'technology', 'computer', 'laptop', 'phone'],
            'music': ['music', 'song', 'album', 'artist', 'band'],
            'sports': ['football', 'basketball', 'soccer', 'baseball', 'sport'],
            'movies': ['movie', 'film', 'cinema', 'watch', 'series'],
            'cooking': ['cook', 'recipe', 'food', 'kitchen', 'meal'],
            'travel': ['travel', 'trip', 'vacation', 'country', 'visit']
        }
        
        for interest, keywords in interest_keywords.items():
            if any(keyword in text for keyword in keywords):
                interests.append(interest.title())
        
        return interests[:10]
    
    def _extract_personality_traits(self, posts: List[RedditPost]) -> List[str]:
        """Extract personality traits from posts"""
        traits = []
        
        # Analyze posting patterns
        total_posts = len([p for p in posts if p.post_type == 'post'])
        total_comments = len([p for p in posts if p.post_type == 'comment'])
        
        if total_comments > total_posts:
            traits.append("More of a commenter than poster")
        if total_posts > total_comments:
            traits.append("Active content creator")
        
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'awesome', 'love', 'like', 'amazing', 'excellent']
        negative_words = ['bad', 'terrible', 'hate', 'dislike', 'awful', 'horrible']
        
        all_content = ' '.join([post.content.lower() for post in posts if post.content])
        
        positive_count = sum(1 for word in positive_words if word in all_content)
        negative_count = sum(1 for word in negative_words if word in all_content)
        
        if positive_count > negative_count * 1.5:
            traits.append("Generally positive attitude")
        elif negative_count > positive_count * 1.5:
            traits.append("Critical thinker")
        
        return traits
    
    def _extract_behavior_patterns(self, posts: List[RedditPost], subreddit_counts: Dict) -> List[str]:
        """Extract behavior patterns"""
        patterns = []
        
        patterns.append(f"Active in {len(subreddit_counts)} different subreddits")
        
        avg_score = sum(post.score for post in posts) / len(posts) if posts else 0
        if avg_score > 10:
            patterns.append("Posts tend to receive good engagement")
        
        return patterns
    
    def _infer_demographics(self, text: str, top_subreddits: List) -> Dict[str, str]:
        """Infer basic demographics"""
        demographics = {
            'age_range': 'Unknown',
            'location': 'Unknown',
            'occupation': 'Unknown'
        }
        
        # Simple location inference
        locations = ['usa', 'america', 'canada', 'uk', 'britain', 'australia', 'europe']
        for location in locations:
            if location in text:
                demographics['location'] = location.title()
                break
        
        # Simple occupation inference
        occupations = {
            'student': ['student', 'college', 'university', 'school'],
            'developer': ['developer', 'programmer', 'coding', 'software'],
            'teacher': ['teacher', 'teaching', 'education'],
            'healthcare': ['doctor', 'nurse', 'medical', 'healthcare']
        }
        
        for job, keywords in occupations.items():
            if any(keyword in text for keyword in keywords):
                demographics['occupation'] = job.title()
                break
        
        return demographics
    
    def _extract_goals(self, text: str) -> List[str]:
        """Extract goals and motivations"""
        goals = []
        
        goal_keywords = {
            'Learn new skills': ['learn', 'learning', 'study', 'education'],
            'Career advancement': ['job', 'career', 'work', 'promotion'],
            'Help others': ['help', 'helping', 'advice', 'support'],
            'Entertainment': ['fun', 'entertainment', 'hobby', 'enjoy']
        }
        
        for goal, keywords in goal_keywords.items():
            if any(keyword in text for keyword in keywords):
                goals.append(goal)
        
        return goals
    
    def _extract_frustrations(self, text: str) -> List[str]:
        """Extract frustrations"""
        frustrations = []
        
        frustration_keywords = {
            'Technical issues': ['bug', 'error', 'problem', 'issue', 'broken'],
            'Time management': ['time', 'busy', 'schedule', 'deadline'],
            'Learning curve': ['difficult', 'hard', 'struggle', 'confusing']
        }
        
        for frustration, keywords in frustration_keywords.items():
            if any(keyword in text for keyword in keywords):
                frustrations.append(frustration)
        
        return frustrations
    
    def _extract_online_habits(self, posts: List[RedditPost], subreddit_counts: Dict) -> List[str]:
        """Extract online habits"""
        habits = []
        
        if subreddit_counts:
            top_sub = max(subreddit_counts, key=subreddit_counts.get)
            habits.append(f"Most active in r/{top_sub}")
        
        habits.append(f"Has made {len(posts)} posts/comments")
        
        return habits
    
    def _create_citations(self, posts: List[RedditPost]) -> Dict[str, List[str]]:
        """Create citations for persona characteristics"""
        citations = {}
        
        # Sample citations for top posts
        top_posts = sorted(posts, key=lambda x: x.score, reverse=True)[:5]
        
        citations['top_content'] = [post.url for post in top_posts if post.url]
        
        return citations
    
    def _create_empty_persona(self, username: str) -> Dict:
        """Create empty persona when no content found"""
        return {
            'username': username,
            'demographics': {'age_range': 'Unknown', 'location': 'Unknown', 'occupation': 'Unknown'},
            'interests': ['No data available'],
            'personality_traits': ['No data available'],
            'behavior_patterns': ['No data available'],
            'goals_motivations': ['No data available'],
            'frustrations': ['No data available'],
            'online_habits': ['No data available'],
            'citations': {}
        }

def save_persona_to_file(persona: Dict, filename: str):
    """Save persona to text file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"USER PERSONA: {persona['username'].upper()}\n")
        f.write("=" * 50 + "\n\n")
        
        # Demographics
        f.write("DEMOGRAPHICS:\n")
        f.write("-" * 20 + "\n")
        for key, value in persona['demographics'].items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        f.write("\n")
        
        # Interests
        f.write("INTERESTS:\n")
        f.write("-" * 20 + "\n")
        for interest in persona['interests']:
            f.write(f"• {interest}\n")
        f.write("\n")
        
        # Personality Traits
        f.write("PERSONALITY TRAITS:\n")
        f.write("-" * 20 + "\n")
        for trait in persona['personality_traits']:
            f.write(f"• {trait}\n")
        f.write("\n")
        
        # Behavior Patterns
        f.write("BEHAVIOR PATTERNS:\n")
        f.write("-" * 20 + "\n")
        for pattern in persona['behavior_patterns']:
            f.write(f"• {pattern}\n")
        f.write("\n")
        
        # Goals & Motivations
        f.write("GOALS & MOTIVATIONS:\n")
        f.write("-" * 20 + "\n")
        for goal in persona['goals_motivations']:
            f.write(f"• {goal}\n")
        f.write("\n")
        
        # Frustrations
        f.write("FRUSTRATIONS:\n")
        f.write("-" * 20 + "\n")
        for frustration in persona['frustrations']:
            f.write(f"• {frustration}\n")
        f.write("\n")
        
        # Online Habits
        f.write("ONLINE HABITS:\n")
        f.write("-" * 20 + "\n")
        for habit in persona['online_habits']:
            f.write(f"• {habit}\n")
        f.write("\n")
        
        # Citations
        if persona['citations']:
            f.write("CITATIONS:\n")
            f.write("-" * 20 + "\n")
            for category, citations in persona['citations'].items():
                if citations:
                    f.write(f"{category.replace('_', ' ').title()}:\n")
                    for citation in citations:
                        f.write(f"  - {citation}\n")
                    f.write("\n")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate Reddit user persona with citations')
    parser.add_argument('profile_url', help='Reddit user profile URL')
    parser.add_argument('-o', '--output', help='Output filename (optional)')
    
    args = parser.parse_args()
    
    try:
        # Initialize scraper and analyzer
        scraper = RedditScraper()
        analyzer = SimplePersonaAnalyzer()
        
        # Extract username from URL
        username = scraper.extract_username(args.profile_url)
        print(f"Analyzing user: {username}")
        
        # Scrape user content
        posts = scraper.scrape_user_content(username)
        
        if not posts:
            print("Error: No content found - cannot generate persona")
            return
        
        print(f"Found {len(posts)} posts/comments")
        
        # Generate persona
        print("Generating persona...")
        persona = analyzer.analyze_user_persona(username, posts)
        
        # Save to file
        output_filename = args.output if args.output else f"{username}_persona.txt"
        save_persona_to_file(persona, output_filename)
        
        print(f"Analysis complete! Check the file: {output_filename}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    main()