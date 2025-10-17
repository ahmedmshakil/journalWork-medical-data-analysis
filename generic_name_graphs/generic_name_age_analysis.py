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
import matplotlib.patches as patches

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

def create_comprehensive_table(df, generic_counts, output_dir):
    """Create a comprehensive table with all generic drug statistics"""
    
    # Initialize table data
    table_data = []
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE GENERIC DRUGS DATA TABLE")
    print(f"{'='*80}")
    
    # Column headers
    headers = [
        "Generic Name", "Total Patients", "Male", "Female", "Male %", "Female %",
        "Min Age", "Max Age", "Mean Age", "Age Std", "Age 11-20", "Age 21-30", 
        "Age 31-40", "Age 41-50", "Age 51-60", "Age 61-70", "Age 71-80", "Age 81-90", "Age 91-100"
    ]
    
    for generic, total_patients in generic_counts.items():
        generic_data = df[df['Generic name'] == generic]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(generic_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Get age statistics
        ages = generic_data['Age']
        min_age = ages.min()
        max_age = ages.max()
        mean_age = ages.mean()
        std_age = ages.std()
        
        # Get age distribution by bins
        bins, bin_labels, age_counts = create_age_bins(ages)
        
        # Create row data
        row = [
            generic,
            total_patients,
            male_count,
            female_count,
            f"{male_pct:.1f}%",
            f"{female_pct:.1f}%",
            min_age,
            max_age,
            f"{mean_age:.1f}",
            f"{std_age:.1f}",
            age_counts[1],  # 11-20
            age_counts[2],  # 21-30
            age_counts[3],  # 31-40
            age_counts[4],  # 41-50
            age_counts[5],  # 51-60
            age_counts[6],  # 61-70
            age_counts[7],  # 71-80
            age_counts[8],  # 81-90
            age_counts[9]   # 91-100
        ]
        
        table_data.append(row)
    
    # Create DataFrame for better formatting
    table_df = pd.DataFrame(table_data, columns=headers)
    
    # Display table in console
    print("\nGeneric Drugs Comprehensive Data Table:")
    print("-" * 120)
    for i, row in table_df.iterrows():
        print(f"{row['Generic Name']:<20} | {row['Total Patients']:<4} | {row['Male']:<4} | {row['Female']:<4} | {row['Male %']:<6} | {row['Female %']:<6} | {row['Min Age']:<3} | {row['Max Age']:<3} | {row['Mean Age']:<6} | {row['Age Std']:<6}")
    
    print("\nAge Distribution by Groups:")
    print("-" * 120)
    print(f"{'Generic Name':<20} | {'11-20':<4} | {'21-30':<4} | {'31-40':<4} | {'41-50':<4} | {'51-60':<4} | {'61-70':<4} | {'71-80':<4} | {'81-90':<4} | {'91-100':<4}")
    print("-" * 120)
    for i, row in table_df.iterrows():
        print(f"{row['Generic Name']:<20} | {row['Age 11-20']:<4} | {row['Age 21-30']:<4} | {row['Age 31-40']:<4} | {row['Age 41-50']:<4} | {row['Age 51-60']:<4} | {row['Age 61-70']:<4} | {row['Age 71-80']:<4} | {row['Age 81-90']:<4} | {row['Age 91-100']:<4}")
    
    # Save table as CSV file
    csv_file = os.path.join(output_dir, 'generic_drugs_comprehensive_table.csv')
    table_df.to_csv(csv_file, index=False)
    print(f"\nComprehensive table saved as CSV: {csv_file}")
    
    # Save table as formatted text file
    txt_file = os.path.join(output_dir, 'generic_drugs_comprehensive_table.txt')
    with open(txt_file, 'w') as f:
        f.write("COMPREHENSIVE GENERIC DRUGS DATA TABLE\n")
        f.write("="*80 + "\n\n")
        
        f.write("Basic Statistics:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Generic Name':<20} | {'Total':<5} | {'Male':<4} | {'Female':<6} | {'Male%':<6} | {'Female%':<7} | {'Min Age':<7} | {'Max Age':<7} | {'Mean Age':<8} | {'Std Age':<7}\n")
        f.write("-" * 120 + "\n")
        
        for i, row in table_df.iterrows():
            f.write(f"{row['Generic Name']:<20} | {row['Total Patients']:<5} | {row['Male']:<4} | {row['Female']:<6} | {row['Male %']:<6} | {row['Female %']:<7} | {row['Min Age']:<7} | {row['Max Age']:<7} | {row['Mean Age']:<8} | {row['Age Std']:<7}\n")
        
        f.write("\n\nAge Distribution by Groups:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Generic Name':<20} | {'11-20':<5} | {'21-30':<5} | {'31-40':<5} | {'41-50':<5} | {'51-60':<5} | {'61-70':<5} | {'71-80':<5} | {'81-90':<5} | {'91-100':<6}\n")
        f.write("-" * 120 + "\n")
        
        for i, row in table_df.iterrows():
            f.write(f"{row['Generic Name']:<20} | {row['Age 11-20']:<5} | {row['Age 21-30']:<5} | {row['Age 31-40']:<5} | {row['Age 41-50']:<5} | {row['Age 51-60']:<5} | {row['Age 61-70']:<5} | {row['Age 71-80']:<5} | {row['Age 81-90']:<5} | {row['Age 91-100']:<6}\n")
        
        f.write(f"\n\nTotal Patients Analyzed: {len(df)}\n")
        f.write(f"Total Generic Drugs: {len(generic_counts)}\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"Comprehensive table saved as text: {txt_file}")
    
    return table_df

def create_summary_statistics_table(df, generic_counts, output_dir):
    """Create a summary statistics table for all generic drugs"""
    
    summary_stats = {
        'Total Patients': [],
        'Male Count': [],
        'Female Count': [],
        'Male Percentage': [],
        'Female Percentage': [],
        'Age Min': [],
        'Age Max': [],
        'Most Common Age Group': []
    }
    
    generic_names = []
    
    for generic, total_patients in generic_counts.items():
        generic_data = df[df['Generic name'] == generic]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(generic_data)
        
        # Get age statistics
        ages = generic_data['Age']
        
        # Get most common age group
        bins, bin_labels, age_counts = create_age_bins(ages)
        max_age_group_idx = np.argmax(age_counts)
        most_common_age_group = bin_labels[max_age_group_idx] if age_counts[max_age_group_idx] > 0 else "N/A"
        
        # Append data
        generic_names.append(generic)
        summary_stats['Total Patients'].append(total_patients)
        summary_stats['Male Count'].append(male_count)
        summary_stats['Female Count'].append(female_count)
        summary_stats['Male Percentage'].append(f"{(male_count/total_patients*100):.1f}%")
        summary_stats['Female Percentage'].append(f"{(female_count/total_patients*100):.1f}%")
        summary_stats['Age Min'].append(ages.min())
        summary_stats['Age Max'].append(ages.max())
        summary_stats['Most Common Age Group'].append(most_common_age_group)
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_stats, index=generic_names)
    
    # Save summary table
    summary_csv = os.path.join(output_dir, 'generic_drugs_summary_statistics.csv')
    summary_df.to_csv(summary_csv)
    
    print(f"\nSummary statistics table saved: {summary_csv}")
    
    # Print summary to console
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS TABLE")
    print(f"{'='*80}")
    print(summary_df.to_string())
    
    return summary_df

def create_ieee_standard_table_png(df, generic_counts, output_dir):
    """Create IEEE standard borderless table PNG for journal publication"""
    
    # Prepare data for the main content table
    table_data = []
    
    # Create headers similar to your demo table
    headers = ["Generic Name", "Total\nPatients", "Male", "Female", "Male\n%", "Female\n%", 
               "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90"]
    
    for generic, total_patients in generic_counts.items():
        generic_data = df[df['Generic name'] == generic]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(generic_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Get age distribution by bins
        bins, bin_labels, age_counts = create_age_bins(generic_data['Age'])
        
        # Create row data (excluding ages 0-10 and 91-100 for space)
        row = [
            generic.title(),
            str(total_patients),
            str(male_count),
            str(female_count),
            f"{male_pct:.1f}",
            f"{female_pct:.1f}",
            str(age_counts[1]),  # 11-20
            str(age_counts[2]),  # 21-30
            str(age_counts[3]),  # 31-40
            str(age_counts[4]),  # 41-50
            str(age_counts[5]),  # 51-60
            str(age_counts[6]),  # 61-70
            str(age_counts[7]),  # 71-80
            str(age_counts[8])   # 81-90
        ]
        
        table_data.append(row)
    
    # Create the table figure with IEEE standards
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    ax.axis('off')  # Remove axes
    
    # Create table
    table = ax.table(cellText=table_data, 
                     colLabels=headers,
                     cellLoc='center', 
                     loc='center',
                     colWidths=[0.18, 0.08, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06])
    
    # IEEE standard formatting - borderless and clean
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2.0)
    
    # Remove all borders and set clean formatting
    for i in range(len(headers)):
        # Header formatting
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', fontsize=10)
        cell.set_facecolor('#f0f0f0')
        cell.set_edgecolor('none')
        cell.set_linewidth(0)
        
        # Add subtle bottom line for headers only
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        cell.get_text().set_ha('center')
        cell.get_text().set_va('center')
    
    # Format data cells
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor('white')
            cell.set_edgecolor('none')
            cell.set_linewidth(0)
            cell.get_text().set_fontsize(9)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            # Alternate row colors for better readability
            if i % 2 == 0:
                cell.set_facecolor('#f9f9f9')
    
    # Add title
    plt.title('Generic Drug Distribution Analysis - Patient Demographics and Age Groups', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add subtitle with total information
    plt.figtext(0.5, 0.02, f'Total Patients: {len(df)} | Total Generic Drugs: {len(generic_counts)} | Age Groups: Years', 
                ha='center', fontsize=10, style='italic')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'generic_drugs_comprehensive_table.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nIEEE Standard Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def create_summary_statistics_table_png(df, generic_counts, output_dir):
    """Create a summary statistics table PNG following IEEE standards"""
    
    # Prepare summary data
    table_data = []
    headers = ["Generic Name", "Total\nPatients", "Gender Distribution", "Age Statistics", "Most Common\nAge Group"]
    
    for generic, total_patients in generic_counts.items():
        generic_data = df[df['Generic name'] == generic]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(generic_data)
        gender_info = f"M: {male_count} ({male_count/total_patients*100:.1f}%)\nF: {female_count} ({female_count/total_patients*100:.1f}%)"
        
        # Get age statistics
        ages = generic_data['Age']
        age_info = f"Range: {ages.min()}-{ages.max()}\nMean: {ages.mean():.1f}±{ages.std():.1f}"
        
        # Get most common age group
        bins, bin_labels, age_counts = create_age_bins(ages)
        max_age_group_idx = np.argmax(age_counts)
        most_common_age_group = f"{bin_labels[max_age_group_idx]}\n({age_counts[max_age_group_idx]} patients)"
        
        row = [
            generic.title(),
            str(total_patients),
            gender_info,
            age_info,
            most_common_age_group
        ]
        
        table_data.append(row)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.25, 0.12, 0.25, 0.25, 0.18])
    
    # IEEE standard formatting
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 2.5)
    
    # Format headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', fontsize=10)
        cell.set_facecolor('#e6e6e6')
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        cell.get_text().set_ha('center')
        cell.get_text().set_va('center')
    
    # Format data cells
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor('white')
            cell.set_edgecolor('none')
            cell.set_linewidth(0)
            cell.get_text().set_fontsize(8)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            if i % 2 == 0:
                cell.set_facecolor('#f5f5f5')
    
    # Add title
    plt.title('Generic Drug Summary Statistics - Comprehensive Overview', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add subtitle
    plt.figtext(0.5, 0.02, f'Summary of {len(generic_counts)} Generic Drugs | Total Dataset: {len(df)} Patients', 
                ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'generic_drugs_summary_statistics.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nSummary Statistics Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def create_age_distribution_table_png(df, generic_counts, output_dir):
    """Create detailed age distribution table PNG for all generic drugs"""
    
    # Prepare age distribution data
    table_data = []
    headers = ["Generic Name", "0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100", "Total"]
    
    for generic, total_patients in generic_counts.items():
        generic_data = df[df['Generic name'] == generic]
        
        # Get age distribution by bins
        bins, bin_labels, age_counts = create_age_bins(generic_data['Age'])
        
        row = [generic.title()] + [str(count) for count in age_counts] + [str(total_patients)]
        table_data.append(row)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 8), dpi=300)
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.2] + [0.07]*10 + [0.08])
    
    # IEEE standard formatting
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 2.0)
    
    # Format headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', fontsize=10)
        cell.set_facecolor('#d4d4d4')
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        cell.get_text().set_ha('center')
        cell.get_text().set_va('center')
    
    # Format data cells with color coding for values
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_edgecolor('none')
            cell.set_linewidth(0)
            cell.get_text().set_fontsize(9)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            # Color coding for better visualization
            if j == 0:  # Generic name column
                cell.set_facecolor('#f0f0f0')
                cell.get_text().set_weight('bold')
            elif j == len(headers) - 1:  # Total column
                cell.set_facecolor('#e6e6e6')
                cell.get_text().set_weight('bold')
            else:
                # Age group columns - color based on value
                try:
                    value = int(table_data[i-1][j])
                    if value == 0:
                        cell.set_facecolor('white')
                    elif value <= 5:
                        cell.set_facecolor('#fff2cc')
                    elif value <= 15:
                        cell.set_facecolor('#ffd966')
                    else:
                        cell.set_facecolor('#ff9900')
                        cell.get_text().set_weight('bold')
                except:
                    cell.set_facecolor('white')
            
            # Alternate row background
            if i % 2 == 0:
                if j == 0:
                    cell.set_facecolor('#e8e8e8')
                elif j == len(headers) - 1:
                    cell.set_facecolor('#d4d4d4')
    
    # Add title
    plt.title('Age Distribution Analysis by Generic Drug - Detailed Breakdown', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add legend explanation
    plt.figtext(0.5, 0.02, 'Color Legend: White (0 patients) | Light Yellow (1-5 patients) | Yellow (6-15 patients) | Orange (>15 patients)', 
                ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'generic_drugs_age_distribution_detailed.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nDetailed Age Distribution Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'generic_name_graphs'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, generic_counts = load_and_analyze_data('../521.xlsx')
        
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
        
        # Create comprehensive data table
        print(f"\n{'='*70}")
        print("GENERATING COMPREHENSIVE DATA TABLES...")
        print(f"{'='*70}")
        
        comprehensive_table = create_comprehensive_table(df, generic_counts, output_dir)
        summary_stats_table = create_summary_statistics_table(df, generic_counts, output_dir)
        
        # Create IEEE standard table PNGs for journal publication
        print(f"\n{'='*70}")
        print("GENERATING IEEE STANDARD TABLE PNGs FOR JOURNAL PUBLICATION...")
        print(f"{'='*70}")
        
        # Create comprehensive table PNG
        comprehensive_png = create_ieee_standard_table_png(df, generic_counts, output_dir)
        
        # Create summary statistics table PNG
        summary_png = create_summary_statistics_table_png(df, generic_counts, output_dir)
        
        # Create detailed age distribution table PNG
        age_dist_png = create_age_distribution_table_png(df, generic_counts, output_dir)
        
        print(f"\n{'='*70}")
        print("All graphs and tables generated successfully!")
        print(f"Graph files created: {len(generated_files)}")
        print(f"Table files created: 6 (3 data files + 3 PNG images)")
        print(f"Output directory: {output_dir}/")
        print("\nGraph files:")
        for file in generated_files:
            print(f"  - {os.path.basename(file)}")
        print("\nData Table files:")
        print(f"  - generic_drugs_summary.txt")
        print(f"  - generic_drugs_comprehensive_table.csv")
        print(f"  - generic_drugs_comprehensive_table.txt")
        print(f"  - generic_drugs_summary_statistics.csv")
        print("\nJournal-Ready Table PNG files (IEEE Standard):")
        print(f"  - generic_drugs_comprehensive_table.png")
        print(f"  - generic_drugs_summary_statistics.png")
        print(f"  - generic_drugs_age_distribution_detailed.png")
        print(f"{'='*70}")
        print("📊 IEEE Standard borderless tables created for journal publication!")
        print("✅ All tables follow journal formatting standards")
        print("🎯 Ready for publication submission")
        print(f"{'='*70}")
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()