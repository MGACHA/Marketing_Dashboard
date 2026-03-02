# Marketing Data Generator
This script generates fake marketing campaign data and saves it to a CSV file.
Setup Instructions:
1. Create a virtual environment (if not already done):
   python -m venv .venv
2. Activate the virtual environment:
   Windows: .venv\Scripts\Activate.ps1
3. Install required packages:
   pip install -r requirements.txt
4. Run the script:
   python loaddata.py

# Marketing Data Visualisation
This script reads marketing_data.csv and creates various visualisations.
Setup Instructions:
1. Make sure you've run loaddata.py first to generate the CSV
2. Install required packages: pip install -r requirements.txt
3. Run this script: python visualize_data.py


# marketing_data.csv
CampaignName - what marketing campaign this row is about
Examples:
"Google Ads"
"Email Blast"
"Social Ads"
"Referral"
"Facebook Ads"

Date - when the activity happened
Example: 2026-03-01

Leads how many people showed interest
Example:
45 leads = 45 people clicked/signed up / left email

Conversions - real interest - how many of those leads became customers
Example:
45 leads -> 5 conversions

Spend - how much money was spent on the campaign
Example: 120.50 GBP spent on Google Ads that day.


# Marketing_analytics.png

### 1. Histogram of Leads - How frequently different lead counts occur across all 250 records.
### 2. Histogram of Conversions - How frequently different conversion counts occur across all records.
### 3. Total Leads by Campaign
### 4. Total Spend by Campaign



# Dashboard.xlsx
results in the Excel histograms, bar charts, and pivot tables showing data


