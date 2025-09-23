#!/usr/bin/env python3
"""
Symptom-Brand Distribution Analysis
Creates individual brand distribution graphs for each symptom for journal publication
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def load_and_analyze_data(filename):
    """Load Excel data and analyze symptoms"""
    df = pd.read_excel(filename)
    print(f"Dataset loaded: {df.shape[0]} patients")
    
    # Get top 15 symptoms information
    symptoms_counts = df['Symptoms'].value_counts().sort_values(ascending=False).head(15)
    print(f"\nTop 15 Symptoms:")
    for i, (symptom, count) in enumerate(symptoms_counts.items(), 1):
        print(f"  {i:2d}. {symptom}: {count} patients")
    
    return df, symptoms_counts

def get_brand_distribution(symptom_data):
    """Get brand distribution for patients with specific symptom"""
    brand_counts = symptom_data['Brand name'].value_counts().sort_values(ascending=False)
    return brand_counts

def create_symptom_brand_graph(symptom_data, symptom_name, total_patients, output_dir, color_scheme):
    """Create a publication-ready graph for a specific symptom showing brand distribution"""
    
    # Set up the style for publication
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    
    # Get brand distribution
    brand_counts = get_brand_distribution(symptom_data)
    
    # Limit to top 15 brands if more than 15
    if len(brand_counts) > 15:
        brand_counts = brand_counts.head(15)
        title_suffix = f" (Top 15 of {len(symptom_data['Brand name'].unique())})"
    else:
        title_suffix = ""
    
    # Create the bar chart
    x_positions = range(len(brand_counts))
    bars = ax.bar(x_positions, brand_counts.values, 
                  color=color_scheme['color'], 
                  edgecolor=color_scheme['edge'], 
                  linewidth=1.2,
                  alpha=0.8)
    
    # Customize the plot for journal publication
    ax.set_xlabel('Brand Name', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Patients', fontsize=14, fontweight='bold')
    
    # Create title with symptom name and total patients
    title = f'Brand Distribution for Patients with "{symptom_name.title()}"\n(Total: {total_patients} patients{title_suffix})'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=25)
    
    # Set x-axis labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(brand_counts.index, fontsize=11, rotation=45, ha='right')
    
    # Customize y-axis
    max_count = max(brand_counts.values) if len(brand_counts) > 0 else 1
    ax.set_ylim(0, max_count * 1.15)
    ax.tick_params(axis='y', labelsize=12)
    
    # Add value labels on top of bars
    for i, (bar, count) in enumerate(zip(bars, brand_counts.values)):
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
    safe_filename = symptom_name.replace(' ', '_').replace(',', '').replace("'", '').replace('.', '').replace('/', '_').lower()
    output_filename = os.path.join(output_dir, f'{safe_filename}_brand_distribution.png')
    
    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"\nGraph saved for '{symptom_name}': {output_filename}")
    
    # Display statistics for this symptom
    print(f"Brand Distribution for '{symptom_name}' ({total_patients} patients):")
    for i, (brand, count) in enumerate(brand_counts.items(), 1):
        print(f"  {i:2d}. {brand}: {count} patients")
        if i >= 10:  # Limit console output to top 10
            if len(brand_counts) > 10:
                print(f"      ... and {len(brand_counts) - 10} more brands")
            break
    
    plt.close()  # Close the figure to free memory
    
    return output_filename

def get_color_schemes():
    """Return journal-appropriate color schemes for different symptoms"""
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

def create_summary_report(df, symptoms_counts, output_dir):
    """Create a summary report of all symptoms and their brand distributions"""
    summary_file = os.path.join(output_dir, 'symptoms_brand_summary.txt')
    
    with open(summary_file, 'w') as f:
        f.write("Symptoms Brand Distribution Summary\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Total Patients: {len(df)}\n")
        f.write(f"Total Unique Symptoms: {len(df['Symptoms'].unique())}\n")
        f.write(f"Analyzed Top 15 Symptoms\n\n")
        
        for i, (symptom, count) in enumerate(symptoms_counts.items(), 1):
            symptom_data = df[df['Symptoms'] == symptom]
            brand_counts = get_brand_distribution(symptom_data)
            
            f.write(f"{i:2d}. {symptom.title()}:\n")
            f.write(f"    Total Patients: {count}\n")
            f.write(f"    Unique Brands: {len(brand_counts)}\n")
            f.write(f"    Top Brand: {brand_counts.index[0]} ({brand_counts.iloc[0]} patients)\n")
            f.write("\n")
    
    print(f"\nSummary report saved: {summary_file}")

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'symptoms_brand_graphs'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, symptoms_counts = load_and_analyze_data('521.xlsx')
        
        # Get color schemes
        color_schemes = get_color_schemes()
        
        print(f"\n{'='*80}")
        print("Generating individual brand distribution graphs for each symptom...")
        print(f"{'='*80}")
        
        # Create individual graphs for each symptom
        generated_files = []
        for i, (symptom, total_patients) in enumerate(symptoms_counts.items()):
            symptom_data = df[df['Symptoms'] == symptom]
            color_scheme = color_schemes[i % len(color_schemes)]
            output_file = create_symptom_brand_graph(symptom_data, symptom, total_patients, output_dir, color_scheme)
            generated_files.append(output_file)
        
        # Create summary report
        create_summary_report(df, symptoms_counts, output_dir)
        
        print(f"\n{'='*80}")
        print("All graphs generated successfully!")
        print(f"Total files created: {len(generated_files)}")
        print(f"Output directory: {output_dir}/")
        print("Files created:")
        for file in generated_files:
            print(f"  - {os.path.basename(file)}")
        print(f"{'='*80}")
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()