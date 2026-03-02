r"""
Marketing Data Generator

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
"""

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is not installed.")
    print("Please install it by running: pip install pandas")
    print("Or install all requirements: pip install -r requirements.txt")
    exit(1)

import random
from datetime import datetime, timedelta

# Example: generate fake campaigns data
campaigns = ["Email Blast", "Social Ads", "Google Ads", "Referral", "Affiliate", "Facebook Ads"]
data = []

for i in range(250):
    campaign = random.choice(campaigns)
    date = datetime.today() - timedelta(days=random.randint(0,30))
    leads = random.randint(10, 100)
    conversions = random.randint(0, leads)
    spend = round(random.uniform(50, 500), 2)
    data.append([campaign, date.date(), leads, conversions, spend])

df = pd.DataFrame(data, columns=["CampaignName", "Date", "Leads", "Conversions", "Spend"])
df.to_csv("marketing_data.csv", index=False)
print(df.head())
