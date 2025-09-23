#!/usr/bin/env python3
"""
Medical Center Age Distribution Analysis
Creates individual age distribution graphs for each medical center for journal publication
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def load_and_analyze_data(filename):
    """Load Excel data and analyze medical centers"""
    df = pd.read_excel(filename)
    print(f"Dataset loaded: {df.shape[0]} patients")
    
    # Get medical center information
    center_counts = df['Medical center'].value_counts().sort_values(ascending=False)
    print(f"\nMedical Centers ({len(center_counts)} total):")
    for center, count in center_counts.items():
        print(f"  {center}: {count} patients")
    
    return df, center_counts

def create_age_bins(ages):
    """Create age bins similar to the reference image"""
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    bin_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    
    # Count patients in each age group
    age_counts, _ = np.histogram(ages, bins=bins)
    
    return bins, bin_labels, age_counts

def create_medical_center_graph(center_data, center_name, total_patients, output_dir):
    """Create a publication-ready graph for a specific medical center"""
    
    # Set up the style for publication
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    
    # Create age bins
    bins, bin_labels, age_counts = create_age_bins(center_data['Age'])
    
    # Create the bar chart
    x_positions = range(len(bin_labels))
    bars = ax.bar(x_positions, age_counts, 
                  color='lightcoral', 
                  edgecolor='darkred', 
                  linewidth=1.2,
                  alpha=0.8)
    
    # Customize the plot for journal publication
    ax.set_xlabel('Age Limit (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Patients', fontsize=14, fontweight='bold')
    
    # Create title with center name and total patients
    title = f'Age Distribution of Patients\n{center_name.title()} (Total: {total_patients} patients)'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Set x-axis labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bin_labels, fontsize=12)
    
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
    safe_filename = center_name.replace(' ', '_').replace("'", '').replace('.', '').lower()
    output_filename = os.path.join(output_dir, f'{safe_filename}_age_distribution.png')
    
    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"\nGraph saved for {center_name}: {output_filename}")
    
    # Display statistics for this center
    print(f"Age Distribution for {center_name}:")
    total_in_bins = 0
    for label, count in zip(bin_labels, age_counts):
        if count > 0:
            print(f"  {label} years: {count} patients")
            total_in_bins += count
    
    if total_in_bins != total_patients:
        print(f"  Note: {total_patients - total_in_bins} patients may be outside age ranges")
    
    plt.close()  # Close the figure to free memory
    
    return output_filename

def create_summary_report(df, center_counts, output_dir):
    """Create a summary report of all medical centers"""
    summary_file = os.path.join(output_dir, 'medical_centers_summary.txt')
    
    with open(summary_file, 'w') as f:
        f.write("Medical Centers Age Distribution Summary\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Total Patients: {len(df)}\n")
        f.write(f"Total Medical Centers: {len(center_counts)}\n\n")
        
        for center, count in center_counts.items():
            center_data = df[df['Medical center'] == center]
            f.write(f"{center.title()}:\n")
            f.write(f"  Total Patients: {count}\n")
            f.write(f"  Age Range: {center_data['Age'].min()}-{center_data['Age'].max()} years\n")
            f.write(f"  Mean Age: {center_data['Age'].mean():.1f} ± {center_data['Age'].std():.1f} years\n")
            f.write("\n")
    
    print(f"\nSummary report saved: {summary_file}")

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'medical_center_graphs'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, center_counts = load_and_analyze_data('521.xlsx')
        
        print(f"\n{'='*60}")
        print("Generating individual age distribution graphs for each medical center...")
        print(f"{'='*60}")
        
        # Create individual graphs for each medical center
        generated_files = []
        for center, total_patients in center_counts.items():
            center_data = df[df['Medical center'] == center]
            output_file = create_medical_center_graph(center_data, center, total_patients, output_dir)
            generated_files.append(output_file)
        
        # Create summary report
        create_summary_report(df, center_counts, output_dir)
        
        print(f"\n{'='*60}")
        print("All graphs generated successfully!")
        print(f"Total files created: {len(generated_files)}")
        print(f"Output directory: {output_dir}/")
        print("Files created:")
        for file in generated_files:
            print(f"  - {os.path.basename(file)}")
        print(f"{'='*60}")
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()