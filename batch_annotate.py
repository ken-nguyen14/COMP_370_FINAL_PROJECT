"""
COMP 370 Final Project - Batch Annotation Tool

A simpler tool for annotating posts in batches.
This displays multiple posts at once and lets you annotate them quickly.
"""

import pandas as pd
import json
import os

# For open coding 200 articles
#SAMPLE_FILE = 'data/annotation_sample.csv'

# For remaining articles (change name of sample file) i.e. remaining_posts_teammate1.csv
SAMPLE_FILE = 'data/remaining_posts_teammate1.csv'
CODEBOOK_FILE = 'data/codebook.json'
# Change annotation file to your specific one i.e. annotated_teammate1.csv
ANNOTATIONS_FILE = 'data/annotated_teammate1.csv'
BATCH_SIZE = 5

def load_or_create_codebook():
    """Load existing codebook or create a starter one"""
    if os.path.exists(CODEBOOK_FILE):
        try:
            with open(CODEBOOK_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("⚠️  Codebook file exists but is corrupted. Creating new one...")
    
    # Create starter codebook based on common movie discussion topics
    print("\n🎬 Creating starter codebook...")
    print("These are suggested codes based on common movie discussions.")
    print("You can modify, add, or remove codes as you go through the data.\n")
    
    codebook = {
        'anticipation': {
            'name': 'Pre-release Anticipation/Hype',
            'definition': 'Posts expressing excitement, speculation, or anticipation before the movie release'
        },
        'box_office': {
            'name': 'Box Office Performance',
            'definition': 'Discussion of ticket sales, financial performance, box office records'
        },
        'comparison': {
            'name': 'Movie Comparisons',
            'definition': 'Comparing the movie to other films, franchises, or discussing Barbenheimer phenomenon'
        },
        'reactions_and_reviews': {
            'name': 'Reactions and Reviews',
            'definition': 'Posts discussing the film\'s quality, themes, plot, acting, direction, or other creative elements. Includes both brief reactions and in-depth critical analysis.'
        },
        'cultural_impact': {
            'name': 'Cultural/Social Impact',
            'definition': 'Discussion of the movie\'s social, political, or cultural significance and impact'
        },
        'technical_aspects': {
            'name': 'Technical/Production Discussion',
            'definition': 'Discussion of special effects, soundtrack, cinematography, IMAX, technical achievements'
        }
    }
    
    with open(CODEBOOK_FILE, 'w') as f:
        json.dump(codebook, f, indent=2)
    
    print("✓ Starter codebook created!")
    return codebook

def load_annotations():
    """Load existing annotations"""
    if os.path.exists(ANNOTATIONS_FILE):
        try:
            df = pd.read_csv(ANNOTATIONS_FILE)
            if len(df) > 0:
                return dict(zip(df['post_id'], df['topic_code']))
        except (pd.errors.EmptyDataError, KeyError):
            # File exists but is empty or malformed
            return {}
    return {}

def save_annotations(annotations):
    """Save annotations to CSV"""
    annotations_list = [
        {'post_id': post_id, 'topic_code': code}
        for post_id, code in annotations.items()
    ]
    df = pd.DataFrame(annotations_list)
    df.to_csv(ANNOTATIONS_FILE, index=False)

def display_codebook(codebook):
    """Display the codebook"""
    print("\n📋 CODEBOOK:")
    print("="*80)
    for code_id, info in codebook.items():
        print(f"[{code_id}] {info['name']}")
        print(f"    {info['definition']}")
        print()

def display_batch(df, start_idx, batch_size, annotations):
    """Display a batch of posts"""
    print("\n" + "="*100)
    print(f"BATCH: Posts {start_idx + 1} to {min(start_idx + batch_size, len(df))}")
    print("="*100)
    
    for i in range(start_idx, min(start_idx + batch_size, len(df))):
        row = df.iloc[i]
        post_id = row['id']
        
        # Check if already annotated
        status = f" [ANNOTATED: {annotations[post_id]}]" if post_id in annotations else ""
        
        print(f"\n[{i}] Post ID: {post_id}{status}")
        print(f"    Movie: {row['movie_primary_label']}")
        print(f"    Subreddit: r/{row['subreddit']} | Score: {row['score']}")
        print(f"    TITLE: {row['title']}")
        
        # Show snippet of text
        selftext = str(row['selftext']) if pd.notna(row['selftext']) else ""
        if len(selftext) > 150:
            print(f"    TEXT: {selftext[:150]}...")
        elif selftext:
            print(f"    TEXT: {selftext}")
        print("-"*100)

def annotate_batch(df, start_idx, batch_size, codebook, annotations):
    """Annotate a batch of posts"""
    batch_annotations = {}
    
    for i in range(start_idx, min(start_idx + batch_size, len(df))):
        row = df.iloc[i]
        post_id = row['id']
        
        if post_id in annotations:
            # Already annotated, ask if want to change
            change = input(f"[{i}] Already annotated as '{annotations[post_id]}'. Change? (y/n/code): ").strip().lower()
            if change == 'n' or change == '':
                batch_annotations[post_id] = annotations[post_id]
                continue
            elif change == 'y':
                pass  # Will ask for new code below
            elif change in codebook:
                batch_annotations[post_id] = change
                print(f"    ✓ Changed to: {change}")
                continue
        
        # Get annotation
        while True:
            code = input(f"[{i}] Code (or 'skip'/'help'): ").strip().lower()
            
            if code == 'skip':
                print(f"    ⏭️  Skipped")
                break
            elif code == 'help':
                display_codebook(codebook)
            elif code in codebook:
                batch_annotations[post_id] = code
                print(f"    ✓ Annotated as: {code}")
                break
            else:
                print(f"    ❌ Invalid code. Available: {list(codebook.keys())}")
    
    return batch_annotations

def quick_review(df, annotations, codebook):
    """Quick review of all annotations"""
    print("\n" + "="*100)
    print("📊 QUICK REVIEW")
    print("="*100)
    
    # Show distribution
    if annotations:
        annotations_df = pd.DataFrame([
            {'post_id': k, 'code': v} for k, v in annotations.items()
        ])
        
        print("\nCode Distribution:")
        code_counts = annotations_df['code'].value_counts()
        for code, count in code_counts.items():
            code_name = codebook.get(code, {}).get('name', 'Unknown')
            percentage = (count / len(annotations_df)) * 100
            print(f"  [{code}] {code_name}: {count} ({percentage:.1f}%)")
        
        print(f"\nTotal annotated: {len(annotations)}/{len(df)} ({len(annotations)/len(df)*100:.1f}%)")
        print(f"Remaining: {len(df) - len(annotations)}")
    else:
        print("No annotations yet!")

def main():
    print("\n" + "="*100)
    print("🎬 COMP 370 - Batch Annotation Tool")
    print("="*100)
    
    # Load data
    if not os.path.exists(SAMPLE_FILE):
        print(f"❌ Error: {SAMPLE_FILE} not found!")
        print("Please make sure annotation_sample.csv is in the current directory.")
        return
    
    df = pd.read_csv(SAMPLE_FILE)
    print(f"✓ Loaded {len(df)} posts")
    
    # Load or create codebook
    codebook = load_or_create_codebook()
    print(f"✓ Loaded codebook with {len(codebook)} codes")
    
    # Load existing annotations
    annotations = load_annotations()
    if annotations:
        print(f"✓ Loaded {len(annotations)} existing annotations")
    
    display_codebook(codebook)
    
    # Find first unannotated post
    start_idx = 0
    for i in range(len(df)):
        if df.iloc[i]['id'] not in annotations:
            start_idx = i
            break
    
    print(f"\nStarting from post {start_idx + 1}")
    print("\nInstructions:")
    print("  - Review each batch of posts")
    print("  - Enter the code ID for each post")
    print("  - Type 'skip' to skip a post")
    print("  - Type 'help' to see the codebook again")
    print("  - Type 'quit' at any prompt to save and exit")
    
    input("\nPress Enter to start annotating...")
    
    # Annotation loop
    current_idx = start_idx
    
    while current_idx < len(df):
        # Display batch
        display_batch(df, current_idx, BATCH_SIZE, annotations)
        display_codebook(codebook)
        
        print(f"\n📊 Progress: {len(annotations)}/{len(df)} annotated")
        print("\nAnnotate this batch? (y/n/jump/review/quit)")
        choice = input("Choice: ").strip().lower()
        
        if choice == 'quit' or choice == 'q':
            save_annotations(annotations)
            print("\n✓ Annotations saved!")
            quick_review(df, annotations, codebook)
            break
        elif choice == 'review' or choice == 'r':
            quick_review(df, annotations, codebook)
            continue
        elif choice == 'jump' or choice == 'j':
            try:
                jump_to = int(input("Jump to post number (1-200): ")) - 1
                if 0 <= jump_to < len(df):
                    current_idx = jump_to
                else:
                    print("Invalid post number!")
            except ValueError:
                print("Invalid input!")
            continue
        elif choice == 'n':
            current_idx += BATCH_SIZE
            continue
        
        # Annotate batch
        batch_annotations = annotate_batch(df, current_idx, BATCH_SIZE, codebook, annotations)
        annotations.update(batch_annotations)
        save_annotations(annotations)
        print(f"\n✓ Batch saved! ({len(annotations)}/{len(df)} total)")
        
        current_idx += BATCH_SIZE
    
    print("\n" + "="*100)
    print("ANNOTATION COMPLETE!")
    print("="*100)
    quick_review(df, annotations, codebook)
    print(f"\n✓ Files saved:")
    print(f"  - {CODEBOOK_FILE}")
    print(f"  - {ANNOTATIONS_FILE}")


if __name__ == "__main__":
    main()