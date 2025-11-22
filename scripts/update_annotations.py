import pandas as pd
import os

if os.path.exists('data/annotations.csv'):
    df = pd.read_csv('data/annotations.csv')
    
    # Count before
    print("Before update:")
    if 'topic_code' in df.columns:
        print(df['topic_code'].value_counts())
    
    # Update old codes
    df['topic_code'] = df['topic_code'].replace({
        'critical_analysis': 'reactions_and_reviews',
        'general_reaction': 'reactions_and_reviews'
    })
    
    # Save
    df.to_csv('data/annotations.csv', index=False)
    
    print("\n✓ Updated annotations.csv")
    print("\nAfter update:")
    print(df['topic_code'].value_counts())
else:
    print("No annotations file found yet - that's ok!")