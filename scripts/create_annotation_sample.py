import pandas as pd
import numpy as np
import os

# Configuration
INPUT_FILE = 'data/reddit_movies_posts.csv'
OUTPUT_FILE = 'data/annotation_sample.csv'
SAMPLE_SIZE = 200
RANDOM_SEED = 42

def create_annotation_sample():
    """Create stratified sample of 200 posts"""
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found")
        return False
    
    # Load, sample, save
    df = pd.read_csv(INPUT_FILE)
    np.random.seed(RANDOM_SEED)
    
    sample = df.groupby('movie_primary_label', group_keys=False).apply(
        lambda x: x.sample(
            n=min(len(x), int(SAMPLE_SIZE * len(x) / len(df)) + 20),
            random_state=RANDOM_SEED
        )
    ).sample(n=min(SAMPLE_SIZE, len(df)), random_state=RANDOM_SEED)
    
    os.makedirs('data', exist_ok=True)
    sample.to_csv(OUTPUT_FILE, index=False)
    
    print(f"✓ Created {OUTPUT_FILE}")
    return True

if __name__ == "__main__":
    create_annotation_sample()