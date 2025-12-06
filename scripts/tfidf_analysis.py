import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import defaultdict

# Set style for plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("📊 COMP 370 - Part 2, Task 3: Topic Characterization")
print("="*80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

print("\n" + "="*80)
print("STEP 1: Loading Data")
print("="*80)

# Load full dataset
posts_df = pd.read_csv('data/reddit_movies_posts.csv')
print(f"✓ Loaded full dataset: {len(posts_df)} posts")

# Load annotations
annotations_df = pd.read_csv('data/annotations_complete.csv')
print(f"✓ Loaded annotations: {len(annotations_df)} annotated posts")

# Load codebook
with open('data/codebook.json', 'r') as f:
    codebook = json.load(f)
print(f"✓ Loaded codebook: {len(codebook)} codes")

# Merge posts with annotations
df = posts_df.merge(annotations_df, left_on='id', right_on='post_id', how='inner')
print(f"✓ Merged dataset: {len(df)} posts with annotations")

# Show code distribution
print(f"\n📊 Code Distribution:")
print(df['topic_code'].value_counts())
print(f"\nPercentages:")
print((df['topic_code'].value_counts(normalize=True) * 100).round(1))

# ============================================================================
# STEP 2: PREPARE TEXT DATA
# ============================================================================

print("\n" + "="*80)
print("STEP 2: Preparing Text Data")
print("="*80)

# Combine title and selftext for full content
df['full_text'] = df['title'].fillna('') + ' ' + df['selftext'].fillna('')

# Remove very short posts (less than 10 characters)
df = df[df['full_text'].str.len() >= 10].reset_index(drop=True)
print(f"✓ Filtered to posts with sufficient text: {len(df)} posts")

# Show sample
print(f"\n📝 Sample post:")
sample = df.iloc[0]
print(f"Topic: {sample['topic_code']}")
print(f"Title: {sample['title']}")
print(f"Text length: {len(sample['full_text'])} characters")

# ============================================================================
# STEP 3: TF-IDF ANALYSIS PER TOPIC
# ============================================================================

print("\n" + "="*80)
print("STEP 3: TF-IDF Analysis")
print("="*80)

# Initialize results dictionary
tfidf_results = {}

# Parameters for TF-IDF
tfidf_params = {
    'max_features': 1000,
    'min_df': 2,  # Word must appear in at least 2 documents
    'max_df': 0.8,  # Word must appear in less than 80% of documents
    'stop_words': 'english',
    'ngram_range': (1, 2),  # Include both unigrams and bigrams
    'lowercase': True
}

print(f"TF-IDF Parameters:")
print(f"  - max_features: {tfidf_params['max_features']}")
print(f"  - min_df: {tfidf_params['min_df']}")
print(f"  - max_df: {tfidf_params['max_df']}")
print(f"  - ngram_range: {tfidf_params['ngram_range']}")

# Perform TF-IDF analysis for each topic
for code in sorted(df['topic_code'].unique()):
    print(f"\n--- Analyzing: {code} ---")
    
    # Get posts for this topic
    topic_posts = df[df['topic_code'] == code]
    print(f"Posts in this topic: {len(topic_posts)}")
    
    # Get posts from OTHER topics (for comparison)
    other_posts = df[df['topic_code'] != code]
    
    # Combine for TF-IDF
    all_texts = pd.concat([topic_posts['full_text'], other_posts['full_text']])
    labels = ['topic'] * len(topic_posts) + ['other'] * len(other_posts)
    
    # Fit TF-IDF
    vectorizer = TfidfVectorizer(**tfidf_params)
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get TF-IDF scores for topic posts only
    topic_tfidf = tfidf_matrix[:len(topic_posts)].mean(axis=0).A1
    
    # Get top 10 words
    top_indices = topic_tfidf.argsort()[-10:][::-1]
    top_words = [(feature_names[i], topic_tfidf[i]) for i in top_indices]
    
    # Store results
    tfidf_results[code] = {
        'top_words': top_words,
        'num_posts': len(topic_posts),
        'code_name': codebook[code]['name']
    }
    
    # Print top words
    print(f"Top 10 words (by TF-IDF):")
    for i, (word, score) in enumerate(top_words, 1):
        print(f"  {i:2d}. {word:25s} (score: {score:.4f})")

# ============================================================================
# STEP 4: SAVE TF-IDF RESULTS
# ============================================================================

print("\n" + "="*80)
print("STEP 4: Saving TF-IDF Results")
print("="*80)

# Create summary table
tfidf_summary = []
for code, results in tfidf_results.items():
    words = [word for word, score in results['top_words']]
    tfidf_summary.append({
        'topic_code': code,
        'topic_name': results['code_name'],
        'num_posts': results['num_posts'],
        'top_10_words': ', '.join(words)
    })

tfidf_df = pd.DataFrame(tfidf_summary)
tfidf_df = tfidf_df.sort_values('num_posts', ascending=False)

# Save to CSV
tfidf_df.to_csv('data/tfidf_results.csv', index=False)
print(f"✓ Saved TF-IDF results to: data/tfidf_results.csv")

# Display table
print(f"\n📊 TF-IDF Summary:")
print(tfidf_df.to_string(index=False))

# ============================================================================
# STEP 5: PREPARE TEXT FOR LLM SUMMARIZATION
# ============================================================================

print("\n" + "="*80)
print("STEP 5: Preparing Text for LLM Summarization")
print("="*80)

# For each topic, collect sample posts for LLM summary
llm_input = {}

for code in sorted(df['topic_code'].unique()):
    topic_posts = df[df['topic_code'] == code]
    
    # Get up to 20 representative posts (mix of high and low scores)
    # Sort by score and take top 10 and bottom 10
    sorted_posts = topic_posts.sort_values('score', ascending=False)
    
    if len(sorted_posts) >= 20:
        sample_posts = pd.concat([
            sorted_posts.head(10),  # Top 10 by score
            sorted_posts.tail(10)   # Bottom 10 by score
        ])
    else:
        sample_posts = sorted_posts
    
    # Create summary for LLM
    posts_text = []
    for idx, row in sample_posts.iterrows():
        # Handle NaN selftext
        selftext = row['selftext'] if pd.notna(row['selftext']) else ""
        text_preview = selftext[:200] if len(selftext) > 0 else "(no text)"
        post_summary = f"Title: {row['title']}\nContent: {text_preview}..."
        posts_text.append(post_summary)
    
    llm_input[code] = {
        'code_name': codebook[code]['name'],
        'definition': codebook[code]['definition'],
        'num_posts': len(topic_posts),
        'top_words': [word for word, score in tfidf_results[code]['top_words']],
        'sample_posts': posts_text[:10]  # Limit to 10 for LLM
    }
    
    print(f"\n✓ Prepared {code}: {len(posts_text)} sample posts")

# Save LLM input
with open('data/llm_input.json', 'w') as f:
    json.dump(llm_input, f, indent=2)
print(f"\n✓ Saved LLM input to: data/llm_input.json")

# ============================================================================
# STEP 6: CREATE PROMPT FOR CHATGPT
# ============================================================================

print("\n" + "="*80)
print("STEP 6: Creating ChatGPT Prompts")
print("="*80)

# Create prompt for each topic
prompts = {}

for code, data in llm_input.items():
    prompt = f"""I am analyzing Reddit discussions about Summer 2023 movies (Barbie, Oppenheimer, Mission: Impossible, Spider-Man, Guardians of the Galaxy).

I have categorized {data['num_posts']} posts as "{data['code_name']}" defined as:
"{data['definition']}"

The top 10 distinctive words (by TF-IDF) for this category are:
{', '.join(data['top_words'])}

Here are 10 representative post titles from this category:
{chr(10).join([f"{i+1}. {post.split('Content:')[0].replace('Title: ', '')}" for i, post in enumerate(data['sample_posts'])])}

Based on this information, please write a 2-3 sentence summary that characterizes what people are discussing in this category. Focus on:
1. The main themes and topics
2. The tone or sentiment (if applicable)
3. What makes this category distinct from others

Keep the summary concise and factual."""
    
    prompts[code] = prompt
    
    print(f"\n--- Prompt for {code} ---")
    print(prompt)
    print(f"\n{'-'*80}")

# Save prompts to file
with open('data/chatgpt_prompts.txt', 'w') as f:
    for code, prompt in prompts.items():
        f.write(f"{'='*80}\n")
        f.write(f"PROMPT FOR: {code}\n")
        f.write(f"{'='*80}\n\n")
        f.write(prompt)
        f.write(f"\n\n")

print(f"\n✓ Saved ChatGPT prompts to: data/chatgpt_prompts.txt")

# ============================================================================
# STEP 7: VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("STEP 7: Creating Visualizations")
print("="*80)

# Set up figure
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Topic Analysis - Summer 2023 Movie Discussions', fontsize=16, fontweight='bold')

# 1. Topic Distribution (Bar Chart)
ax1 = axes[0, 0]
topic_counts = df['topic_code'].value_counts()
colors = sns.color_palette("husl", len(topic_counts))
topic_counts.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('Distribution of Topics', fontweight='bold')
ax1.set_xlabel('Topic Code')
ax1.set_ylabel('Number of Posts')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(topic_counts):
    ax1.text(i, v + 5, str(v), ha='center', fontweight='bold')

# 2. Topic Distribution (Pie Chart)
ax2 = axes[0, 1]
topic_pct = (df['topic_code'].value_counts(normalize=True) * 100).round(1)
ax2.pie(topic_pct, labels=topic_pct.index, autopct='%1.1f%%', colors=colors, startangle=90)
ax2.set_title('Topic Distribution (Percentage)', fontweight='bold')

# 3. Topics by Movie
ax3 = axes[1, 0]
movie_topic_crosstab = pd.crosstab(df['movie_primary_label'], df['topic_code'], normalize='index') * 100
movie_topic_crosstab.plot(kind='bar', stacked=True, ax=ax3, color=colors)
ax3.set_title('Topic Distribution by Movie (%)', fontweight='bold')
ax3.set_xlabel('Movie')
ax3.set_ylabel('Percentage')
ax3.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
ax3.tick_params(axis='x', rotation=45)

# 4. Posts per Topic (Horizontal Bar)
ax4 = axes[1, 1]
topic_counts_sorted = topic_counts.sort_values()
ax4.barh(range(len(topic_counts_sorted)), topic_counts_sorted.values, color=colors)
ax4.set_yticks(range(len(topic_counts_sorted)))
ax4.set_yticklabels(topic_counts_sorted.index)
ax4.set_xlabel('Number of Posts')
ax4.set_title('Posts per Topic', fontweight='bold')
for i, v in enumerate(topic_counts_sorted.values):
    ax4.text(v + 3, i, str(v), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('data/topic_analysis_visualization.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization to: data/topic_analysis_visualization.png")
plt.show()

# ============================================================================
# STEP 8: SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("STEP 8: Summary Statistics")
print("="*80)

# Overall statistics
print(f"\n📊 Overall Statistics:")
print(f"   Total annotated posts: {len(df)}")
print(f"   Number of topics: {df['topic_code'].nunique()}")
print(f"   Average post score: {df['score'].mean():.1f}")
print(f"   Average post length: {df['full_text'].str.len().mean():.0f} characters")

# Statistics per topic
print(f"\n📊 Statistics per Topic:")
topic_stats = df.groupby('topic_code').agg({
    'id': 'count',
    'score': 'mean',
    'num_comments': 'mean',
    'full_text': lambda x: x.str.len().mean()
}).round(1)
topic_stats.columns = ['num_posts', 'avg_score', 'avg_comments', 'avg_length']
topic_stats = topic_stats.sort_values('num_posts', ascending=False)
print(topic_stats)

# Movie coverage
print(f"\n📊 Movie Coverage:")
movie_counts = df['movie_primary_label'].value_counts()
print(movie_counts)
print(f"\nPercentages:")
print((movie_counts / len(df) * 100).round(1))

# ============================================================================
# FINAL OUTPUT
# ============================================================================

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)

print(f"\n📁 Files Created:")
print(f"   1. data/tfidf_results.csv - Top 10 words per topic")
print(f"   2. data/llm_input.json - Data for LLM summarization")
print(f"   3. data/chatgpt_prompts.txt - Ready-to-use ChatGPT prompts")
print(f"   4. data/topic_analysis_visualization.png - Visualization")

print(f"\n📝 Next Steps:")
print(f"   1. Review the TF-IDF results above")
print(f"   2. Open data/chatgpt_prompts.txt")
print(f"   3. Copy each prompt to ChatGPT")
print(f"   4. Save ChatGPT's summaries")
print(f"   5. Create final report with both TF-IDF words and LLM summaries")

print(f"\n🎉 Ready for final report writing!")