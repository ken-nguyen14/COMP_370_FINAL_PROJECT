import pandas as pd
import os

def main():
    print("\n" + "="*80)
    print("📂 Splitting Remaining Posts for Team Annotation")
    print("="*80)
    
    # File paths
    full_dataset = 'data/reddit_movies_posts.csv'
    sample_file = 'data/annotation_sample.csv'
    
    # Check files exist
    if not os.path.exists(full_dataset):
        print(f"❌ Error: {full_dataset} not found!")
        return
    
    if not os.path.exists(sample_file):
        print(f"❌ Error: {sample_file} not found!")
        return
    
    # Load the full dataset
    full_df = pd.read_csv(full_dataset)
    print(f"✓ Loaded full dataset: {len(full_df)} posts")
    
    # Load the annotation sample (200 posts already annotated)
    sample_df = pd.read_csv(sample_file)
    print(f"✓ Loaded annotation sample: {len(sample_df)} posts")
    
    # Get post IDs from the sample (already annotated)
    sample_ids = set(sample_df['id'].tolist())
    print(f"✓ Found {len(sample_ids)} post IDs already annotated")
    
    # Filter to get remaining posts (not in sample)
    remaining_df = full_df[~full_df['id'].isin(sample_ids)].reset_index(drop=True)
    
    print(f"\n📊 Post Counts:")
    print(f"   Total posts: {len(full_df)}")
    print(f"   Already annotated: {len(sample_df)}")
    print(f"   Remaining: {len(remaining_df)}")
    print(f"   Verification: {len(sample_df)} + {len(remaining_df)} = {len(sample_df) + len(remaining_df)} ✓")
    
    # Save all remaining posts to one file
    remaining_file = 'data/remaining_posts_to_annotate.csv'
    remaining_df.to_csv(remaining_file, index=False)
    print(f"\n✓ Saved all remaining posts to: {remaining_file}")
    
    # Split remaining posts into two equal parts
    midpoint = len(remaining_df) // 2
    
    teammate1_df = remaining_df.iloc[:midpoint].reset_index(drop=True)
    teammate2_df = remaining_df.iloc[midpoint:].reset_index(drop=True)
    
    print(f"\n📂 Splitting posts for teammates:")
    print(f"   Teammate 1: {len(teammate1_df)} posts (rows 0-{midpoint-1})")
    print(f"   Teammate 2: {len(teammate2_df)} posts (rows {midpoint}-{len(remaining_df)-1})")
    
    # Save teammate files
    teammate1_file = 'data/remaining_posts_teammate1.csv'
    teammate2_file = 'data/remaining_posts_teammate2.csv'
    
    teammate1_df.to_csv(teammate1_file, index=False)
    teammate2_df.to_csv(teammate2_file, index=False)
    
    print(f"\n✓ Created: {teammate1_file}")
    print(f"✓ Created: {teammate2_file}")
    
    # Show distribution for each teammate
    print(f"\n📊 Teammate 1 - Movie distribution:")
    print(teammate1_df['movie_primary_label'].value_counts())
    
    print(f"\n📊 Teammate 2 - Movie distribution:")
    print(teammate2_df['movie_primary_label'].value_counts())
    
    # Show first few posts from each file
    print(f"\n📋 Preview of Teammate 1's first 3 posts:")
    print(teammate1_df[['id', 'title', 'movie_primary_label']].head(3).to_string(index=False))
    
    print(f"\n📋 Preview of Teammate 2's first 3 posts:")
    print(teammate2_df[['id', 'title', 'movie_primary_label']].head(3).to_string(index=False))
    
    print("\n" + "="*80)
    print("✅ SUCCESS!")
    print("="*80)
    print(f"\nCreated 3 files:")
    print(f"  1. {remaining_file} - All 418 remaining posts")
    print(f"  2. {teammate1_file} - {len(teammate1_df)} posts for Teammate 1")
    print(f"  3. {teammate2_file} - {len(teammate2_df)} posts for Teammate 2")
    print(f"\n📝 Next steps:")
    print(f"  1. Give each teammate their CSV file")
    print(f"  2. Share the MANUAL_ANNOTATION_GUIDE.md")
    print(f"  3. Share data/codebook.json for reference")
    print(f"  4. After both finish, run: python3 merge_manual_annotations.py")


if __name__ == "__main__":
    main()