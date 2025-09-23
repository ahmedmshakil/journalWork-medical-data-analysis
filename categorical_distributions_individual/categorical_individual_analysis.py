#!/usr/bin/env python3
"""
Individual Categorical Variable Distribution Analysis
Creates separate distribution graphs for each categorical variable for journal publication
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def load_and_analyze_data(filename):
    """Load Excel data and analyze categorical variables"""
    df = pd.read_excel(filename)
    print(f"Dataset loaded: {df.shape[0]} patients")
    
    # Clean gender data - remove trailing/leading spaces and standardize
    if 'Gender' in df.columns:
        print(f"\nCleaning Gender column...")
        print(f"Before cleaning: {df['Gender'].value_counts().to_dict()}")
        df['Gender'] = df['Gender'].str.strip().str.lower()
        # Standardize gender values
        df['Gender'] = df['Gender'].replace({'male': 'Male', 'female': 'Female'})
        print(f"After cleaning: {df['Gender'].value_counts().to_dict()}")
    
    # Get categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    print(f"\nCategorical Variables ({len(categorical_cols)} total):")
    for i, col in enumerate(categorical_cols, 1):
        unique_count = df[col].nunique()
        print(f"  {i:2d}. {col}: {unique_count} unique values")
    
    return df, categorical_cols

def create_individual_categorical_graph(df, column_name, output_dir, color_scheme):
    """Create a publication-ready graph for a specific categorical variable"""
    
    # Set up the style for publication
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    
    # Get value counts for the column
    value_counts = df[column_name].value_counts()
    
    # Limit to top 15 categories if more than 15
    if len(value_counts) > 15:
        value_counts = value_counts.head(15)
        title_suffix = f" (Top 15 of {df[column_name].nunique()})"
    else:
        title_suffix = ""
    
    # Create the bar chart
    x_positions = range(len(value_counts))
    bars = ax.bar(x_positions, value_counts.values, 
                  color=color_scheme['color'], 
                  edgecolor=color_scheme['edge'], 
                  linewidth=1.2,
                  alpha=0.8)
    
    # Customize the plot for journal publication
    ax.set_xlabel(column_name.title(), fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    
    # Create title
    title = f'Distribution of {column_name.title()}{title_suffix}'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=25)
    
    # Set x-axis labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(value_counts.index, fontsize=11, rotation=45, ha='right')
    
    # Customize y-axis
    max_count = max(value_counts.values) if len(value_counts) > 0 else 1
    ax.set_ylim(0, max_count * 1.15)
    ax.tick_params(axis='y', labelsize=12)
    
    # Add value labels on top of bars
    for i, (bar, count) in enumerate(zip(bars, value_counts.values)):
        if count > 0:  # Only show labels for non-zero counts
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_count * 0.02,
                   str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Create safe filename
    safe_filename = column_name.replace(' ', '_').replace(',', '').replace("'", '').replace('.', '').replace('/', '_').lower()
    output_filename = os.path.join(output_dir, f'{safe_filename}_distribution.png')
    
    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"\nGraph saved for '{column_name}': {output_filename}")
    
    # Display statistics for this variable
    print(f"Distribution for '{column_name}':")
    print(f"  Total unique values: {df[column_name].nunique()}")
    print(f"  Total records: {len(df[column_name].dropna())}")
    for i, (category, count) in enumerate(value_counts.items(), 1):
        print(f"  {i:2d}. {category}: {count} ({count/len(df)*100:.1f}%)")
        if i >= 10:  # Limit console output to top 10
            if len(value_counts) > 10:
                print(f"      ... and {len(value_counts) - 10} more categories")
            break
    
    plt.close()  # Close the figure to free memory
    
    return output_filename

def get_color_schemes():
    """Return journal-appropriate color schemes for different categorical variables"""
    # Using professional, journal-appropriate colors
    colors = [
        {'color': '#1f77b4', 'edge': '#0f4c7c'},  # Blue
        {'color': '#ff7f0e', 'edge': '#cc5500'},  # Orange  
        {'color': '#2ca02c', 'edge': '#1a661a'},  # Green
        {'color': '#d62728', 'edge': '#a01c1d'},  # Red
        {'color': '#9467bd', 'edge': '#6b4c87'},  # Purple
        {'color': '#8c564b', 'edge': '#5d3a32'},  # Brown
        {'color': '#e377c2', 'edge': '#b85d91'},  # Pink
        {'color': '#7f7f7f', 'edge': '#4d4d4d'},  # Gray
        {'color': '#bcbd22', 'edge': '#8a8b19'},  # Olive
        {'color': '#17becf', 'edge': '#0f8a9a'},  # Cyan
        {'color': '#aec7e8', 'edge': '#7ba7d9'},  # Light Blue
        {'color': '#ffbb78', 'edge': '#ff9933'},  # Light Orange
        {'color': '#98df8a', 'edge': '#66cc55'},  # Light Green
        {'color': '#ff9896', 'edge': '#ff6666'},  # Light Red
        {'color': '#c5b0d5', 'edge': '#9370db'},  # Light Purple
    ]
    return colors

def create_summary_report(df, categorical_cols, output_dir):
    """Create a summary report of all categorical variables"""
    summary_file = os.path.join(output_dir, 'categorical_variables_summary.txt')
    
    with open(summary_file, 'w') as f:
        f.write("Categorical Variables Distribution Summary\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Total Patients: {len(df)}\n")
        f.write(f"Total Categorical Variables: {len(categorical_cols)}\n\n")
        
        for i, col in enumerate(categorical_cols, 1):
            value_counts = df[col].value_counts()
            
            f.write(f"{i:2d}. {col.title()}:\n")
            f.write(f"    Total unique values: {df[col].nunique()}\n")
            f.write(f"    Most common: {value_counts.index[0]} ({value_counts.iloc[0]} records, {value_counts.iloc[0]/len(df)*100:.1f}%)\n")
            f.write(f"    Missing values: {df[col].isnull().sum()}\n")
            f.write("\n")
    
    print(f"\nSummary report saved: {summary_file}")

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'categorical_distributions_individual'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, categorical_cols = load_and_analyze_data('521.xlsx')
        
        # Get color schemes
        color_schemes = get_color_schemes()
        
        print(f"\n{'='*80}")
        print("Generating individual distribution graphs for each categorical variable...")
        print(f"{'='*80}")
        
        # Create individual graphs for each categorical variable
        generated_files = []
        for i, col in enumerate(categorical_cols):
            color_scheme = color_schemes[i % len(color_schemes)]
            output_file = create_individual_categorical_graph(df, col, output_dir, color_scheme)
            generated_files.append(output_file)
        
        # Create summary report
        create_summary_report(df, categorical_cols, output_dir)
        
        print(f"\n{'='*80}")
        print("All graphs generated successfully!")
        print(f"Total files created: {len(generated_files)}")
        print(f"Output directory: {output_dir}/")
        print("Files created:")
        for file in generated_files:
            print(f"  - {os.path.basename(file)}")
        print(f"{'='*80}")
        
        # Print insights
        print("\nKEY INSIGHTS:")
        print("="*30)
        for i, col in enumerate(categorical_cols, 1):
            value_counts = df[col].value_counts()
            diversity_index = len(value_counts) / len(df)
            
            if diversity_index < 0.1:
                diversity = "Low diversity"
            elif diversity_index < 0.5:
                diversity = "Medium diversity"
            else:
                diversity = "High diversity"
            
            print(f"{i:2d}. {col}: {diversity} ({len(value_counts)} unique values)")
            print(f"    Dominant category: {value_counts.index[0]} ({value_counts.iloc[0]/len(df)*100:.1f}%)")
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()