#!/usr/bin/env python3
"""
Age Distribution Analysis for Patient Data
Creates a histogram showing age limits vs number of patients for journal publication
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def load_and_analyze_data(filename):
    """Load Excel data and analyze age distribution"""
    df = pd.read_excel(filename)
    print(f"Dataset loaded: {df.shape[0]} patients")
    print(f"Age range: {df['Age'].min()} - {df['Age'].max()} years")
    print(f"Mean age: {df['Age'].mean():.1f} ± {df['Age'].std():.1f} years")
    return df

def create_age_bins(ages):
    """Create age bins similar to the reference image"""
    # Based on the reference image, create bins: 0-10, 11-20, 21-30, 31-40, etc.
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    bin_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    
    # Count patients in each age group
    age_counts, _ = np.histogram(ages, bins=bins)
    
    return bins, bin_labels, age_counts

def create_publication_graph(ages, output_filename='age_distribution_journal.png'):
    """Create a publication-ready graph of age vs number of patients"""
    
    # Set up the style for publication
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Create age bins
    bins, bin_labels, age_counts = create_age_bins(ages)
    
    # Create the bar chart
    x_positions = range(len(bin_labels))
    bars = ax.bar(x_positions, age_counts, 
                  color='lightblue', 
                  edgecolor='black', 
                  linewidth=1.2,
                  alpha=0.8)
    
    # Customize the plot for journal publication
    ax.set_xlabel('Age Limit (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Patients', fontsize=14, fontweight='bold')
    ax.set_title('Age Distribution of Patients', fontsize=16, fontweight='bold', pad=20)
    
    # Set x-axis labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bin_labels, fontsize=12)
    
    # Customize y-axis
    ax.set_ylim(0, max(age_counts) * 1.1)
    ax.tick_params(axis='y', labelsize=12)
    
    # Add value labels on top of bars
    for i, (bar, count) in enumerate(zip(bars, age_counts)):
        if count > 0:  # Only show labels for non-zero counts
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   str(count), ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"Graph saved as: {output_filename}")
    
    # Display statistics
    print("\nAge Distribution Summary:")
    for label, count in zip(bin_labels, age_counts):
        if count > 0:
            print(f"{label} years: {count} patients")
    
    return fig, ax

def main():
    """Main function to run the analysis"""
    try:
        # Load data
        df = load_and_analyze_data('521.xlsx')
        
        # Create the publication graph
        fig, ax = create_publication_graph(df['Age'])
        
        # Show the plot
        plt.show()
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()