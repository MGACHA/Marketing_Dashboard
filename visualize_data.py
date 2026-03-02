"""Marketing Data Visualization

This script reads marketing_data.csv and creates various visualizations.

Setup Instructions:
1. Make sure you've run loaddata.py first to generate the CSV
2. Install required packages: pip install -r requirements.txt
3. Run this script: python visualize_data.py
"""

# import required libraries
try:
    import pandas as pd  # Import pandas for data manipulation and CSV reading
    import matplotlib.pyplot as plt  # Import matplotlib for creating charts and graphs
except ImportError as e:  # If any library is missing, catch the error
    print(f"Error: Required package not installed - {e}")  # Display which package is missing
    print("Please install requirements: pip install -r requirements.txt")  # Show installation instructions
    exit(1)  # Exit the program with error code 1

# Read the marketing data
try:  # Try to read the CSV file
    df = pd.read_csv("marketing_data.csv")  # Load the CSV file into a pandas DataFrame
    print(f"Loaded {len(df)} records from marketing_data.csv\n")  # Display how many rows were loaded
except FileNotFoundError:  # If the CSV file doesn't exist, catch the error
    print("Error: marketing_data.csv not found!")  # Tell user the file is missing
    print("Please run loaddata.py first to generate the data.")  # Provide instructions to fix the issue
    exit(1)  # Exit the program with error code 1

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # Create a 2x2 grid of charts, size 14x10 inches
fig.suptitle('Marketing Campaign Analytics Dashboard', fontsize=16, fontweight='bold')  # Add main title to the entire figure

# 1. Histogram of Leads
axes[0, 0].hist(df['Leads'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)  # Create histogram in top-left position with 20 bins, skyblue color
axes[0, 0].set_title('Distribution of Leads', fontweight='bold')  # Set the title for this chart
axes[0, 0].set_xlabel('Number of Leads')  # Label the x-axis
axes[0, 0].set_ylabel('Frequency')  # Label the y-axis
axes[0, 0].grid(axis='y', alpha=0.3)  # Add horizontal grid lines with 30% transparency

# 2. Histogram of Conversions
axes[0, 1].hist(df['Conversions'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)  # Create histogram in top-right position with 20 bins, light green color
axes[0, 1].set_title('Distribution of Conversions', fontweight='bold')  # Set the title for this chart
axes[0, 1].set_xlabel('Number of Conversions')  # Label the x-axis
axes[0, 1].set_ylabel('Frequency')  # Label the y-axis
axes[0, 1].grid(axis='y', alpha=0.3)  # Add horizontal grid lines with 30% transparency

# 3. Total Leads by Campaign
campaign_leads = df.groupby('CampaignName')['Leads'].sum().sort_values(ascending=True)  # Group data by campaign, sum all leads, sort from lowest to highest
axes[1, 0].barh(campaign_leads.index, campaign_leads.values, color='coral')  # Create horizontal bar chart in bottom-left position with coral color
axes[1, 0].set_title('Total Leads by Campaign', fontweight='bold')  # Set the title for this chart
axes[1, 0].set_xlabel('Total Leads')  # Label the x-axis
axes[1, 0].grid(axis='x', alpha=0.3)  # Add vertical grid lines with 30% transparency

# 4. Total Spend by Campaign
campaign_spend = df.groupby('CampaignName')['Spend'].sum().sort_values(ascending=True)  # Group data by campaign, sum all spending, sort from lowest to highest
axes[1, 1].barh(campaign_spend.index, campaign_spend.values, color='mediumpurple')  # Create horizontal bar chart in bottom-right position with purple color
axes[1, 1].set_title('Total Spend by Campaign', fontweight='bold')  # Set the title for this chart
axes[1, 1].set_xlabel('Total Spend ($)')  # Label the x-axis with dollar sign
axes[1, 1].grid(axis='x', alpha=0.3)  # Add vertical grid lines with 30% transparency

plt.tight_layout()  # Automatically adjust spacing between subplots to prevent overlap

# Save the figure
output_file = 'marketing_analytics.jpg'  # Define the output filename
plt.savefig(output_file, dpi=300, bbox_inches='tight')  # Save the figure as JPG with 300 DPI (high quality), tight bounding box
print(f"Visualizations saved to: {output_file}")  # Confirm the file was saved

# Show the plot
plt.show()  # Display the charts in a window

# Print some summary statistics
print("\n=== Summary Statistics ===")  # Print header for statistics section
print(f"Total Campaigns: {df['CampaignName'].nunique()}")  # Count unique campaign names
print(f"Total Records: {len(df)}")  # Count total number of rows in the data
print(f"Total Leads: {df['Leads'].sum():,}")  # Sum all leads and format with comma separators
print(f"Total Conversions: {df['Conversions'].sum():,}")  # Sum all conversions and format with comma separators
print(f"Total Spend: ${df['Spend'].sum():,.2f}")  # Sum all spending, format with dollar sign, commas, and 2 decimal places
print(f"Average Conversion Rate: {(df['Conversions'].sum() / df['Leads'].sum() * 100):.2f}%")  # Calculate conversion rate percentage and format to 2 decimals
