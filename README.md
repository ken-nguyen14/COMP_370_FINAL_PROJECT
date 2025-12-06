# COMP 370 Final Project: Summer 2023 Movie Discussions on Reddit

**Topic Analysis of Barbenheimer and Other Summer 2023 Films**

## Project Overview

This project analyzes Reddit discussions about major Summer 2023 movie releases, with particular focus on the "Barbenheimer" phenomenon (the simultaneous release of *Barbie* and *Oppenheimer*). We collected 618 Reddit posts, manually annotated 452 of them across six discussion topics, and characterized these topics using TF-IDF analysis and LLM-generated summaries.

### Key Findings
- **Oppenheimer** received the most coverage (218 posts, 48.2%), followed by **Barbie** (149 posts, 33.0%)
- Combined, these two films accounted for **81.2%** of all discussions
- **Box office performance** was the dominant topic across all movies (51.5% of posts)
- Coverage ratio of 8.7:1 between most-discussed (Oppenheimer) and least-discussed (Spider-Man) films

## Dataset

### Movies Analyzed
1. **Oppenheimer** (218 posts, 48.2%)
2. **Barbie** (149 posts, 33.0%)
3. **Mission: Impossible – Dead Reckoning Part One** (60 posts, 13.3%)
4. **Spider-Man: Across the Spider-Verse** (25 posts, 5.5%)

### Data Collection
- **Source**: Reddit (r/boxoffice, r/movies)
- **Time Period**: April 15 - September 30, 2023
- **Total Posts Collected**: 618
- **Posts Annotated**: 452 (73.1%)
- **Posts Excluded**: 166 (26.9% - off-topic, generic recommendations, meta-discussions)

### Subreddit Distribution
- **r/boxoffice**: More focused, financial-tracking discussions
- **r/movies**: Broader, general film discussions

## Topic Codebook

We developed a 6-topic codebook through open coding on 200 posts:

| Topic Code | Topic Name | Posts | % | Description |
|------------|------------|-------|---|-------------|
| `box_office` | Box Office Performance | 233 | 51.5% | Financial performance, opening weekends, box office records |
| `reactions_and_reviews` | Reactions and Reviews | 72 | 15.9% | Film quality, themes, plot, acting, critical analysis |
| `comparison` | Movie Comparisons | 56 | 12.4% | Comparing films, Barbenheimer phenomenon |
| `technical_aspects` | Technical/Production | 35 | 7.7% | IMAX, 70mm, cinematography, soundtracks |
| `anticipation` | Pre-release Hype | 28 | 6.2% | Trailers, posters, pre-release excitement |
| `cultural_impact` | Cultural/Social Impact | 28 | 6.2% | Social/political implications, cultural significance |

### Codebook Development
- Initial open coding identified 7 topics
- Merged `critical_analysis` and `general_reaction` into `reactions_and_reviews` due to low inter-rater reliability
- Final codebook validated with Cohen's kappa = 0.82 (strong agreement)

## Project Structure

```
COMP_370_FINAL_PROJECT/
├── data/
│   ├── reddit_movies_posts.csv              # Raw scraped data (618 posts)
│   ├── annotations.csv                       
│   ├── annotated_teammate1.csv               # Individual annotations
│   ├── annotated_teammate2.csv
│   ├── annotations_complete.csv              # Complete annotations (452 posts)
│   ├── annotation_sample.csv                 # Sample for inter-rater reliability
│   ├── remaining_posts_teammate1.csv         # Unannotated posts
│   ├── remaining_posts_teammate2.csv
│   ├── codebook.json                         # Topic definitions
│   ├── chatgpt_prompts.txt                   # LLM prompt templates
│   ├── chatgpt_summaries_ACTUAL.txt          # LLM-generated characterizations
│   ├── llm_input.json                        # Input for ChatGPT
│   ├── tfidf_results.csv                     # Top 10 TF-IDF words per topic
│   ├── final_topic_characterization_table.csv # Complete topic table
│   ├── movie_coverage_table.csv              # Coverage statistics
│   ├── movie_coverage_analysis.png           # Coverage visualization
│   └── topic_analysis_visualization.png      # Topic distribution charts
│
├── scripts/
│   ├── reddit_scraper.py                     # PRAW-based Reddit scraper
│   ├── split_posts_for_team.py               # Stratified annotation distribution
│   ├── merge_annotations.py                  # Combine team annotations
│   ├── create_annotation_sample.py           # Inter-rater reliability sample
│   ├── batch_annotate.py                     # Annotation helper
│   ├── update_annotations.py                 # Annotation utilities
│   ├── tfidf_analysis.py                     # TF-IDF computation
│   └── visualize_coverage.py                 # Coverage charts
│
├── analyze_data.ipynb                        # Main analysis notebook
├── README.md                                 # This file
└── .gitignore
```

## Methodology

### Part 1: Data Collection

#### Reddit Scraping
- Built scraper using PRAW (Python Reddit API Wrapper)
- Searched r/boxoffice and r/movies for movie-specific keywords
- Multi-movie tagging strategy (primary + comprehensive labels)
- Language filtering (95% confidence English detection using `langdetect`)
- Collected 618 posts from April-September 2023

#### Data Cleaning
- Removed duplicates
- Filtered non-English posts
- Extracted metadata: title, selftext, score, num_comments, created_utc, subreddit

### Part 2: Topic Analysis

#### Open Coding & Codebook Development
1. Initial coding on 200 posts (100 from each subreddit)
2. Developed practical boundary rules for edge cases
3. Pilot testing revealed overlap between `critical_analysis` and `general_reaction`
4. Merged overlapping categories based on inter-rater reliability results
5. Final codebook: 6 mutually exclusive topics

#### Annotation Process
- Stratified distribution across annotators (by date, movie, subreddit)
- Manual coding of 452 posts (73.1% of total)
- Inter-rater reliability testing: Cohen's kappa = 0.82 (strong agreement)
- Clear exclusion criteria for off-topic posts

#### Topic Characterization

**TF-IDF Analysis:**
- Per-topic calculation (each topic vs. all other topics combined)
- Parameters: `min_df=2`, `max_df=0.8`
- Included unigrams and bigrams (`ngram_range=(1,2)`)
- Top 10 distinctive words per topic

**LLM Summarization:**
- ChatGPT prompts with codebook definitions
- 10 representative post titles per topic (5 high-upvoted, 5 low-scoring)
- Explicit instruction to explain topic distinctiveness
- Generated concise topic characterizations

### Part 3: Results & Reporting

#### Statistical Analysis
- Topic distribution across 452 annotated posts
- Movie coverage analysis (post counts and percentages)
- Cross-topic vocabulary patterns (TF-IDF term overlap)
- Topic distribution by individual movie

#### Visualizations
Created comprehensive visualizations:
1. **Topic Analysis** (4-panel):
   - Topic distribution (bar chart)
   - Topic percentages (pie chart)
   - Topic by movie (grouped bar chart)
   - Topic distribution (horizontal bar chart)

2. **Movie Coverage Analysis** (4-panel):
   - Movie distribution (bar chart)
   - Movie percentages (pie chart)
   - Coverage comparison (horizontal bar chart)
   - Summary statistics table

#### Report Writing
- **Introduction Section**: General overview of key findings
- **Data Section**: Dataset, number of articles, filtering, statistics
- **Methods Section**: Codebook development, TF-IDF methodology, LLM prompts, annotation workflow
- **Results Section**: Topic validation, distributions, characterizations, coverage analysis
- **Discussion Section**: Interpretations, limitations, implications
- **AAAI LaTeX Format**: Two-column layout with appendix tables/figures

## Key Results

### Topic Distribution Findings
1. **Box Office (51.5%)**: Dominated discussion across all films, reflecting Reddit's focus on commercial performance
2. **Reactions/Reviews (15.9%)**: Second most common, especially prevalent for *Barbie*
3. **Comparison (12.4%)**: Heavily focused on Barbenheimer phenomenon
4. **Technical Aspects (7.7%)**: IMAX 70mm discussions, particularly prominent for *Oppenheimer*
5. **Anticipation (6.2%)**: Pre-release excitement and marketing
6. **Cultural Impact (6.2%)**: Social/political significance of films

### Movie-Specific Patterns
- **Oppenheimer**: Highest coverage, elevated technical discussions (IMAX/70mm), strong box office focus
- **Barbie**: More balanced topic distribution, higher reactions/reviews percentage
- **Mission: Impossible**: Heavy box office concentration (typical for franchise films)
- **Spider-Man**: Elevated comparison discussions despite small sample size

### Distinctive Vocabulary Insights
- **"Barbenheimer"**: Appeared in 3 topics (box_office, comparison, cultural_impact) - truly cross-cutting phenomenon
- **Christopher Nolan**: Appeared in 4 topics - director as major discussion point
- **Exclusive terms**: 
  - "IMAX"/"70mm" → technical_aspects
  - "ken" → reactions_and_reviews
  - "mattel"/"warner"/"japan" → cultural_impact

### Coverage Analysis
- **Oppenheimer**: 218 posts (48.2%) - highest coverage
- **Barbie**: 149 posts (33.0%) - second highest
- **Barbenheimer Combined**: 367 posts (81.2%) - dominated Summer 2023 discussions
- **Coverage Ratio**: 8.7:1 between Oppenheimer and Spider-Man

## Installation & Usage

### Requirements
```bash
pip install praw pandas numpy scikit-learn matplotlib seaborn langdetect --break-system-packages
```

### Configuration

1. **Reddit API Credentials** (for scraping):
Create a Reddit app at https://www.reddit.com/prefs/apps
```python
# In reddit_scraper.py
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="YOUR_USER_AGENT"
)
```

### Running the Analysis

1. **Data Collection**:
```bash
cd scripts
python reddit_scraper.py
```

2. **Annotation Workflow**:
```bash
# Split posts for team annotation
python split_posts_for_team.py

# Annotate individually (manual process)
python batch_annotate.py

# Merge team annotations
python merge_annotations.py
```

3. **Topic Analysis**:
```bash
# Run TF-IDF analysis
python tfidf_analysis.py

# This generates:
# - tfidf_results.csv
# - llm_input.json (for ChatGPT)
```

4. **Visualization**:
```bash
# Generate coverage visualizations
python visualize_coverage.py

# This generates:
# - movie_coverage_analysis.png
# - movie_coverage_table.csv
```

5. **Complete Analysis Pipeline**:
```bash
# Run Jupyter notebook with all analyses
jupyter notebook analyze_data.ipynb
```

## Files Description

### Data Files
- **reddit_movies_posts.csv**: Raw scraped posts with metadata (618 posts)
- **annotations.csv**: Final annotated dataset (452 posts with topic labels)
- **codebook.json**: Topic definitions and boundary rules
- **tfidf_results.csv**: Top 10 TF-IDF words for each topic
- **final_topic_characterization_table.csv**: Complete topic table with TF-IDF terms and LLM summaries
- **movie_coverage_table.csv**: Coverage statistics by movie

### Scripts
- **reddit_scraper.py**: PRAW-based scraper for r/boxoffice and r/movies with language filtering
- **tfidf_analysis.py**: Per-topic TF-IDF calculation with parameter tuning (min_df, max_df, ngrams)
- **visualize_coverage.py**: Generate 4-panel coverage visualizations with seaborn
- **split_posts_for_team.py**: Stratified annotation distribution across team members
- **merge_annotations.py**: Combine individual annotations with conflict resolution
- **batch_annotate.py**: Interactive CLI for manual annotation

### Notebooks
- **analyze_data.ipynb**: Complete analysis pipeline from data loading to visualization

## Technical Details

### TF-IDF Configuration
- **min_df**: 2 (eliminate typos/unique terms that appear in only 1 document)
- **max_df**: 0.8 (exclude common HTML artifacts like "amp" that appear in 80%+ of posts)
- **ngram_range**: (1, 2) (unigrams + bigrams for better phrase capture)
- **Per-topic calculation**: Each topic vs. all others combined (not global TF-IDF)

### Annotation Quality Metrics
- **Main disagreements**: box_office vs. comparison boundary for multi-film financial discussions
- **Zero disagreements**: technical_aspects, anticipation, cultural_impact (clear boundaries)

### Exclusion Criteria
Posts were excluded if they:
- Generic movie recommendations without specific film focus
- Filmmaking discussions without connection to specific movies
- Reddit meta-discussions about subreddit rules
- Non-English posts (below 95% confidence threshold)
- Spam or promotional content

## License

This is an educational project completed for COMP 370 at McGill University. Data collected from Reddit adheres to Reddit's API terms of service. All analyses and visualizations are original work by the project team.