# Reddit User Persona Analyzer

This is a Python script that analyzes a Reddit user's public posts and comments to generate a user persona. It scrapes Reddit data directly.

## Features

- Scrapes **submitted posts** and **comments** from a Reddit user's profile
- Builds a **text-based persona** inferred from user content
- Cites relevant posts/comments for each trait
- Simple CLI-based usage

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nidhimahesh/reddit-persona-analyzer.git
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

1. **User Persona**: A structured summary including demographics, interests, personality traits, behavior patterns, and online habits.
2. **Citations**: A list of specific Reddit posts/comments that support each persona insight.

## Script Architecture

### Main Components

1. **RedditUserAnalyzer**: Orchestrates scraping and persona generation.
2. **Data Scraping**: Extracts posts and comments using Reddit's public `.json` endpoints.
3. **Rule-Based Classifier**: Organizes traits into structured categories using keyword mapping and frequency.
4. **Citation System**: Extracts key URLs to support each characteristic.
5. **Output Writer**: Formats and writes the final persona to a `.txt` file.

### Analysis Categories

- **Demographics**: Inferred location, age group, and role (e.g., student)
- **Interests**: Active subreddits, repeated topics, hobbies
- **Personality Traits**: Commenting/posting balance, tone, inferred sentiment
- **Behavior Patterns**: Activity levels, frequency, diversity of content
- **Goals & Motivations**: Inferred from repeated themes or posts
- **Frustrations**: Common issues or complaints discussed
- **Online Habits**: Time of activity, subreddit focus
- **Citations**: Specific post/comment URLs backing the traits

## Sample Output #1

```
USER PERSONA: KOJIED
==================================================

DEMOGRAPHICS:
--------------------
Age Range: Unknown
Location: Usa
Occupation: Student

INTERESTS:
--------------------
• r/ManorLords community
• r/VisionPro community
• r/AskReddit community
• r/OnePiece community
• r/plantclinic community
• Programming
• Gaming
• Technology
• Music
• Movies

PERSONALITY TRAITS:
--------------------
• More of a commenter than poster
• Generally positive attitude

BEHAVIOR PATTERNS:
--------------------
• Active in 24 different subreddits
• Posts tend to receive good engagement

GOALS & MOTIVATIONS:
--------------------
• Learn new skills
• Career advancement
• Help others
• Entertainment

FRUSTRATIONS:
--------------------
• Technical issues
• Time management
• Learning curve

ONLINE HABITS:
--------------------
• Most active in r/ManorLords
• Has made 47 posts/comments

CITATIONS:
--------------------
Top Content:
  - https://reddit.com/r/VisionPro/comments/1b4yi15/spacial_tours_with_3d_map_and_360_video/
  - https://reddit.com/r/VisionPro/comments/1alx270/watching_edgerunners_on_the_moon_feels/
  - https://reddit.com/r/projectzomboid/comments/13dwl0i/3_months_in_the_cleanest_and_most_functional_rv/
  - https://reddit.com/r/Frugal/comments/15szxcx/how_do_you_decide_what_to_buy_and_not_buy/
  - https://reddit.com/r/VisionPro/comments/1ajbkqm/would_you_guys_like_to_see_pokemon_go_in_avp/
```

## Error Handling

The script includes comprehensive error handling for:


- Invalid or malformed Reddit usernames
- Private or deleted profiles
- Internet connectivity issues
- No posts/comments found (inactive users)
- Reddit temporarily unavailable

## Technical Details

### Dependencies

- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing
- **re** (Python built-in): For keyword and pattern matching
- `**os**: For file management and path handling

### Fallback Mechanisms

1. **If a user has no posts or comments**: Script exits gracefully with a message.
2. **If Reddit returns 429 (rate limit)**: Script prints a warning to retry later.
3. **If output folder doesn't exist**: Script will create/write locally by default.
