#!/usr/bin/env python3
"""
Generic Name Age Distribution Analysis
Creates individual age distribution graphs for each generic drug name for journal publication
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def load_and_analyze_data(filename):
    """Load Excel data and analyze generic names"""
    df = pd.read_excel(filename)
    print(f"Dataset loaded: {df.shape[0]} patients")
    
    # Get generic name information
    generic_counts = df['Generic name'].value_counts().sort_values(ascending=False)
    print(f"\nGeneric Names ({len(generic_counts)} total):")
    for generic, count in generic_counts.items():
        print(f"  {generic}: {count} patients")
    
    return df, generic_counts

def create_age_bins(ages):
    """Create age bins similar to the reference image"""
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    bin_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    
    # Count patients in each age group
    age_counts, _ = np.histogram(ages, bins=bins)
    
    return bins, bin_labels, age_counts

def get_gender_distribution(generic_data):
    """Get male/female distribution for the generic drug"""
    gender_counts = generic_data['Gender'].value_counts()
    male_count = gender_counts.get('Male', 0) + gender_counts.get('male', 0) + gender_counts.get('M', 0)
    female_count = gender_counts.get('Female', 0) + gender_counts.get('female', 0) + gender_counts.get('F', 0)
    
    return male_count, female_count

def create_generic_name_graph(generic_data, generic_name, total_patients, output_dir, color_scheme):
    """Create a publication-ready graph for a specific generic drug"""
    
    # Set up the style for publication
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    
    # Create age bins
    bins, bin_labels, age_counts = create_age_bins(generic_data['Age'])
    
    # Get gender distribution
    male_count, female_count = get_gender_distribution(generic_data)
    
    # Create the bar chart with journal-appropriate colors
    x_positions = range(len(bin_labels))
    bars = ax.bar(x_positions, age_counts, 
                  color=color_scheme['color'], 
                  edgecolor=color_scheme['edge'], 
                  linewidth=1.2,
                  alpha=0.8)
    
    # Customize the plot for journal publication
    ax.set_xlabel('Age Limit (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Patients', fontsize=14, fontweight='bold')
    
    # Create title with generic name, total patients, and gender distribution
    title = f'Age Distribution of Patients\n{generic_name.title()} (Total: {total_patients} patients)\nMale: {male_count}, Female: {female_count}'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=25)
    
    # Set x-axis labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bin_labels, fontsize=12, rotation=0)
    
    # Customize y-axis
    max_count = max(age_counts) if max(age_counts) > 0 else 1
    ax.set_ylim(0, max_count * 1.15)
    ax.tick_params(axis='y', labelsize=12)
    
    # Add value labels on top of bars
    for i, (bar, count) in enumerate(zip(bars, age_counts)):
        if count > 0:  # Only show labels for non-zero counts
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_count * 0.02,
                   str(count), ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Create safe filename
    safe_filename = generic_name.replace(' ', '_').replace("'", '').replace('.', '').lower()
    output_filename = os.path.join(output_dir, f'{safe_filename}_age_distribution.png')
    
    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"\nGraph saved for {generic_name}: {output_filename}")
    
    # Display statistics for this generic drug
    print(f"Age Distribution for {generic_name}:")
    print(f"  Total Patients: {total_patients} (Male: {male_count}, Female: {female_count})")
    total_in_bins = 0
    for label, count in zip(bin_labels, age_counts):
        if count > 0:
            print(f"  {label} years: {count} patients")
            total_in_bins += count
    
    if total_in_bins != total_patients:
        print(f"  Note: {total_patients - total_in_bins} patients may be outside age ranges")
    
    plt.close()  # Close the figure to free memory
    
    return output_filename

def get_color_schemes():
    """Return journal-appropriate color schemes for different generic drugs"""
    # Using professional, journal-appropriate colors that are distinguishable and print-friendly
    colors = [
        {'color': '#2E8B57', 'edge': '#1F5F3F'},  # Sea Green
        {'color': '#4682B4', 'edge': '#2F4F4F'},  # Steel Blue
        {'color': '#8B4513', 'edge': '#5D2F0A'},  # Saddle Brown
        {'color': '#6A5ACD', 'edge': '#4B0082'},  # Slate Blue
        {'color': '#20B2AA', 'edge': '#008B8B'},  # Light Sea Green
        {'color': '#CD853F', 'edge': '#8B4513'},  # Peru
        {'color': '#708090', 'edge': '#2F4F4F'},  # Slate Gray
        {'color': '#9932CC', 'edge': '#4B0082'},  # Dark Orchid
        {'color': '#228B22', 'edge': '#006400'},  # Forest Green
    ]
    return colors

def create_summary_report(df, generic_counts, output_dir):
    """Create a summary report of all generic drugs"""
    summary_file = os.path.join(output_dir, 'generic_drugs_summary.txt')
    
    with open(summary_file, 'w') as f:
        f.write("Generic Drugs Age Distribution Summary\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Total Patients: {len(df)}\n")
        f.write(f"Total Generic Drugs: {len(generic_counts)}\n\n")
        
        for generic, count in generic_counts.items():
            generic_data = df[df['Generic name'] == generic]
            male_count, female_count = get_gender_distribution(generic_data)
            
            f.write(f"{generic.title()}:\n")
            f.write(f"  Total Patients: {count}\n")
            f.write(f"  Male: {male_count}, Female: {female_count}\n")
            f.write(f"  Age Range: {generic_data['Age'].min()}-{generic_data['Age'].max()} years\n")
            f.write(f"  Mean Age: {generic_data['Age'].mean():.1f} ± {generic_data['Age'].std():.1f} years\n")
            f.write("\n")
    
    print(f"\nSummary report saved: {summary_file}")

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'generic_name_graphs'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, generic_counts = load_and_analyze_data('521.xlsx')
        
        # Get color schemes
        color_schemes = get_color_schemes()
        
        print(f"\n{'='*70}")
        print("Generating individual age distribution graphs for each generic drug...")
        print(f"{'='*70}")
        
        # Create individual graphs for each generic drug
        generated_files = []
        for i, (generic, total_patients) in enumerate(generic_counts.items()):
            generic_data = df[df['Generic name'] == generic]
            color_scheme = color_schemes[i % len(color_schemes)]
            output_file = create_generic_name_graph(generic_data, generic, total_patients, output_dir, color_scheme)
            generated_files.append(output_file)
        
        # Create summary report
        create_summary_report(df, generic_counts, output_dir)
        
        print(f"\n{'='*70}")
        print("All graphs generated successfully!")
        print(f"Total files created: {len(generated_files)}")
        print(f"Output directory: {output_dir}/")
        print("Files created:")
        for file in generated_files:
            print(f"  - {os.path.basename(file)}")
        print(f"{'='*70}")
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()