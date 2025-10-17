#!/usr/bin/env python3
"""
Symptom-Brand Table Analysis
Creates comprehensive tables for symptom-brand distribution analysis for journal publication
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

def get_gender_distribution(symptom_data):
    """Get male/female distribution for the symptom"""
    gender_counts = symptom_data['Gender'].value_counts()
    male_count = gender_counts.get('Male', 0) + gender_counts.get('male', 0) + gender_counts.get('M', 0)
    female_count = gender_counts.get('Female', 0) + gender_counts.get('female', 0) + gender_counts.get('F', 0)
    
    return male_count, female_count

def create_comprehensive_symptom_table(df, symptoms_counts, output_dir):
    """Create a comprehensive table with all symptom statistics"""
    
    # Initialize table data
    table_data = []
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE SYMPTOM-BRAND DATA TABLE")
    print(f"{'='*80}")
    
    # Column headers
    headers = [
        "Symptom", "Total Patients", "Male", "Female", "Male %", "Female %",
        "Unique Brands", "Top Brand", "Top Brand Count", "Top Brand %", 
        "2nd Brand", "2nd Brand Count", "3rd Brand", "3rd Brand Count"
    ]
    
    for symptom, total_patients in symptoms_counts.items():
        symptom_data = df[df['Symptoms'] == symptom]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(symptom_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Get brand distribution
        brand_counts = get_brand_distribution(symptom_data)
        unique_brands = len(brand_counts)
        
        # Get top 3 brands
        top_brand = brand_counts.index[0] if len(brand_counts) > 0 else "N/A"
        top_brand_count = brand_counts.iloc[0] if len(brand_counts) > 0 else 0
        top_brand_pct = (top_brand_count / total_patients * 100) if total_patients > 0 else 0
        
        second_brand = brand_counts.index[1] if len(brand_counts) > 1 else "N/A"
        second_brand_count = brand_counts.iloc[1] if len(brand_counts) > 1 else 0
        
        third_brand = brand_counts.index[2] if len(brand_counts) > 2 else "N/A"
        third_brand_count = brand_counts.iloc[2] if len(brand_counts) > 2 else 0
        
        # Create row data
        row = [
            symptom,
            total_patients,
            male_count,
            female_count,
            f"{male_pct:.1f}%",
            f"{female_pct:.1f}%",
            unique_brands,
            top_brand,
            top_brand_count,
            f"{top_brand_pct:.1f}%",
            second_brand,
            second_brand_count,
            third_brand,
            third_brand_count
        ]
        
        table_data.append(row)
    
    # Create DataFrame for better formatting
    table_df = pd.DataFrame(table_data, columns=headers)
    
    # Display table in console
    print("\nSymptom-Brand Comprehensive Data Table:")
    print("-" * 150)
    for i, row in table_df.iterrows():
        print(f"{row['Symptom']:<25} | {row['Total Patients']:<4} | {row['Male']:<4} | {row['Female']:<4} | {row['Male %']:<6} | {row['Female %']:<6} | {row['Unique Brands']:<4} | {row['Top Brand']:<20} | {row['Top Brand Count']:<4}")
    
    # Save table as CSV file
    csv_file = os.path.join(output_dir, 'symptom_brand_comprehensive_table.csv')
    table_df.to_csv(csv_file, index=False)
    print(f"\nComprehensive table saved as CSV: {csv_file}")
    
    # Save table as formatted text file
    txt_file = os.path.join(output_dir, 'symptom_brand_comprehensive_table.txt')
    with open(txt_file, 'w') as f:
        f.write("COMPREHENSIVE SYMPTOM-BRAND DATA TABLE\n")
        f.write("="*80 + "\n\n")
        
        f.write("Basic Statistics:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Symptom':<25} | {'Total':<5} | {'Male':<4} | {'Female':<6} | {'Male%':<6} | {'Female%':<7} | {'Brands':<6} | {'Top Brand':<20} | {'Count':<5}\n")
        f.write("-" * 150 + "\n")
        
        for i, row in table_df.iterrows():
            f.write(f"{row['Symptom']:<25} | {row['Total Patients']:<5} | {row['Male']:<4} | {row['Female']:<6} | {row['Male %']:<6} | {row['Female %']:<7} | {row['Unique Brands']:<6} | {row['Top Brand']:<20} | {row['Top Brand Count']:<5}\n")
        
        f.write(f"\n\nTotal Patients Analyzed: {len(df)}\n")
        f.write(f"Total Symptoms Analyzed: {len(symptoms_counts)}\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"Comprehensive table saved as text: {txt_file}")
    
    return table_df

def create_symptom_summary_statistics_table(df, symptoms_counts, output_dir):
    """Create a summary statistics table for all symptoms"""
    
    summary_stats = {
        'Total Patients': [],
        'Male Count': [],
        'Female Count': [],
        'Male Percentage': [],
        'Female Percentage': [],
        'Unique Brands': [],
        'Top Brand': [],
        'Brand Diversity Index': []
    }
    
    symptom_names = []
    
    for symptom, total_patients in symptoms_counts.items():
        symptom_data = df[df['Symptoms'] == symptom]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(symptom_data)
        
        # Get brand distribution
        brand_counts = get_brand_distribution(symptom_data)
        unique_brands = len(brand_counts)
        top_brand = brand_counts.index[0] if len(brand_counts) > 0 else "N/A"
        
        # Calculate brand diversity index (normalized entropy)
        brand_diversity = 0
        if unique_brands > 1:
            proportions = brand_counts.values / total_patients
            brand_diversity = -sum(p * np.log2(p) for p in proportions if p > 0) / np.log2(unique_brands)
        
        # Append data
        symptom_names.append(symptom)
        summary_stats['Total Patients'].append(total_patients)
        summary_stats['Male Count'].append(male_count)
        summary_stats['Female Count'].append(female_count)
        summary_stats['Male Percentage'].append(f"{(male_count/total_patients*100):.1f}%")
        summary_stats['Female Percentage'].append(f"{(female_count/total_patients*100):.1f}%")
        summary_stats['Unique Brands'].append(unique_brands)
        summary_stats['Top Brand'].append(top_brand)
        summary_stats['Brand Diversity Index'].append(f"{brand_diversity:.3f}")
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_stats, index=symptom_names)
    
    # Save summary table
    summary_csv = os.path.join(output_dir, 'symptom_brand_summary_statistics.csv')
    summary_df.to_csv(summary_csv)
    
    print(f"\nSummary statistics table saved: {summary_csv}")
    
    # Print summary to console
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS TABLE")
    print(f"{'='*80}")
    print(summary_df.to_string())
    
    return summary_df

def create_ieee_standard_symptom_table_png(df, symptoms_counts, output_dir):
    """Create IEEE standard borderless table PNG for journal publication"""
    
    # Prepare data for the main content table
    table_data = []
    
    # Create headers
    headers = ["Symptom", "Total\nPatients", "Male", "Female", "Male\n%", "Female\n%", 
               "Unique\nBrands", "Top Brand", "Top Brand\nCount", "Top Brand\n%"]
    
    for symptom, total_patients in symptoms_counts.items():
        symptom_data = df[df['Symptoms'] == symptom]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(symptom_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Get brand distribution
        brand_counts = get_brand_distribution(symptom_data)
        unique_brands = len(brand_counts)
        top_brand = brand_counts.index[0] if len(brand_counts) > 0 else "N/A"
        top_brand_count = brand_counts.iloc[0] if len(brand_counts) > 0 else 0
        top_brand_pct = (top_brand_count / total_patients * 100) if total_patients > 0 else 0
        
        # Truncate long symptom names
        display_symptom = symptom[:20] + "..." if len(symptom) > 23 else symptom
        display_brand = top_brand[:15] + "..." if len(top_brand) > 18 else top_brand
        
        # Create row data
        row = [
            display_symptom,
            str(total_patients),
            str(male_count),
            str(female_count),
            f"{male_pct:.1f}",
            f"{female_pct:.1f}",
            str(unique_brands),
            display_brand,
            str(top_brand_count),
            f"{top_brand_pct:.1f}"
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
                     colWidths=[0.18, 0.08, 0.06, 0.06, 0.06, 0.06, 0.08, 0.16, 0.08, 0.08])
    
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
    plt.title('Symptom-Brand Distribution Analysis - Patient Demographics and Brand Preferences', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add subtitle with total information
    plt.figtext(0.5, 0.02, f'Total Patients: {len(df)} | Total Symptoms Analyzed: {len(symptoms_counts)} | Top 15 Symptoms', 
                ha='center', fontsize=10, style='italic')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'symptom_brand_comprehensive_table.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nIEEE Standard Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def create_brand_frequency_table_png(df, symptoms_counts, output_dir):
    """Create brand frequency table PNG for symptoms"""
    
    # Prepare brand frequency data
    table_data = []
    headers = ["Symptom", "1st Brand (Count)", "2nd Brand (Count)", "3rd Brand (Count)", "4th Brand (Count)", "5th Brand (Count)", "Others"]
    
    for symptom, total_patients in symptoms_counts.items():
        symptom_data = df[df['Symptoms'] == symptom]
        brand_counts = get_brand_distribution(symptom_data)
        
        # Get top 5 brands
        brands_info = []
        for i in range(5):
            if i < len(brand_counts):
                brand_name = brand_counts.index[i][:12] + "..." if len(brand_counts.index[i]) > 15 else brand_counts.index[i]
                brands_info.append(f"{brand_name} ({brand_counts.iloc[i]})")
            else:
                brands_info.append("N/A")
        
        # Calculate others
        others_count = sum(brand_counts.iloc[5:]) if len(brand_counts) > 5 else 0
        others_info = f"{others_count} patients" if others_count > 0 else "N/A"
        
        # Truncate symptom name
        display_symptom = symptom[:18] + "..." if len(symptom) > 21 else symptom
        
        row = [display_symptom] + brands_info + [others_info]
        table_data.append(row)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 10), dpi=300)
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14])
    
    # IEEE standard formatting
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 2.0)
    
    # Format headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', fontsize=9)
        cell.set_facecolor('#d4d4d4')
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        cell.get_text().set_ha('center')
        cell.get_text().set_va('center')
    
    # Format data cells
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_edgecolor('none')
            cell.set_linewidth(0)
            cell.get_text().set_fontsize(7)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            # Color coding
            if j == 0:  # Symptom column
                cell.set_facecolor('#f0f0f0')
                cell.get_text().set_weight('bold')
            else:
                cell.set_facecolor('white')
            
            # Alternate row background
            if i % 2 == 0:
                if j == 0:
                    cell.set_facecolor('#e8e8e8')
                else:
                    cell.set_facecolor('#f5f5f5')
    
    # Add title
    plt.title('Brand Preference Distribution by Symptom - Top 5 Brands Analysis', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add subtitle
    plt.figtext(0.5, 0.02, 'Ranking shows most frequently prescribed brands for each symptom', 
                ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'symptom_brand_frequency_table.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nBrand Frequency Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def create_gender_symptom_table_png(df, symptoms_counts, output_dir):
    """Create gender distribution table PNG for symptoms"""
    
    # Prepare gender distribution data
    table_data = []
    headers = ["Symptom", "Total\nPatients", "Male\nCount", "Female\nCount", "Male\n%", "Female\n%", "Gender\nRatio (F:M)"]
    
    for symptom, total_patients in symptoms_counts.items():
        symptom_data = df[df['Symptoms'] == symptom]
        
        # Get gender distribution
        male_count, female_count = get_gender_distribution(symptom_data)
        male_pct = (male_count / total_patients * 100) if total_patients > 0 else 0
        female_pct = (female_count / total_patients * 100) if total_patients > 0 else 0
        
        # Calculate gender ratio
        if male_count > 0:
            gender_ratio = f"{female_count/male_count:.1f}:1"
        else:
            gender_ratio = "N/A"
        
        # Truncate symptom name
        display_symptom = symptom[:20] + "..." if len(symptom) > 23 else symptom
        
        row = [
            display_symptom,
            str(total_patients),
            str(male_count),
            str(female_count),
            f"{male_pct:.1f}",
            f"{female_pct:.1f}",
            gender_ratio
        ]
        
        table_data.append(row)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.25, 0.12, 0.12, 0.12, 0.10, 0.10, 0.15])
    
    # IEEE standard formatting
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 2.0)
    
    # Format headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', fontsize=10)
        cell.set_facecolor('#e6e6e6')
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        cell.get_text().set_ha('center')
        cell.get_text().set_va('center')
    
    # Format data cells with color coding
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_edgecolor('none')
            cell.set_linewidth(0)
            cell.get_text().set_fontsize(8)
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            
            # Color coding based on gender predominance
            if j in [4, 5]:  # Percentage columns
                try:
                    pct_value = float(table_data[i-1][j])
                    if pct_value > 60:
                        cell.set_facecolor('#ffcccc')  # Light red for high percentage
                    elif pct_value > 40:
                        cell.set_facecolor('#ffffcc')  # Light yellow for moderate
                    else:
                        cell.set_facecolor('white')
                except:
                    cell.set_facecolor('white')
            else:
                cell.set_facecolor('white')
            
            # Alternate row background
            if i % 2 == 0:
                if j in [4, 5]:  # Keep color coding for percentages
                    pass
                else:
                    cell.set_facecolor('#f5f5f5')
    
    # Add title
    plt.title('Gender Distribution Analysis by Symptom', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add subtitle
    plt.figtext(0.5, 0.02, 'Color coding: Red (>60%), Yellow (40-60%), White (<40%)', 
                ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    # Save as PNG
    output_filename = os.path.join(output_dir, 'symptom_gender_distribution_table.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png')
    
    print(f"\nGender Distribution Table PNG saved: {output_filename}")
    plt.close()
    
    return output_filename

def main():
    """Main function to run the analysis"""
    try:
        # Create output directory
        output_dir = 'symptoms_brand_graphs'
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        df, symptoms_counts = load_and_analyze_data('../521.xlsx')
        
        print(f"\n{'='*70}")
        print("GENERATING COMPREHENSIVE SYMPTOM-BRAND DATA TABLES...")
        print(f"{'='*70}")
        
        # Create comprehensive data table
        comprehensive_table = create_comprehensive_symptom_table(df, symptoms_counts, output_dir)
        summary_stats_table = create_symptom_summary_statistics_table(df, symptoms_counts, output_dir)
        
        # Create IEEE standard table PNGs for journal publication
        print(f"\n{'='*70}")
        print("GENERATING IEEE STANDARD TABLE PNGs FOR JOURNAL PUBLICATION...")
        print(f"{'='*70}")
        
        # Create comprehensive table PNG
        comprehensive_png = create_ieee_standard_symptom_table_png(df, symptoms_counts, output_dir)
        
        # Create brand frequency table PNG
        frequency_png = create_brand_frequency_table_png(df, symptoms_counts, output_dir)
        
        # Create gender distribution table PNG
        gender_png = create_gender_symptom_table_png(df, symptoms_counts, output_dir)
        
        print(f"\n{'='*70}")
        print("All symptom-brand tables generated successfully!")
        print(f"Table files created: 5 (2 data files + 3 PNG images)")
        print(f"Output directory: {output_dir}/")
        print("\nData Table files:")
        print(f"  - symptom_brand_comprehensive_table.csv")
        print(f"  - symptom_brand_comprehensive_table.txt")
        print(f"  - symptom_brand_summary_statistics.csv")
        print("\nJournal-Ready Table PNG files (IEEE Standard):")
        print(f"  - symptom_brand_comprehensive_table.png")
        print(f"  - symptom_brand_frequency_table.png")
        print(f"  - symptom_gender_distribution_table.png")
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