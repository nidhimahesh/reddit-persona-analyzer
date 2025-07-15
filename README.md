# Reddit User Persona Analyzer

A Python script that analyzes Reddit user profiles to generate comprehensive user personas based on their posts and comments.

## Features

- Scrapes Reddit user posts and comments
- Analyzes interests, personality traits, communication style, and activity patterns  
- Generates detailed user personas with AI assistance
- Provides citations for each persona characteristic
- Supports both Reddit API and web scraping methods
- Follows PEP-8 coding guidelines

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd reddit-persona-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```


## Usage

### Basic Usage

```bash
python reddit_persona_analyzer.py <reddit_profile_url>
```

### Examples

```bash
# Analyze the first sample user
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/

# Analyze the second sample user  
python reddit_persona_analyzer.py https://www.reddit.com/user/Hungry-Move-6603/
```

### Output

The script will generate a text file named `{username}_persona.txt` containing:

1. **User Persona**: Detailed analysis including demographics, interests, personality traits, and behavioral patterns
2. **Citations**: Specific posts and comments that support each persona characteristic

## Script Architecture

### Main Components

1. **RedditUserAnalyzer**: Main class handling the entire analysis pipeline
2. **Data Scraping**: Supports both Reddit API and web scraping methods
3. **Analysis Engine**: Processes user data to extract persona characteristics
4. **AI Integration**: Uses OpenAI GPT for enhanced persona generation
5. **Citation System**: Tracks source content for each persona element

### Analysis Categories

- **Basic Information**: Account age, karma, activity level
- **Interests**: Top subreddits, primary/secondary interests
- **Personality Traits**: Helpfulness, enthusiasm, curiosity, formality
- **Communication Style**: Tone, writing length, readability
- **Demographics**: Age range, location, profession (inferred)
- **Activity Patterns**: Most active times, posting frequency

## Sample Output

```
USER PERSONA

Name: kojied
Account Age: 365 days
Activity Level: 15 posts, 45 comments

INTERESTS & HOBBIES:
Primary Interests: Technology (programming), Learning (learnpython)
Secondary Interests: Lifestyle (coffee), Urban Living (AskNYC)

PERSONALITY TRAITS:
- Communication Style: Positive
- Activity Pattern: Most active around 14:00
- Engagement Level: Regular

DEMOGRAPHICS:
- Likely Age Range: 25-35
- Likely Location: Urban area
- Likely Profession: Technology/Student

BEHAVIORAL PATTERNS:
- Prefers communities focused on technology and learning
- Engages in helpful discussions
- Regular contributor to community discussions

======================================================
CITATIONS
======================================================

INTERESTS:
- Post in r/learnpython: "My experience with Python programming..."
- Post in r/AskNYC: "Best coffee shops in NYC?..."

PERSONALITY:
- Comment in r/programming: "I totally agree! Python is much more readable..."
- Comment in r/AskNYC: "Try Blue Bottle Coffee on 30th Street..."
```

## Error Handling

The script includes comprehensive error handling for:

- Invalid Reddit URLs
- API rate limiting
- Network connectivity issues
- Missing API credentials
- Empty or private profiles

## Technical Details

### Dependencies

- **praw**: Reddit API wrapper
- **openai**: OpenAI API integration
- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing
- **textstat**: Text readability analysis
- **python-dotenv**: Environment variable management

### Fallback Mechanisms

1. If Reddit API fails
