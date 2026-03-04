-- main table data from marketing_campains.csv
select * from  marketing_campaigns

-- query table marketing_campaigns to get summary
  
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
        FROM marketing_campaigns
        GROUP BY CampaignName

-- query table marketing_campaigns to get summary GROUPED BY date and CampaigneName

SELECT
    Date,
	CampaignName,
    SUM(Leads)        AS TotalLeads,
    SUM(Conversions) AS TotalConversions,
    SUM(Spend)        AS TotalSpend,
    ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0), 2) AS ConversionRate
FROM marketing_campaigns
GROUP BY Date, CampaignName
ORDER BY Date;

-- query table marketing_campaigns to get performance summary GROUPED BY date 
SELECT 
            Date,
            SUM(Leads) as TotalLeads,
            SUM(Conversions) as TotalConversions,
            SUM(Spend) as TotalSpend,
            ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0), 2) as ConversionRate
    
        FROM marketing_campaigns
        GROUP BY Date
        ORDER BY Date
