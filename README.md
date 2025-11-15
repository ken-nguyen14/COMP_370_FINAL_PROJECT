# 🎬 Reddit Movie Data Collection Project

### *Part 1: Reddit Data Scraper for Summer 2023 Movie Analysis*

This project collects Reddit posts related to **five major films released in Summer 2023**:

* **Oppenheimer** (July 2023)
* **Barbie** (July 2023)
* **Mission: Impossible – Dead Reckoning Part One** (July 2023)
* **Spider-Man: Across the Spider-Verse** (June 2023)
* **Guardians of the Galaxy Vol. 3** (May 2023)

This dataset will be used for:

* Topic discovery
* Open coding
* Manual annotation
* TF-IDF analysis
* Coverage comparison across films

This README helps maintain the workflow so another LLM or teammate can easily continue development.

---

# 📁 **Project Structure**

```
reddit_movie_project/
│
├── reddit_scraper.py          # Main scraper script
├── requirements.txt           # Python dependencies
├── reddit_movies_posts.csv    # Output dataset (generated after running)
├── README.md                  # This file
└── venv/                      # Virtual environment (optional)
```

---

# 🧠 **Project Overview**

Your job (Part 1 of the team assignment):

> ✨ “Collect 500+ English Reddit posts related to the selected movies
> using unbiased filters and export them to CSV.”

We accomplish this by:

* Searching multiple movie-related subreddits
* Using broad keyword lists per film
* Pulling multiple pages of results
* Filtering to a specific time window (15 Apr – 30 Sep 2023)
* Filtering posts for English using language detection
* Deduplicating by Reddit post ID
* Labeling posts with corresponding movie(s)

This ensures the dataset is **unbiased, relevant, and complete**.

---

# 🚀 **How to Run the Scraper**

### 1. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the scraper

```bash
python reddit_scraper.py
```

### 4. View CSV output

The script generates:

```
reddit_movies_posts.csv
```

This contains:

| Column              | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| id                  | Reddit post ID                                               |
| title               | Post title                                                   |
| selftext            | Post body text                                               |
| created_utc         | Timestamp                                                    |
| subreddit           | Where the post appeared                                      |
| score               | Upvotes                                                      |
| num_comments        | Comment count                                                |
| url                 | Link to post                                                 |
| movie_primary_label | Movie label from the query source                            |
| movie_labels        | All matched movie labels (Barbenheimer posts tagged as both) |

---

# 🧪 **English Filtering Logic**

We use `langdetect` to classify the post’s combined title + body text.

If text is short (<20 chars), we assume English to avoid false errors.

---

# 🎯 **Search Strategy**

### Subreddits used:

* r/movies
* r/moviediscussion
* r/boxoffice
* r/MovieDetails
* r/TrueFilm
* r/marvelstudios
* r/SpiderMan

### Search queries per movie:

(See `MOVIES` dict in `reddit_scraper.py`)

Each movie has 2–4 broad keyword variations to capture all references.

---

# 📅 **Time Window Filter**

All posts must satisfy:

```
2023-04-15  →  2023-09-30
```

This:

* avoids time bias between movies
* captures trailer + release + early discussion

---

# 📈 **Progress Tracker**

### ✔ DONE

* Created project folder
* Set up virtual environment
* Installed dependencies
* Implemented JSON-based Reddit API scraper
* Added multi-query search for 5 movies
* Added subreddit looping
* Added pagination (`after` parameter)
* Added English language filtering
* Added time window filtering
* Added deduplication by post ID
* Added multi-movie tagging
* Exported dataset to CSV
* Wrote README

### 🔄 IN PROGRESS

* Validate CSV for:

  * Dead links
  * Non-English false positives
  * Off-topic noise
* explore increasing `MAX_PAGES` if needed

### ⏳ TODO (for next LLM agent or teammate)

* [ ] Perform initial sanity check of the dataset
* [ ] Randomly review 20 posts for relevance
* [ ] Adjust keyword lists if any movie underperforms in coverage
* [ ] (Optional) Add additional subreddits
* [ ] Confirm total post count > 500
* [ ] Deliver dataset to open-coding team
* [ ] Produce small data summary:
  - Posts per movie
  - Posts per subreddit
  - Posts over time