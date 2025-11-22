# 🎬 Reddit Movie Data Collection & Analysis Project

### *COMP 370 Final Project: Summer 2023 Movie Discussion Analysis*

This project analyzes Reddit discussions about **five major films released in Summer 2023**:

* **Oppenheimer** (July 2023)
* **Barbie** (July 2023)
* **Mission: Impossible – Dead Reckoning Part One** (July 2023)
* **Spider-Man: Across the Spider-Verse** (June 2023)
* **Guardians of the Galaxy Vol. 3** (May 2023)

**Research Questions:**
1. What aspects of these movies were discussed on Reddit?
2. How much coverage did each movie receive relative to others?

---

# 📁 **Project Structure**

```
COMP_370_FINAL_PROJECT/
│
├── data/
│   ├── annotated_teammate1.csv            # Teammate 1's annotations (for merging)
│   ├── annotated_teammate2.csv            # Teammate 2's annotations (for merging)
│   ├── annotation_sample.csv              # 200-post sample for open coding
│   ├── annotations.csv                    # Master annotations file (174/618 complete)
│   ├── codebook.json                      # Finalized 6-code codebook
│   ├── reddit_movies_posts.csv            # Full dataset (618 posts)
│   ├── remaining_posts_teammate1.csv      # 209 posts for Teammate 1 to annotate
│   └── remaining_posts_teammate2.csv      # 209 posts for Teammate 2 to annotate
│
├── scripts/
│   ├── create_annotation_sample.py        # Helper: Creates 200-post sample
│   ├── merge_annotations.py               # Merges multi-annotator files
│   ├── reddit_scraper.py                  # Part 1: Data collection
│   ├── split_posts_for_team.py            # Splits remaining posts for teammates
│   └── update_annotations.py              # Helper: Updates annotation codes
│
├── analyze_data.ipynb                     # TF-IDF analysis (Task 3)
├── batch_annotate.py                      # Main annotation tool
├── .gitignore                             # Git ignore file
├── README.md                              # This file
└── requirements.txt                       # Python dependencies
```

---

# 📊 **Project Progress**

## ✅ **Part 1: Data Collection** (COMPLETE)

**Status:** ✅ Done

**What was accomplished:**
- Collected 618 English Reddit posts from movie-related subreddits
- Time window: April 15 - September 30, 2023
- Filtered for English language using `langdetect`
- Deduplicated by post ID
- Tagged posts with primary movie labels
- Exported to `data/reddit_movies_posts.csv`

**Dataset Statistics:**
- Total posts: 618
- Subreddits: r/movies, r/boxoffice, r/TrueFilm, r/MovieDetails, etc.
- Time range: ~5.5 months covering pre-release to post-release discussion

---

### 🎯 **Search Strategy Details**

**Subreddits used:**
- r/movies
- r/moviediscussion
- r/boxoffice
- r/MovieDetails
- r/TrueFilm
- r/marvelstudios
- r/SpiderMan

**Search approach:**
- Each movie has 2-4 broad keyword variations to capture all references
- Multiple pages of results per query (`after` parameter pagination)
- Broad filters to avoid bias in data collection

### 🧪 **English Filtering Logic**

We use `langdetect` to classify the post's combined title + body text.

If text is short (<20 chars), we assume English to avoid false errors.

This ensures high-quality English-only dataset while avoiding over-filtering.

### 📅 **Time Window Filter**

All posts must satisfy:

```
2023-04-15  →  2023-09-30
```

This time window:
- Avoids time bias between movies
- Captures trailer discussions + release + early post-release discussion
- Covers ~5.5 months of organic conversation

### 🎬 **Multi-Movie Tagging**

Posts are tagged with:
- **movie_primary_label:** The movie from the search query that found it
- **movie_labels:** All movies mentioned (e.g., Barbenheimer posts tagged with both)

This allows analysis of:
- Individual movie coverage
- Cross-movie discussions (Barbenheimer phenomenon)
- Comparative discourse

---

## 🔄 **Part 2, Task 1-2: Open Coding & Manual Annotation** (IN PROGRESS)

### ✅ **Completed: Open Coding on 200 Posts**

**Status:** ✅ Done (174 posts annotated, 26 skipped as off-topic)

**Codebook Development:**
Through iterative open coding on the first 200 posts, we developed a **6-code codebook**:

| Code | Description | Usage in Sample |
|------|-------------|----------------|
| **box_office** | Discussion of ticket sales, financial performance, box office records | 58.6% |
| **reactions_and_reviews** | Film quality, themes, plot, acting, direction, critical analysis | 12.1% |
| **comparison** | Comparing movies, Barbenheimer phenomenon, multi-movie discussions | 10.9% |
| **cultural_impact** | Social, political, or cultural significance and impact | 6.9% |
| **anticipation** | Pre-release excitement, speculation, hype | 5.7% |
| **technical_aspects** | Special effects, IMAX, cinematography, production details | 5.7% |

**Key Findings from Open Coding:**
- Box office discussions dominated Reddit conversation (58.6%)
- Reflects the "Barbenheimer" phenomenon and summer 2023's record-breaking performance
- Cultural impact discussions focused on Barbie's feminist themes and Oppenheimer's historical significance
- Technical discussions often centered on Oppenheimer's IMAX 70mm presentation

**Files Generated:**
- `data/codebook.json` - Finalized 6-code codebook with definitions
- `data/annotations.csv` - 174 manually annotated posts from sample

---

### ⏳ **TODO: Annotate Remaining Posts** (NEXT STEP)

**Status:** 🔄 In Progress - **174/618 posts complete (28.2%)**

**What needs to be done:**
- Annotate remaining **~444 posts** (618 total - 174 already done)
- Use the **finalized 6-code codebook** (NO changes allowed)
- Skip off-topic posts (expect ~10-13% skip rate)
- Expected final dataset: ~540-580 coded posts

**For teammates to continue:**

1. **Run the annotation tool:**
   ```bash
   python3 batch_annotate.py
   ```

2. **The tool will:**
   - Load all 618 posts from `reddit_movies_posts.csv`
   - Skip the 174 already annotated posts
   - Start from post #175 automatically
   - Save progress after each batch

3. **Annotation guidelines:**
   - ⚠️ **DO NOT modify the codebook** - use existing 6 codes only
   - Type the code ID for each post (e.g., `box_office`)
   - Type `skip` for off-topic posts
   - Type `help` to see codebook
   - Type `quit` to save and exit
   - Tool auto-saves after each batch

4. **Expected time:**
   - ~4-8 hours for remaining 444 posts
   - Work in sessions (50-100 posts per session)
   - Take breaks to maintain quality

---

## ⏳ **Part 2, Task 3: TF-IDF Analysis** (TODO)

**Status:** ⏳ Not Started

**What needs to be done:**
1. Load completed annotations (~540-580 posts)
2. For each movie-topic pair, conduct TF-IDF analysis
3. Extract top 10 most distinctive words per topic
4. Generate brief summaries for each topic
5. Create visualizations showing coverage by movie and topic

**Files to use:**
- `analyze_data.ipynb` - Jupyter notebook for analysis
- `data/annotations.csv` - Complete annotations (after Task 2)
- `data/reddit_movies_posts.csv` - Full text data

---

# 🎯 **Codebook Reference**

## Finalized 6-Code Codebook

### 1. **anticipation**
**Pre-release Anticipation/Hype**
- Posts expressing excitement, speculation, or anticipation before the movie release
- Examples: "Can't wait to see Oppenheimer!", ticket pre-sales, trailer reactions

### 2. **box_office**
**Box Office Performance**
- Discussion of ticket sales, financial performance, box office records
- Examples: "$1 billion milestone", daily/weekly tracking, international performance

### 3. **comparison**
**Movie Comparisons**
- Comparing movies to each other, discussing Barbenheimer phenomenon
- Examples: "Barbie vs Oppenheimer", franchise comparisons, release strategy discussions

### 4. **reactions_and_reviews**
**Reactions and Reviews**
- Film quality, themes, plot, acting, direction, or other creative elements
- Includes both brief reactions and in-depth critical analysis
- Examples: Film reviews, thematic analysis, performance discussions

### 5. **cultural_impact**
**Cultural/Social Impact**
- Discussion of the movie's social, political, or cultural significance
- Examples: Barbie's feminist themes, Oppenheimer's historical relevance, awards discussions

### 6. **technical_aspects**
**Technical/Production Discussion**
- Discussion of special effects, soundtrack, cinematography, IMAX, technical achievements
- Examples: IMAX 70mm discussions, visual effects, production design, casting decisions

---

# 🚀 **Quick Start Guide**

## For Data Collection (Part 1) - COMPLETE ✅

### How the Scraper Was Run:

```bash
# 1. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the scraper
python scripts/reddit_scraper.py

# 4. Output generated
# reddit_movies_posts.csv (618 posts)
```

**Note:** This step is already complete. No need to re-run unless collecting new data.

## For Annotation (Part 2, Task 2) - IN PROGRESS 🔄

```bash
# Continue annotating remaining posts
python3 batch_annotate.py
```

**Tool features:**
- Shows 5 posts at a time
- Displays movie, subreddit, score, title, and text snippet
- Auto-saves progress after each batch
- Can jump to specific posts
- Shows progress statistics with `review` command

## For Analysis (Part 2, Task 3) - TODO ⏳

```bash
# After all annotations complete
jupyter notebook analyze_data.ipynb
```

---

# 📈 **Progress Tracker**

## ✅ Part 1: Data Collection
- [x] Set up Reddit API scraper
- [x] Implement multi-subreddit search
- [x] Add English language filtering
- [x] Add time window filtering (Apr 15 - Sep 30, 2023)
- [x] Add deduplication
- [x] Export to CSV (618 posts)
- [x] Create annotation sample (200 posts)

## 🔄 Part 2, Task 1-2: Open Coding & Annotation
- [x] Perform open coding on 200 posts
- [x] Develop codebook (6 codes)
- [x] Refine and finalize codebook
- [x] Annotate first 174 posts
- [ ] **Annotate remaining ~444 posts** ← CURRENT TASK
- [ ] Verify annotation quality
- [ ] Calculate inter-rater reliability (if multiple annotators)

## ⏳ Part 2, Task 3: Analysis
- [ ] Load and merge annotations with full dataset
- [ ] Conduct TF-IDF analysis by topic
- [ ] Extract top 10 words per topic
- [ ] Generate topic summaries
- [ ] Create coverage visualizations
- [ ] Analyze movie-specific patterns
- [ ] Write final report

---

# 📊 **Expected Final Dataset**

After completing annotation:

**Estimated distribution (based on first 200 posts):**
- box_office: ~350 posts (58.6%)
- reactions_and_reviews: ~70 posts (12.1%)
- comparison: ~65 posts (10.9%)
- cultural_impact: ~40 posts (6.9%)
- anticipation: ~35 posts (5.7%)
- technical_aspects: ~35 posts (5.7%)
- Skipped (off-topic): ~80 posts (13%)
- **Total coded:** ~595 posts

---

# 👥 **Team Workflow**

## If you're continuing this project:

### 1. **Review existing work:**
   - Check `data/annotations.csv` for current progress (174 posts done)
   - Read `data/codebook.json` to understand the 6 codes
   - Review first 20-30 annotations to see annotation quality and standards

### 2. **Continue annotation:**
   - Run `python3 batch_annotate.py`
   - Tool automatically resumes from post #175
   - Maintain consistency with existing annotations
   - **DO NOT modify codebook** - use existing 6 codes only

### 3. **Quality checks:**
   - Every 50-100 posts, type `review` to check distribution
   - Compare to expected distribution (box_office ~60%, etc.)
   - If distribution is very different, discuss with team

### 4. **After completion:**
   - Verify total annotations (~540-580 posts expected)
   - Check for any duplicate post_ids
   - Proceed to Task 3 (TF-IDF analysis)

---

# 📝 **Notes for Future Development**

## Lessons Learned from Open Coding:

1. **Box office dominance is expected:** The r/boxoffice subreddit and summer 2023's record-breaking performance naturally lead to high box office discussion percentage (~60%).

2. **Barbenheimer phenomenon:** Many posts discuss both Barbie and Oppenheimer together, requiring careful judgment on primary topic.

3. **Skip off-topic posts:** ~13% of posts mention movies but aren't about the movies themselves (e.g., generic "What movies should I watch?" questions).

4. **Merged code works well:** Combining "critical_analysis" and "general_reaction" into "reactions_and_reviews" eliminated ambiguity between brief reactions and detailed analysis.

5. **Rare codes are still valuable:** Even though "anticipation" and "technical_aspects" are only ~6% each, they represent distinct discussion types worth tracking separately.

## Annotation Consistency Tips:

- **Box office:** Any post with specific numbers, rankings, or financial performance
- **Comparison:** Posts comparing multiple movies or discussing the Barbenheimer phenomenon
- **Cultural impact:** Social/political themes, controversies, awards discussions
- **Technical aspects:** IMAX, 70mm, visual effects, production details, casting
- **Skip:** Generic movie questions, recommendation requests, off-topic posts

---

# 🛠️ **Technical Details**

## Dependencies

```bash
pip install -r requirements.txt
```

**Key libraries:**
- `requests` - Reddit API access
- `pandas` - Data manipulation
- `langdetect` - Language filtering
- `scikit-learn` - TF-IDF analysis (Task 3)
- `matplotlib`, `seaborn` - Visualizations (Task 3)

## Data Format

### `reddit_movies_posts.csv` (618 posts)

**Columns:**

| Column | Description |
|--------|-------------|
| `id` | Reddit post ID (unique identifier) |
| `title` | Post title |
| `selftext` | Post body text |
| `created_utc` | Unix timestamp of post creation |
| `subreddit` | Subreddit where post appeared |
| `score` | Reddit upvotes/score |
| `num_comments` | Number of comments |
| `url` | Direct link to Reddit post |
| `movie_primary_label` | Primary movie label from search query |
| `movie_labels` | All matched movie labels (for multi-movie posts like Barbenheimer) |

**Example row:**
```csv
15o22fz,"Films that were better than they had any right to be","It's always nice...",1689955200,movies,1050,1736,https://reddit.com/...,Barbie,"['Barbie']"
```

### `annotations.csv`
```csv
post_id,topic_code
15o22fz,comparison
15ruap0,box_office
...
```

### `codebook.json`
```json
{
  "box_office": {
    "name": "Box Office Performance",
    "definition": "Discussion of ticket sales..."
  },
  ...
}
```

---

# 📧 **Contact & Collaboration**

This is a team project for COMP 370. All team members should:
1. Read this README completely before continuing work
2. Use the annotation tool as-is (already configured correctly)
3. Follow the established 6-code codebook without modifications
4. Document any issues or questions in team communication

**Current Status:** Part 2, Task 2 - Need teammates to annotate remaining ~444 posts (72% remaining)

---

# 📄 **License & Academic Integrity**

This project is for educational purposes (COMP 370 Final Project). All data collected follows Reddit's API terms of service and is used solely for academic analysis.

---

**Last Updated:** November 22, 2024  
**Project Phase:** Part 2, Task 2 (Annotation)  
**Progress:** 174/618 posts annotated (28.2% complete)  
**Next Step:** Teammates continue annotation using `batch_annotate.py`
