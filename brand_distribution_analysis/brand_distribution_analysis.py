#!/usr/bin/env python3
"""
Brand Distribution Analysis
Creates comprehensive brand distribution tables and analysis for journal publication
Analyzes top 30 brands from 521.xlsx dataset
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

def load_and_analyze_data(filename):
    """Load Excel data and analyze brand distribution"""
    df = pd.read_excel(filename)
    print(f"Dataset loaded: {df.shape[0]} patients")
    
    # Get top 30 brand information
    brand_counts = df['Brand name'].value_counts().sort_values(ascending=False).head(30)
    print(f"\nTop 30 Brands:")
    for i, (brand, count) in enumerate(brand_counts.items(), 1):
        print(f"  {i:2d}. {brand}: {count} patients")
    
    return df, brand_counts

def get_gender_distribution(brand_data):
    """Get male/female distribution for the brand"""
    gender_counts = brand_data['Gender'].value_counts()
    male_count = gender_counts.get('Male', 0) + gender_counts.get('male', 0) + gender_counts.get('M', 0)
    female_count = gender_counts.get('Female', 0) + gender_counts.get('female', 0) + gender_counts.get('F', 0)
    
    return male_count, female_count

def get_age_statistics(brand_data):
    """Get age statistics for the brand"""
    ages = brand_data['Age']
    return {
        'min': ages.min(),
        'max': ages.max(),
        'mean': ages.mean(),
        'median': ages.median(),
        'std': ages.std()
    }

def get_top_symptoms(brand_data, top_n=3):
    """Get top symptoms for the brand"""
    symptom_counts = brand_data['Symptoms'].value_counts()
    return symptom_counts.head(top_n)

def create_comprehensive_brand_table(df, brand_counts, output_dir):
    """Create a comprehensive table with all brand statistics"""
    
    # Initialize table data
    table_data = []
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE BRAND DISTRIBUTION DATA TABLE")
    print(f"{'='*80}")
    
    # Column headers
    headers = [
        "Rank", "Brand Name", "Total Patients", "Percentage", "Male", "Female", 
        "Male %", "Female %", "Age Mean", "Age Range", "Top Symptom", "Top Symptom Count"
    ]
    
    for rank, (brand, total_patients) in enumerate(brand_counts.items(), 1):
        brand_data = df[df['Brand name'] == brand]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(brand_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Get age statistics
        age_stats = get_age_statistics(brand_data)
        
        # Get top symptom
        top_symptoms = get_top_symptoms(brand_data, 1)
        top_symptom = top_symptoms.index[0] if len(top_symptoms) > 0 else "N/A"
        top_symptom_count = top_symptoms.iloc[0] if len(top_symptoms) > 0 else 0
        
        # Calculate percentage of total dataset
        dataset_percentage = (total_patients / len(df) * 100)
        
        # Create row data
        row = [
            rank,
            brand,
            total_patients,
            f"{dataset_percentage:.1f}%",
            male_count,
            female_count,
            f"{male_pct:.1f}%",
            f"{female_pct:.1f}%",
            f"{age_stats['mean']:.1f}",
            f"{age_stats['min']}-{age_stats['max']}",
            top_symptom,
            top_symptom_count
        ]
        
        table_data.append(row)
    
    # Create DataFrame for better formatting
    table_df = pd.DataFrame(table_data, columns=headers)
    
    # Display table in console
    print("\nTop 30 Brand Distribution Table:")
    print("-" * 150)
    for i, row in table_df.iterrows():
        print(f"{row['Rank']:<3} | {row['Brand Name']:<20} | {row['Total Patients']:<4} | {row['Percentage']:<6} | {row['Male']:<4} | {row['Female']:<4} | {row['Male %']:<6} | {row['Female %']:<6}")
    
    # Save table as CSV file
    csv_file = os.path.join(output_dir, 'brand_distribution_top30_table.csv')
    table_df.to_csv(csv_file, index=False)
    print(f"\nComprehensive table saved as CSV: {csv_file}")
    
    # Save table as formatted text file
    txt_file = os.path.join(output_dir, 'brand_distribution_top30_table.txt')
    with open(txt_file, 'w') as f:
        f.write("TOP 30 BRAND DISTRIBUTION DATA TABLE\n")
        f.write("="*80 + "\n\n")
        
        f.write("Brand Statistics:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<4} | {'Brand Name':<20} | {'Total':<5} | {'%':<6} | {'Male':<4} | {'Female':<6} | {'M%':<6} | {'F%':<6} | {'Age Mean':<8} | {'Age Range':<10} | {'Top Symptom':<20}\n")
        f.write("-" * 150 + "\n")
        
        for i, row in table_df.iterrows():
            f.write(f"{row['Rank']:<4} | {row['Brand Name']:<20} | {row['Total Patients']:<5} | {row['Percentage']:<6} | {row['Male']:<4} | {row['Female']:<6} | {row['Male %']:<6} | {row['Female %']:<6} | {row['Age Mean']:<8} | {row['Age Range']:<10} | {row['Top Symptom']:<20}\n")
        
        f.write(f"\n\nTotal Patients Analyzed: {len(df)}\n")
        f.write(f"Total Brands: {len(df['Brand name'].unique())}\n")
        f.write(f"Top 30 Brands Coverage: {brand_counts.sum()} patients ({brand_counts.sum()/len(df)*100:.1f}%)\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"Comprehensive table saved as text: {txt_file}")
    
    return table_df

def create_brand_summary_statistics(df, brand_counts, output_dir):
    """Create summary statistics for top 30 brands"""
    
    summary_stats = {
        'Total Patients': [],
        'Dataset Percentage': [],
        'Male Count': [],
        'Female Count': [],
        'Gender Ratio (F:M)': [],
        'Age Mean': [],
        'Age Std': [],
        'Age Range': [],
        'Unique Symptoms': [],
        'Top Symptom': []
    }
    
    brand_names = []
    
    for brand, total_patients in brand_counts.items():
        brand_data = df[df['Brand name'] == brand]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(brand_data)
        
        # Calculate gender ratio
        if male_count > 0:
            gender_ratio = f"{female_count/male_count:.1f}:1"
        else:
            gender_ratio = "All F" if female_count > 0 else "N/A"
        
        # Get age statistics
        age_stats = get_age_statistics(brand_data)
        
        # Get symptom information
        unique_symptoms = len(brand_data['Symptoms'].unique())
        top_symptoms = get_top_symptoms(brand_data, 1)
        top_symptom = top_symptoms.index[0] if len(top_symptoms) > 0 else "N/A"
        
        # Calculate dataset percentage
        dataset_percentage = (total_patients / len(df) * 100)
        
        # Append data
        brand_names.append(brand)
        summary_stats['Total Patients'].append(total_patients)
        summary_stats['Dataset Percentage'].append(f"{dataset_percentage:.1f}%")
        summary_stats['Male Count'].append(male_count)
        summary_stats['Female Count'].append(female_count)
        summary_stats['Gender Ratio (F:M)'].append(gender_ratio)
        summary_stats['Age Mean'].append(f"{age_stats['mean']:.1f}")
        summary_stats['Age Std'].append(f"{age_stats['std']:.1f}")
        summary_stats['Age Range'].append(f"{age_stats['min']}-{age_stats['max']}")
        summary_stats['Unique Symptoms'].append(unique_symptoms)
        summary_stats['Top Symptom'].append(top_symptom)
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_stats, index=brand_names)
    
    # Save summary table
    summary_csv = os.path.join(output_dir, 'brand_summary_statistics_top30.csv')
    summary_df.to_csv(summary_csv)
    
    print(f"\nSummary statistics table saved: {summary_csv}")
    
    return summary_df

def create_ieee_standard_brand_table_png(df, brand_counts, output_dir):
    """Create IEEE standard borderless table PNG for journal publication"""
    
    # Prepare data for the main content table (first 15 brands for better readability)
    table_data = []
    
    # Create headers
    headers = ["Rank", "Brand Name", "Total\nPatients", "Dataset\n%", "Male", "Female", 
               "Male\n%", "Female\n%", "Top Symptom"]
    
    for rank, (brand, total_patients) in enumerate(list(brand_counts.items())[:15], 1):
        brand_data = df[df['Brand name'] == brand]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(brand_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Get age statistics
        age_stats = get_age_statistics(brand_data)
        
        # Get top symptom
        top_symptoms = get_top_symptoms(brand_data, 1)
        top_symptom = top_symptoms.index[0] if len(top_symptoms) > 0 else "N/A"
        
        # Calculate percentage of total dataset
        dataset_percentage = (total_patients / len(df) * 100)
        
        # Truncate long names for display
        display_brand = brand[:15] + "..." if len(brand) > 18 else brand
        display_symptom = top_symptom  # Use full symptom name without truncation
        
        # Create row data
        row = [
            str(rank),
            display_brand,
            str(total_patients),
            f"{dataset_percentage:.1f}",
            str(male_count),
            str(female_count),
            f"{male_pct:.1f}",
            f"{female_pct:.1f}",
            display_symptom
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
                     colWidths=[0.08, 0.16, 0.08, 0.06, 0.06, 0.06, 0.06, 0.06, 0.32])
    
    # IEEE standard formatting - borderless and clean
    table.auto_set_font_size(False)
    table.set_fontsize(9)
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
            cell.get_text().set_fontsize(8)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            # Alternate row colors for better readability
            if i % 2 == 0:
                cell.set_facecolor('#f9f9f9')
    
    # Add title
    plt.title('Brand Distribution Analysis - Top 15 Brands (Patient Demographics)', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add subtitle with total information
    plt.figtext(0.5, 0.02, f'Total Patients: {len(df)} | Total Brands: {len(df["Brand name"].unique())} | Top 15 of 30 Analyzed', 
                ha='center', fontsize=10, style='italic')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'brand_distribution_top15_table.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nIEEE Standard Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def create_full_brand_table_png(df, brand_counts, output_dir):
    """Create full brand table PNG with all 30 brands in one table"""
    
    # Create single table with all 30 brands
    table_data = []
    headers = ["Rank", "Brand Name", "Patients", "%", "Male", "Female", "Top Symptom"]
    
    for rank, (brand, total_patients) in enumerate(brand_counts.items(), 1):
        brand_data = df[df['Brand name'] == brand]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(brand_data)
        
        # Get top symptom
        top_symptoms = get_top_symptoms(brand_data, 1)
        top_symptom = top_symptoms.index[0] if len(top_symptoms) > 0 else "N/A"
        
        # Calculate percentage of total dataset
        dataset_percentage = (total_patients / len(df) * 100)
        
        # Truncate long names for display
        display_brand = brand[:15] + "..." if len(brand) > 18 else brand
        display_symptom = top_symptom  # Use full symptom name without truncation
        
        row = [
            str(rank),
            display_brand,
            str(total_patients),
            f"{dataset_percentage:.1f}",
            str(male_count),
            str(female_count),
            display_symptom
        ]
        
        table_data.append(row)
    
    # Create single figure with all 30 brands
    fig, ax = plt.subplots(figsize=(16, 20), dpi=300)
    ax.axis('off')
    
    # Create table with all 30 brands
    table = ax.table(cellText=table_data, 
                     colLabels=headers,
                     cellLoc='center', 
                     loc='center',
                     colWidths=[0.08, 0.20, 0.10, 0.06, 0.08, 0.08, 0.40])
    
    # Format table
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.5)
    
    # Format headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', fontsize=10)
        cell.set_facecolor('#e0e0e0')
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
            cell.get_text().set_fontsize(7)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            # Alternate row colors for better readability
            if i % 2 == 0:
                cell.set_facecolor('#f5f5f5')
    
    # Add main title
    plt.title('Complete Brand Distribution Analysis - Top 30 Brands', 
              fontsize=16, fontweight='bold', pad=30)
    
    # Add subtitle
    plt.figtext(0.5, 0.02, f'Total Patients: {len(df)} | Total Brands: {len(df["Brand name"].unique())} | Coverage: {brand_counts.sum()}/{len(df)} patients ({brand_counts.sum()/len(df)*100:.1f}%)', 
                ha='center', fontsize=11, style='italic')
    
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'brand_distribution_complete_top30_table.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nComplete Top 30 Brands Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'brand_distribution_analysis'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, brand_counts = load_and_analyze_data('../521.xlsx')
        
        print(f"\n{'='*70}")
        print("GENERATING COMPREHENSIVE BRAND DISTRIBUTION TABLES...")
        print(f"{'='*70}")
        
        # Create comprehensive data table
        comprehensive_table = create_comprehensive_brand_table(df, brand_counts, output_dir)
        summary_stats_table = create_brand_summary_statistics(df, brand_counts, output_dir)
        
        # Create IEEE standard table PNGs for journal publication
        print(f"\n{'='*70}")
        print("GENERATING IEEE STANDARD TABLE PNGs FOR JOURNAL PUBLICATION...")
        print(f"{'='*70}")
        
        # Create top 15 brands table PNG
        top15_png = create_ieee_standard_brand_table_png(df, brand_counts, output_dir)
        
        # Create complete top 30 brands table PNG
        complete_png = create_full_brand_table_png(df, brand_counts, output_dir)
        
        print(f"\n{'='*70}")
        print("All brand distribution tables generated successfully!")
        print(f"Table files created: 4 (2 data files + 2 PNG images)")
        print(f"Output directory: {output_dir}/")
        print("\nData Table files:")
        print(f"  - brand_distribution_top30_table.csv")
        print(f"  - brand_distribution_top30_table.txt")
        print(f"  - brand_summary_statistics_top30.csv")
        print("\nJournal-Ready Table PNG files (IEEE Standard):")
        print(f"  - brand_distribution_top15_table.png")
        print(f"  - brand_distribution_complete_top30_table.png")
        print(f"{'='*70}")
        print("📊 IEEE Standard borderless tables created for journal publication!")
        print("✅ All tables follow journal formatting standards")
        print("🎯 Ready for publication submission")
        
        # Print summary statistics
        print(f"\n{'='*70}")
        print("ANALYSIS SUMMARY:")
        print(f"Total patients: {len(df)}")
        print(f"Total unique brands: {len(df['Brand name'].unique())}")
        print(f"Top 30 brands coverage: {brand_counts.sum()} patients ({brand_counts.sum()/len(df)*100:.1f}%)")
        print(f"Remaining brands: {len(df) - brand_counts.sum()} patients ({(len(df) - brand_counts.sum())/len(df)*100:.1f}%)")
        print(f"{'='*70}")
        
    except FileNotFoundError:
        print("Error: 521.xlsx file not found. Please ensure the file is in the current directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()