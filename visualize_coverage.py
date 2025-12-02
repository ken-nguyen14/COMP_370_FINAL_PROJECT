import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("\n" + "="*80)
    print("📊 Creating Movie Coverage Visualizations (Question 2)")
    print("="*80)
    
    # Load data
    print("\n1. Loading data...")
    posts_df = pd.read_csv('data/reddit_movies_posts.csv')
    annotations_df = pd.read_csv('data/annotations_complete.csv')
    
    # Merge
    df = posts_df.merge(annotations_df, left_on='id', right_on='post_id', how='inner')
    print(f"   ✓ Loaded {len(df)} annotated posts")
    
    # Calculate coverage by movie
    print("\n2. Calculating coverage by movie...")
    coverage = df['movie_primary_label'].value_counts()
    coverage_pct = (coverage / len(df) * 100).round(1)
    
    print("\n   Movie Coverage:")
    for movie, count in coverage.items():
        pct = coverage_pct[movie]
        print(f"   {movie}: {count} posts ({pct}%)")
    
    # Get dominant topic per movie
    print("\n3. Finding dominant topic per movie...")
    dominant_topics = {}
    for movie in df['movie_primary_label'].unique():
        movie_posts = df[df['movie_primary_label'] == movie]
        dominant_topic = movie_posts['topic_code'].value_counts().index[0]
        dominant_topics[movie] = dominant_topic
        print(f"   {movie}: {dominant_topic}")
    
    # Create visualizations
    print("\n4. Creating visualizations...")
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Movie Coverage Analysis - Summer 2023 Films', fontsize=16, fontweight='bold')
    
    # ============================================================================
    # Chart 1: Bar Chart - Posts per Movie
    # ============================================================================
    ax1 = axes[0, 0]
    colors = sns.color_palette("husl", len(coverage))
    coverage.plot(kind='bar', ax=ax1, color=colors)
    ax1.set_title('Coverage by Movie (Post Count)', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Movie', fontsize=10)
    ax1.set_ylabel('Number of Posts', fontsize=10)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for i, v in enumerate(coverage.values):
        ax1.text(i, v + 3, str(v), ha='center', va='bottom', fontweight='bold')
    
    # ============================================================================
    # Chart 2: Pie Chart - Coverage Percentage
    # ============================================================================
    ax2 = axes[0, 1]
    ax2.pie(coverage_pct, labels=coverage_pct.index, autopct='%1.1f%%', 
            colors=colors, startangle=90, textprops={'fontsize': 9})
    ax2.set_title('Coverage by Movie (Percentage)', fontweight='bold', fontsize=12)
    
    # ============================================================================
    # Chart 3: Horizontal Bar - Coverage with Topic Colors
    # ============================================================================
    ax3 = axes[1, 0]
    
    # Create horizontal bar chart
    y_pos = range(len(coverage))
    ax3.barh(y_pos, coverage.values, color=colors)
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(coverage.index, fontsize=9)
    ax3.set_xlabel('Number of Posts', fontsize=10)
    ax3.set_title('Movie Coverage (Horizontal)', fontweight='bold', fontsize=12)
    
    # Add value labels
    for i, v in enumerate(coverage.values):
        pct = coverage_pct.values[i]
        ax3.text(v + 2, i, f'{v} ({pct}%)', va='center', fontweight='bold', fontsize=9)
    
    # ============================================================================
    # Chart 4: Coverage Table
    # ============================================================================
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Create coverage table data
    table_data = []
    for movie in coverage.index:
        count = coverage[movie]
        pct = coverage_pct[movie]
        dominant = dominant_topics[movie]
        table_data.append([movie, count, f"{pct}%", dominant])
    
    # Create table
    table = ax4.table(cellText=table_data,
                     colLabels=['Movie', 'Posts', '%', 'Dominant Topic'],
                     cellLoc='left',
                     loc='center',
                     colWidths=[0.35, 0.15, 0.15, 0.35])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(4):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#E7E6E6')
    
    ax4.set_title('Coverage Summary Table', fontweight='bold', fontsize=12, pad=20)
    
    # ============================================================================
    # Save and display
    # ============================================================================
    plt.tight_layout()
    
    output_file = 'data/movie_coverage_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved visualization to: {output_file}")
    
    plt.show()
    
    # ============================================================================
    # Create coverage table CSV
    # ============================================================================
    print("\n5. Creating coverage table CSV...")
    
    coverage_table = pd.DataFrame({
        'movie': coverage.index,
        'total_posts': coverage.values,
        'percentage': coverage_pct.values,
        'dominant_topic': [dominant_topics[m] for m in coverage.index]
    })
    
    coverage_csv = 'data/movie_coverage_table.csv'
    coverage_table.to_csv(coverage_csv, index=False)
    print(f"   ✓ Saved to: {coverage_csv}")
    
    # Display table
    print("\n" + "="*80)
    print("📋 COVERAGE TABLE")
    print("="*80)
    print(coverage_table.to_string(index=False))
    
    # ============================================================================
    # Additional statistics
    # ============================================================================
    print("\n" + "="*80)
    print("📊 ADDITIONAL STATISTICS")
    print("="*80)
    
    # Barbenheimer combined
    barbenheimer_movies = ['Barbie', 'Oppenheimer']
    barbenheimer_count = coverage[coverage.index.isin(barbenheimer_movies)].sum()
    barbenheimer_pct = (barbenheimer_count / len(df) * 100).round(1)
    
    print(f"\nBarbenheimer Combined:")
    print(f"   Posts: {barbenheimer_count}")
    print(f"   Percentage: {barbenheimer_pct}%")
    
    # Coverage ratio (highest to lowest)
    highest = coverage.iloc[0]
    lowest = coverage.iloc[-1]
    ratio = highest / lowest
    
    print(f"\nCoverage Ratio:")
    print(f"   Highest: {coverage.index[0]} ({highest} posts)")
    print(f"   Lowest: {coverage.index[-1]} ({lowest} posts)")
    print(f"   Ratio: {ratio:.1f}:1")
    
    # Average posts per movie
    avg_posts = coverage.mean()
    print(f"\nAverage posts per movie: {avg_posts:.1f}")
    
    print("\n" + "="*80)
    print("✅ SUCCESS! Coverage visualizations created.")
    print("="*80)
    
    print(f"\n📁 Files created:")
    print(f"   1. {output_file} - Visualization (4 charts)")
    print(f"   2. {coverage_csv} - Coverage table")
    
    print(f"\n📝 For your report:")
    print(f"   - Include the visualization as 'Figure 2: Movie Coverage Analysis'")
    print(f"   - Include the coverage table")
    print(f"   - Discuss Barbenheimer dominance ({barbenheimer_pct}%)")
    print(f"   - Note the {ratio:.1f}:1 ratio between most and least covered")


if __name__ == "__main__":
    main()