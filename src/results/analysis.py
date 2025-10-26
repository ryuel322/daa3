import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
import numpy as np

def analyze_performance():
    print("=== Generating Performance Charts ===")
    
    
    csv_files = glob.glob("results/*_summary.csv")
    
    if not csv_files:
        print("No CSV files found in results/ directory!")
        return
    
    all_data = []
    
    for file in csv_files:
        category = os.path.basename(file).split('_')[0]
        df = pd.read_csv(file)
        df['Category'] = category
        all_data.append(df)
        print(f"Loaded {len(df)} graphs from {category}")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    
   
    create_enhanced_performance_charts(combined_df)
    create_trend_analysis(combined_df)
    create_comparison_charts(combined_df)
    
    print("\n All charts generated successfully!")

def create_enhanced_performance_charts(df):
   
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    
    categories = ['small', 'medium', 'large', 'extra_large']
    colors = {'small': 'green', 'medium': 'blue', 'large': 'orange', 'extra_large': 'red'}
    markers = {'Prim': 'o', 'Kruskal': 's'}
    
    for category in categories:
        cat_data = df[df['Category'] == category]
        if len(cat_data) > 0:
            
            axes[0,0].plot(cat_data['Vertices'], cat_data['PrimTime(ms)'], 
                          color=colors[category], marker='o', linewidth=2, 
                          label=f'Prim {category}', alpha=0.8)
           
            axes[0,0].plot(cat_data['Vertices'], cat_data['KruskalTime(ms)'], 
                          color=colors[category], marker='s', linestyle='--', linewidth=2,
                          label=f'Kruskal {category}', alpha=0.8)
    
    axes[0,0].set_title('Execution Time Trends', fontsize=14, fontweight='bold')
    axes[0,0].set_xlabel('Number of Vertices')
    axes[0,0].set_ylabel('Time (ms)')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
   
    time_means = df.groupby('Category')[['PrimTime(ms)', 'KruskalTime(ms)']].mean()
    x = np.arange(len(time_means))
    width = 0.35
    
    axes[0,1].bar(x - width/2, time_means['PrimTime(ms)'], width, label='Prim', alpha=0.8)
    axes[0,1].bar(x + width/2, time_means['KruskalTime(ms)'], width, label='Kruskal', alpha=0.8)
    
    axes[0,1].set_title('Average Execution Time by Category', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('Category')
    axes[0,1].set_ylabel('Time (ms)')
    axes[0,1].set_xticks(x)
    axes[0,1].set_xticklabels(time_means.index)
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
   
    df['Speedup_Ratio'] = df['KruskalTime(ms)'] / df['PrimTime(ms)']
    speedup_data = df.groupby('Category')['Speedup_Ratio'].agg(['mean', 'std']).fillna(0)
    
    bars = axes[1,0].bar(speedup_data.index, speedup_data['mean'], 
                        yerr=speedup_data['std'], capsize=5, alpha=0.7,
                        color=['green', 'blue', 'orange', 'red'])
    axes[1,0].axhline(1, color='black', linestyle='--', linewidth=2, label='Equal Performance')
    axes[1,0].set_title('Speedup Ratio (Kruskal/Prim)', fontsize=14, fontweight='bold')
    axes[1,0].set_ylabel('Speedup Ratio')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
   
    ops_means = df.groupby('Category')[['PrimOperations', 'KruskalOperations']].mean()
    x = np.arange(len(ops_means))
    
    axes[1,1].bar(x - width/2, ops_means['PrimOperations'], width, label='Prim', alpha=0.8)
    axes[1,1].bar(x + width/2, ops_means['KruskalOperations'], width, label='Kruskal', alpha=0.8)
    
    axes[1,1].set_title('Average Operations Count', fontsize=14, fontweight='bold')
    axes[1,1].set_xlabel('Category')
    axes[1,1].set_ylabel('Operations')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(ops_means.index)
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].set_yscale('log')  
    
    plt.tight_layout()
    plt.savefig('results/performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_trend_analysis(df):
    """Анализ трендов"""
    plt.figure(figsize=(14, 10))
    
    
    plt.subplot(2, 2, 1)
    
    for algorithm, color, marker in [('Prim', 'blue', 'o'), ('Kruskal', 'red', 's')]:
        x = df['Vertices']
        y = df[f'{algorithm}Time(ms)']
        
       
        plt.scatter(x, y, alpha=0.6, color=color, marker=marker, label=algorithm, s=50)
        
        
        if len(x) > 1:
            z = np.polyfit(x, y, 2)
            p = np.poly1d(z)
            x_trend = np.linspace(x.min(), x.max(), 100)
            plt.plot(x_trend, p(x_trend), color=color, linewidth=2, alpha=0.8)
    
    plt.xlabel('Vertices')
    plt.ylabel('Time (ms)')
    plt.title('Execution Time Trends with Polynomial Fit')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    
    plt.subplot(2, 2, 2)
    
    prim_times = df['PrimTime(ms)']
    kruskal_times = df['KruskalTime(ms)']
    
    plt.hist(prim_times, alpha=0.7, label='Prim', bins=10, color='blue')
    plt.hist(kruskal_times, alpha=0.7, label='Kruskal', bins=10, color='red')
    plt.xlabel('Time (ms)')
    plt.ylabel('Frequency')
    plt.title('Time Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    
    plt.subplot(2, 2, 3)
    
    time_data = []
    labels = []
    for category in ['small', 'medium', 'large', 'extra_large']:
        cat_data = df[df['Category'] == category]
        if len(cat_data) > 0:
            time_data.append(cat_data['PrimTime(ms)'])
            time_data.append(cat_data['KruskalTime(ms)'])
            labels.extend([f'{category}\nPrim', f'{category}\nKruskal'])
    
    if time_data:
        box = plt.boxplot(time_data, labels=labels, patch_artist=True)
        
        colors = ['lightblue', 'lightcoral'] * 4
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)
        plt.title('Time Distribution by Category')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
    
    
    plt.subplot(2, 2, 4)
    
    prim_wins = len(df[df['PrimTime(ms)'] < df['KruskalTime(ms)']])
    kruskal_wins = len(df[df['PrimTime(ms)'] > df['KruskalTime(ms)']])
    ties = len(df) - prim_wins - kruskal_wins
    
    wins_data = [prim_wins, kruskal_wins, ties]
    wins_labels = [f'Prim Wins\n{prim_wins}', f'Kruskal Wins\n{kruskal_wins}', f'Ties\n{ties}']
    colors = ['lightblue', 'lightcoral', 'lightgray']
    
    plt.pie(wins_data, labels=wins_labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Algorithm Performance Wins')
    
    plt.tight_layout()
    plt.savefig('results/trend_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_comparison_charts(df):
    
    plt.figure(figsize=(15, 5))
    
    
    plt.subplot(1, 3, 1)
    
    max_time = max(df['PrimTime(ms)'].max(), df['KruskalTime(ms)'].max())
    plt.plot([0, max_time], [0, max_time], 'k--', alpha=0.5, label='y=x')
    plt.scatter(df['PrimTime(ms)'], df['KruskalTime(ms)'], alpha=0.7, s=60)
    
    for i, row in df.iterrows():
        plt.annotate(row['Category'][0], (row['PrimTime(ms)'], row['KruskalTime(ms)']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.xlabel('Prim Time (ms)')
    plt.ylabel('Kruskal Time (ms)')
    plt.title('Direct Time Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    
    plt.subplot(1, 3, 2)
    
    df['Time_Ratio'] = df['KruskalTime(ms)'] / df['PrimTime(ms)']
    plt.scatter(df['Vertices'], df['Time_Ratio'], alpha=0.7, s=60, c=df['Edges'], cmap='viridis')
    plt.axhline(1, color='red', linestyle='--', alpha=0.7)
    plt.xlabel('Vertices')
    plt.ylabel('Kruskal/Prim Time Ratio')
    plt.title('Time Ratio vs Graph Size')
    plt.colorbar(label='Edges')
    plt.grid(True, alpha=0.3)
    
    
    plt.subplot(1, 3, 3)
    
    df['Ops_Ratio'] = df['KruskalOperations'] / df['PrimOperations']
    plt.scatter(df['Vertices'], df['Ops_Ratio'], alpha=0.7, s=60, c=df['Edges'], cmap='plasma')
    plt.axhline(1, color='red', linestyle='--', alpha=0.7)
    plt.xlabel('Vertices')
    plt.ylabel('Kruskal/Prim Operations Ratio')
    plt.title('Operations Ratio vs Graph Size')
    plt.colorbar(label='Edges')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/comparison_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    analyze_performance()