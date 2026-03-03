r"""
Marketing Data Visualization - Terminal Version

This script reads marketing_data.csv and creates visualizations in the terminal/PowerShell.

Setup Instructions:
1. Make sure you've run loaddata.py first to generate the CSV
2. Install required packages: pip install -r requirements.txt
3. Run this script: python visualize_terminal.py
"""

# Import required libraries
try:
    import pandas as pd  # Import pandas for data manipulation and CSV reading
    import plotext as plt  # Import plotext for creating terminal-based charts
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

print("=" * 80)  # Print separator line
print("MARKETING CAMPAIGN ANALYTICS DASHBOARD - TERMINAL VIEW")  # Print main title
print("=" * 80)  # Print separator line
print()  # Empty line for spacing

# 1. Histogram of Leads
plt.hist(df['Leads'].tolist(), bins=20)  # Create histogram of leads with 20 bins
plt.title('Distribution of Leads')  # Set the title for this chart
plt.xlabel('Number of Leads')  # Label the x-axis
plt.ylabel('Frequency')  # Label the y-axis
plt.theme('dark')  # Use dark theme for better terminal visibility
plt.show()  # Display the chart in terminal
print()  # Empty line for spacing

# 2. Histogram of Conversions
plt.clf()  # Clear the previous plot
plt.hist(df['Conversions'].tolist(), bins=20)  # Create histogram of conversions with 20 bins
plt.title('Distribution of Conversions')  # Set the title for this chart
plt.xlabel('Number of Conversions')  # Label the x-axis
plt.ylabel('Frequency')  # Label the y-axis
plt.theme('dark')  # Use dark theme for better terminal visibility
plt.show()  # Display the chart in terminal
print()  # Empty line for spacing

# 3. Total Leads by Campaign
plt.clf()  # Clear the previous plot
campaign_leads = df.groupby('CampaignName')['Leads'].sum().sort_values(ascending=False)  # Group data by campaign, sum all leads, sort from highest to lowest
plt.bar(campaign_leads.index.tolist(), campaign_leads.values.tolist())  # Create vertical bar chart
plt.title('Total Leads by Campaign')  # Set the title for this chart
plt.xlabel('Campaign')  # Label the x-axis
plt.ylabel('Total Leads')  # Label the y-axis
plt.theme('dark')  # Use dark theme for better terminal visibility
plt.show()  # Display the chart in terminal
print()  # Empty line for spacing

# 4. Total Spend by Campaign
plt.clf()  # Clear the previous plot
campaign_spend = df.groupby('CampaignName')['Spend'].sum().sort_values(ascending=False)  # Group data by campaign, sum all spending, sort from highest to lowest
plt.bar(campaign_spend.index.tolist(), campaign_spend.values.tolist())  # Create vertical bar chart
plt.title('Total Spend by Campaign ($)')  # Set the title for this chart
plt.xlabel('Campaign')  # Label the x-axis
plt.ylabel('Total Spend ($)')  # Label the y-axis
plt.theme('dark')  # Use dark theme for better terminal visibility
plt.show()  # Display the chart in terminal
print()  # Empty line for spacing

# Print summary statistics
print("=" * 80)  # Print separator line
print("SUMMARY STATISTICS")  # Print header for statistics section
print("=" * 80)  # Print separator line
print(f"Total Campaigns: {df['CampaignName'].nunique()}")  # Count unique campaign names
print(f"Total Records: {len(df)}")  # Count total number of rows in the data
print(f"Total Leads: {df['Leads'].sum():,}")  # Sum all leads and format with comma separators
print(f"Total Conversions: {df['Conversions'].sum():,}")  # Sum all conversions and format with comma separators
print(f"Total Spend: ${df['Spend'].sum():,.2f}")  # Sum all spending, format with dollar sign, commas, and 2 decimal places
print(f"Average Conversion Rate: {(df['Conversions'].sum() / df['Leads'].sum() * 100):.2f}%")  # Calculate conversion rate percentage and format to 2 decimals
print("=" * 80)  # Print separator line
