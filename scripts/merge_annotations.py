import pandas as pd
import os

def main():
    print("\n" + "="*80)
    print("🔄 Merging Manual Annotations")
    print("="*80)
    
    # Files to merge
    files_to_merge = [
        ('data/annotations.csv', 'Original annotations (174 posts)'),
        ('annotated_teammate1.csv', 'Teammate 1 annotations'),
        ('annotated_teammate2.csv', 'Teammate 2 annotations')
    ]
    
    dfs = []
    
    # Load each file
    for filepath, description in files_to_merge:
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                
                # Check if it has the right columns
                if 'post_id' in df.columns and 'topic_code' in df.columns:
                    # Filter out skipped/empty annotations
                    df = df[df['topic_code'].notna()]
                    df = df[df['topic_code'] != '']
                    df = df[df['topic_code'] != 'skip']
                    
                    print(f"✓ Loaded {description}: {len(df)} posts")
                    dfs.append(df)
                else:
                    print(f"⚠️  {filepath} missing required columns (post_id, topic_code)")
            except Exception as e:
                print(f"⚠️  Error loading {filepath}: {e}")
        else:
            print(f"⚠️  {filepath} not found")
    
    if len(dfs) == 0:
        print("\n❌ Error: No annotation files found!")
        return
    
    # Merge all dataframes
    print("\n🔄 Merging all annotations...")
    merged = pd.concat(dfs, ignore_index=True)
    
    # Check for duplicates
    duplicates = merged[merged.duplicated(subset=['post_id'], keep=False)]
    if len(duplicates) > 0:
        print(f"\n⚠️  Found {len(duplicates)//2} duplicate post_ids")
        print("Removing duplicates (keeping first occurrence)...")
        merged = merged.drop_duplicates(subset=['post_id'], keep='first')
    
    # Sort by post_id
    merged = merged.sort_values('post_id').reset_index(drop=True)
    
    # Validate codes
    valid_codes = ['anticipation', 'box_office', 'comparison', 
                   'reactions_and_reviews', 'cultural_impact', 'technical_aspects']
    
    invalid_codes = merged[~merged['topic_code'].isin(valid_codes)]
    if len(invalid_codes) > 0:
        print(f"\n⚠️  Warning: Found {len(invalid_codes)} posts with invalid codes:")
        print(invalid_codes[['post_id', 'topic_code']].head(10))
        print("\nRemoving invalid codes...")
        merged = merged[merged['topic_code'].isin(valid_codes)]
    
    # Save merged file
    output_file = 'data/annotations_complete.csv'
    merged.to_csv(output_file, index=False)
    
    print(f"\n✅ SUCCESS!")
    print("="*80)
    print(f"Total valid annotations: {len(merged)}")
    print(f"\n📊 Code Distribution:")
    print("-"*80)
    
    code_counts = merged['topic_code'].value_counts()
    for code, count in code_counts.items():
        percentage = (count / len(merged)) * 100
        print(f"  {code:25s} {count:4d} ({percentage:5.1f}%)")
    
    print("="*80)
    print(f"\n✓ Merged annotations saved to: {output_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review the distribution above")
    print(f"   2. If looks good, copy to annotations.csv:")
    print(f"      cp {output_file} data/annotations.csv")
    print(f"   3. Proceed to Part 2, Task 3 (TF-IDF analysis)")
    
    # Optionally replace
    response = input("\n❓ Replace data/annotations.csv with merged file? (y/n): ").strip().lower()
    if response == 'y':
        # Backup original
        if os.path.exists('data/annotations.csv'):
            backup_file = 'data/annotations_backup.csv'
            df_backup = pd.read_csv('data/annotations.csv')
            df_backup.to_csv(backup_file, index=False)
            print(f"✓ Backed up original to: {backup_file}")
        
        # Replace
        merged.to_csv('data/annotations.csv', index=False)
        print(f"✓ Updated data/annotations.csv")
        print(f"\n🎉 All done! Ready for Task 3!")


if __name__ == "__main__":
    main()