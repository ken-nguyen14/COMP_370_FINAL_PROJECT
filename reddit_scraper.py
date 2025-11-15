import time
import datetime as dt
from typing import List, Dict, Any

import httpx
import pandas as pd
from langdetect import detect, LangDetectException

# ---------- CONFIGURATION ----------

BASE_URL = "https://www.reddit.com"
# Change "YOUR_USERNAME" to your actual Reddit username (or something like "student_project_xyz")
USER_AGENT = "movie_research_script by u/MYRAD31"

HEADERS = {
    "User-Agent": USER_AGENT
}

# Movies and search terms
MOVIES = {
    "oppenheimer": {
        "label": "Oppenheimer",
        "queries": ["oppenheimer", "oppenheimer 2023", "nolan oppenheimer"],
    },
    "barbie": {
        "label": "Barbie",
        "queries": ["barbie movie", "barbie film", "barbie 2023", "barbenheimer"],
    },
    "mi7": {
        "label": "Mission: Impossible – Dead Reckoning Part One",
        "queries": [
            "mission impossible dead reckoning",
            "dead reckoning part one",
            "mi7"
        ],
    },
    "spiderverse2": {
        "label": "Spider-Man: Across the Spider-Verse",
        "queries": [
            "across the spider-verse",
            "spider-verse 2",
            "spider man across the spider verse"
        ],
    },
    "gotg3": {
        "label": "Guardians of the Galaxy Vol. 3",
        "queries": [
            "guardians of the galaxy vol 3",
            "gotg vol 3",
            "gotg3"
        ],
    },
}

# Subreddits to search in
SUBREDDITS = [
    "movies",
    "MovieDetails",
    "moviediscussion",
    "boxoffice",
    "TrueFilm"
]

# Time window (UTC) for posts
START_DATE = dt.datetime(2023, 4, 15)
END_DATE = dt.datetime(2023, 9, 30, 23, 59, 59)

# Max pages to fetch per (movie, query, subreddit) combination
MAX_PAGES = 3      # each page = up to 100 posts


# ---------- HELPER FUNCTIONS ----------

def is_english(text: str) -> bool:
    """
    Roughly detect if text is English.
    For very short texts, we just accept them to avoid errors.
    """
    if not text:
        return False
    cleaned = text.strip()
    if len(cleaned) < 20:
        return True
    try:
        return detect(cleaned) == "en"
    except LangDetectException:
        return False


def fetch_posts_for_query(
    movie_label: str,
    query: str,
    subreddit: str,
    max_pages: int = MAX_PAGES
) -> List[Dict[str, Any]]:
    """
    Fetch posts from a single subreddit for a single query.
    Uses Reddit's public JSON search endpoint.
    """
    print(f"\n▶ Fetching for movie='{movie_label}', query='{query}', subreddit='r/{subreddit}'")

    url = f"{BASE_URL}/r/{subreddit}/search.json"
    after = None
    collected_posts: List[Dict[str, Any]] = []

    for page in range(max_pages):
        params = {
            "q": query,
            "limit": 100,
            "restrict_sr": 1,
            "sort": "new",
            "t": "all",
        }
        if after:
            params["after"] = after

        print(f"  Page {page+1} request…")
        response = httpx.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"  ⚠️  Failed with status {response.status_code}: {response.text[:200]}")
            break

        json_data = response.json().get("data", {})
        children = json_data.get("children", [])
        if not children:
            print("  No more posts returned.")
            break

        for child in children:
            data = child.get("data", {})
            created_utc = data.get("created_utc")
            if created_utc is None:
                continue

            created_dt = dt.datetime.utcfromtimestamp(created_utc)

            # Filter by time window
            if not (START_DATE <= created_dt <= END_DATE):
                continue

            title = data.get("title") or ""
            selftext = data.get("selftext") or ""
            full_text = f"{title}\n\n{selftext}"

            # Filter for English
            if not is_english(full_text):
                continue

            collected_posts.append({
                "id": data.get("id"),
                "subreddit": data.get("subreddit"),
                "title": title,
                "selftext": selftext,
                "created_utc": created_dt.isoformat(),
                "score": data.get("score"),
                "num_comments": data.get("num_comments"),
                "url": data.get("url"),
                "movie_primary_label": movie_label,   # we'll also store combined labels later
            })

        after = json_data.get("after")
        if not after:
            print("  Reached the end of results for this query.")
            break

        time.sleep(1)  # be polite and avoid rate-limits

    print(f"  ✓ Collected {len(collected_posts)} posts for this query.")
    return collected_posts


def main():
    # Dictionary to deduplicate posts by Reddit post ID
    posts_by_id: Dict[str, Dict[str, Any]] = {}

    for movie_key, info in MOVIES.items():
        movie_label = info["label"]
        queries = info["queries"]

        for query in queries:
            for subreddit in SUBREDDITS:
                posts = fetch_posts_for_query(movie_label, query, subreddit)

                for post in posts:
                    post_id = post["id"]
                    if not post_id:
                        continue

                    if post_id not in posts_by_id:
                        # Initialize movie_labels as a set, we'll turn it into a string later
                        post["movie_labels"] = {movie_label}
                        posts_by_id[post_id] = post
                    else:
                        # If we've already seen this post, just add the movie label
                        posts_by_id[post_id]["movie_labels"].add(movie_label)

    # Convert dict → DataFrame
    final_records: List[Dict[str, Any]] = []
    for post in posts_by_id.values():
        # convert set to comma-separated string
        labels_set = post.pop("movie_labels", set())
        post["movie_labels"] = ", ".join(sorted(labels_set))
        final_records.append(post)

    df = pd.DataFrame(final_records)
    print("\n==============================")
    print(f"Total unique posts collected: {len(df)}")
    print("==============================")

    # Save to CSV
    output_file = "reddit_movies_posts.csv"
    df.to_csv(output_file, index=False)
    print(f"\nCSV saved as: {output_file}")


if __name__ == "__main__":
    main()
