use marketing_dashboard
-- 1. Create FIRST the table (drop if exists first)
IF OBJECT_ID('campaign_sum', 'U') IS NOT NULL
    DROP TABLE campaign_sum;
GO

CREATE TABLE campaign_sum (
    CampaignName            VARCHAR(255),
    TotalRecords            INT,
    TotalLeads              INT,
    TotalConversions        INT,
    TotalSpend              DECIMAL(18,2),
    AvgConversionRate       DECIMAL(10,2),
    OverallConversionRate   DECIMAL(10,2),
    CostPerLead             DECIMAL(18,2),
    CostPerConversion       DECIMAL(18,2)
);
GO

-- 2. Insert aggregated data
INSERT INTO campaign_sum
(
    CampaignName,
    TotalRecords,
    TotalLeads,
    TotalConversions,
    TotalSpend,
    AvgConversionRate,
    OverallConversionRate,
    CostPerLead,
    CostPerConversion
)
SELECT 
    CampaignName,
    COUNT(*) AS TotalRecords,
    SUM(Leads) AS TotalLeads,
    SUM(Conversions) AS TotalConversions,
    SUM(Spend) AS TotalSpend,
    ROUND(AVG(ConversionRate), 2) AS AvgConversionRate,
    ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0), 2) AS OverallConversionRate,
    ROUND(SUM(Spend) / NULLIF(SUM(Leads), 0), 2) AS CostPerLead,
    ROUND(SUM(Spend) / NULLIF(SUM(Conversions), 0), 2) AS CostPerConversion
FROM marketing_campaigns
GROUP BY CampaignName;
GO


Select * from campaign_sum

-------------------


-- 1. Create SECOND the table (drop if exists first)
IF OBJECT_ID('daily_perf', 'U') IS NOT NULL
    DROP TABLE daily_perf;
GO

CREATE TABLE daily_perf (
    Date                DATE,
    TotalLeads          INT,
    TotalConversions    INT,
    TotalSpend          DECIMAL(18,2),
    ConversionRate      DECIMAL(10,2)
);
GO


-- 2. Insert aggregated data
INSERT INTO daily_perf
(
    Date,
    TotalLeads,
    TotalConversions,
    TotalSpend,
    ConversionRate
)
SELECT 
    Date,
    SUM(Leads) AS TotalLeads,
    SUM(Conversions) AS TotalConversions,
    SUM(Spend) AS TotalSpend,
    ROUND(
        SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0),
        2
    ) AS ConversionRate
FROM marketing_campaigns
GROUP BY Date
ORDER BY Date;
GO


select * from daily_perf

