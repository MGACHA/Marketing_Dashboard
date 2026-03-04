#run in terminal separately
#pip install sqlalchemy
#python -m pip install sqlalchemy
#python.exe -m pip install --upgrade pip
#& "C:/Program Files/Python313/python.exe" -m pip install pyodbc


import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import sys
import urllib.parse

# SQL Server Connection Parameters
# Update these with your SQL Server credentials
DB_CONFIG = {
    'server': 'magda3',  # or IP address like '192.168.1.100' or '.\SQLEXPRESS' for local instance
    'database': 'marketing_dashboard', #create database in MSSQL manually or using an additional script
    'driver': 'ODBC Driver 17 for SQL Server',  # or 'ODBC Driver 18 for SQL Server'
    'trusted_connection': 'yes',  # Use Windows Authentication (set to 'no' for SQL Server auth)
    'user': '',  # Only needed if trusted_connection = 'no'
    'password': ''  # Only needed if trusted_connection = 'no'
}

def load_csv_to_sqlserver():
    """Load marketing_data.csv into SQL Server database"""
    
    # Read the CSV file
    print("Reading marketing_data.csv...")
    df = pd.read_csv("marketing_data.csv")
    
    # Convert Date column to proper datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate additional metrics
    df['ConversionRate'] = (df['Conversions'] / df['Leads'] * 100).round(2)
    df['CostPerLead'] = (df['Spend'] / df['Leads']).round(2)
    df['CostPerConversion'] = (df['Spend'] / df['Conversions'].replace(0, 1)).round(2)
    
    # Create SQL Server connection string
    if DB_CONFIG['trusted_connection'].lower() == 'yes':
        # Windows Authentication
        connection_string = (
            f"mssql+pyodbc://@{DB_CONFIG['server']}/{DB_CONFIG['database']}"
            f"?driver={urllib.parse.quote_plus(DB_CONFIG['driver'])}"
            f"&trusted_connection=yes"
        )
    else:
        # SQL Server Authentication
        connection_string = (
            f"mssql+pyodbc://{DB_CONFIG['user']}:{urllib.parse.quote_plus(DB_CONFIG['password'])}"
            f"@{DB_CONFIG['server']}/{DB_CONFIG['database']}"
            f"?driver={urllib.parse.quote_plus(DB_CONFIG['driver'])}"
        )
    
    try:
        # Create SQLAlchemy engine
        print(f"\nConnecting to SQL Server database '{DB_CONFIG['database']}'...")
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Connected successfully!")
        
    except Exception as e:
        print(f"\n❌ Error connecting to SQL Server: {e}")
        print("\nPlease ensure:")
        print("1. SQL Server is installed and running")
        print("2. The database 'marketing_dashboard' exists (or create it first)")
        print("3. SQL Server is configured to accept connections")
        print("4. The ODBC driver is installed")
        print("\nTo create the database, run in SQL Server:")
        print("  CREATE DATABASE marketing_dashboard;")
        print("\nTo check available ODBC drivers, run in PowerShell:")
        print("  Get-OdbcDriver | Where-Object {$_.Name -like '*SQL Server*'}")
        sys.exit(1)
    
    # Load main data into SQL Server table
    print(f"\nLoading data into marketing_campaigns table...")
    df.to_sql('marketing_campaigns', engine, if_exists='replace', index=False)
    print("✓ Main table created!")
    
    # Create aggregated tables using SQL
    with engine.connect() as conn:
        # 1. Campaign Performance Summary
        print("\nCreating campaign_summary table...")
        conn.execute(text("DROP TABLE IF EXISTS campaign_summary"))
        summary_query = text("""
        SELECT 
            CampaignName,
            COUNT(*) as TotalRecords,
            SUM(Leads) as TotalLeads,
            SUM(Conversions) as TotalConversions,
            SUM(Spend) as TotalSpend,
            ROUND(AVG(ConversionRate), 2) as AvgConversionRate,
            ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0), 2) as OverallConversionRate,
            ROUND(SUM(Spend) / NULLIF(SUM(Leads), 0), 2) as CostPerLead,
            ROUND(SUM(Spend) / NULLIF(SUM(Conversions), 0), 2) as CostPerConversion
        INTO campaign_summary
        FROM marketing_campaigns
        GROUP BY CampaignName
        """)
        conn.execute(summary_query)
        conn.commit()
        print("✓ Campaign summary created!")
        
        # 2. Daily Performance
        print("Creating daily_performance table...")
        conn.execute(text("DROP TABLE IF EXISTS daily_performance"))
        daily_query = text("""
        SELECT 
            Date,
            SUM(Leads) as TotalLeads,
            SUM(Conversions) as TotalConversions,
            SUM(Spend) as TotalSpend,
            ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0), 2) as ConversionRate
        INTO daily_performance
        FROM marketing_campaigns
        GROUP BY Date
        ORDER BY Date
        """)
        conn.execute(daily_query)
        conn.commit()
        print("✓ Daily performance created!")
    
    # Display summary
    print("\n" + "="*60)
    print("DATABASE CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nDatabase: {DB_CONFIG['database']}")
    print(f"Server: {DB_CONFIG['server']}")
    print("\nTables created:")
    print("1. marketing_campaigns (main data table)")
    print("2. campaign_summary (aggregated by campaign)")
    print("3. daily_performance (aggregated by date)")
    
    # Show sample data
    print("\n" + "-"*60)
    print("Sample from marketing_campaigns table:")
    print("-"*60)
    sample_df = pd.read_sql("SELECT TOP 5 * FROM marketing_campaigns", engine)
    print(sample_df.to_string(index=False))
    
    print("\n" + "-"*60)
    print("Campaign Summary:")
    print("-"*60)
    summary_df = pd.read_sql('SELECT * FROM campaign_summary ORDER BY TotalSpend DESC', engine)
    print(summary_df.to_string(index=False))
    
    print("\n✓ Data loaded successfully!")
    print("\n" + "="*60)
    print("CONNECT TO POWER BI:")
    print("="*60)
    print("1. Open Power BI Desktop")
    print("2. Get Data > Database > SQL Server")
    print(f"3. Server: {DB_CONFIG['server']}")
    print(f"4. Database: {DB_CONFIG['database']}")
    print("5. Select tables: marketing_campaigns, campaign_summary, daily_performance")
    print("6. Click 'Load' to import the data")


if __name__ == "__main__":
    load_csv_to_sqlserver()
