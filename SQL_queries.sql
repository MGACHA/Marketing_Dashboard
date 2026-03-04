-- SQL Queries for Marketing Dashboard Analysis
-- QUERY 1: Overall Campaign Performance
-- Shows total metrics for each campaign type
-- ============================================================================
SELECT 
    CampaignName,
    COUNT(*) as TotalRecords,
    SUM(Leads) as TotalLeads,
    SUM(Conversions) as TotalConversions,
    SUM(Spend) as TotalSpend,
    ROUND(SUM(Conversions) * 100.0 / SUM(Leads), 2) as ConversionRate,
    ROUND(SUM(Spend) / SUM(Leads), 2) as CostPerLead,
    ROUND(SUM(Spend) / NULLIF(SUM(Conversions), 0), 2) as CostPerConversion,
    ROUND((SUM(Conversions) * 100) / SUM(Spend), 2) as ROIScore
FROM marketing_campaigns
GROUP BY CampaignName
ORDER BY TotalConversions DESC;


-- QUERY 2: Daily Trend Analysis
-- Track performance over time
-- ============================================================================
SELECT 
    Date,
    COUNT(DISTINCT CampaignName) as ActiveCampaigns,
    SUM(Leads) as DailyLeads,
    SUM(Conversions) as DailyConversions,
    SUM(Spend) as DailySpend,
    ROUND(SUM(Conversions) * 100.0 / SUM(Leads), 2) as DailyConversionRate
FROM marketing_campaigns
GROUP BY Date
ORDER BY Date DESC;


-- QUERY 3: Top Performing Campaigns by Conversion Rate
-- Find campaigns with best conversion rates (minimum 10 leads for reliability)
-- ============================================================================
SELECT TOP 10
    CampaignName,
    Date,
    Leads,
    Conversions,
    Spend,
    ConversionRate,
    CostPerConversion
FROM marketing_campaigns
WHERE Leads >= 10
ORDER BY ConversionRate DESC



-- QUERY 4: Budget Efficiency Analysis
-- Find campaigns with lowest cost per conversion
-- ============================================================================
SELECT 
    CampaignName,
    SUM(Spend) as TotalSpend,
    SUM(Conversions) as TotalConversions,
    ROUND(SUM(Spend) / NULLIF(SUM(Conversions), 0), 2) as AvgCostPerConversion,
    ROUND(SUM(Conversions) * 100.0 / SUM(Leads), 2) as ConversionRate
FROM marketing_campaigns
GROUP BY CampaignName
HAVING SUM(Conversions) > 0
ORDER BY AvgCostPerConversion ASC;


-- QUERY 5: Weekly Performance Aggregation
-- Group by week for trend analysis
-- ============================================================================
SELECT
    CONCAT(
        DATEPART(YEAR, Date),
        '-W',
        RIGHT('0' + CAST(DATEPART(ISO_WEEK, Date) AS VARCHAR(2)), 2)
    ) AS Week,
    CampaignName,
    SUM(Leads) AS WeeklyLeads,
    SUM(Conversions) AS WeeklyConversions,
    SUM(Spend) AS WeeklySpend,
    ROUND(SUM(Conversions) * 100.0 / SUM(Leads), 2) AS WeeklyConversionRate
FROM marketing_campaigns
GROUP BY 
    CONCAT(
        DATEPART(YEAR, Date),
        '-W',
        RIGHT('0' + CAST(DATEPART(ISO_WEEK, Date) AS VARCHAR(2)), 2)
    ),
    CampaignName
ORDER BY 
    Week DESC,
    WeeklyConversions DESC;


-- QUERY 6: Campaign Performance Matrix
-- Compare all campaigns across key metrics
-- ============================================================================
SELECT 
    CampaignName,
    SUM(Leads) as TotalLeads,
    SUM(Conversions) as TotalConversions,
    SUM(Spend) as TotalSpend,
    ROUND(AVG(ConversionRate), 2) as AvgConversionRate,
    ROUND(MIN(CostPerConversion), 2) as BestCostPerConversion,
    ROUND(MAX(CostPerConversion), 2) as WorstCostPerConversion,
    ROUND(AVG(CostPerConversion), 2) as AvgCostPerConversion
FROM marketing_campaigns
WHERE Conversions > 0
GROUP BY CampaignName
ORDER BY TotalConversions DESC;


-- QUERY 7: High Spend Low Performance Campaigns
-- Identify campaigns that may need optimization
-- ============================================================================
SELECT 
    CampaignName,
    Date,
    Leads,
    Conversions,
    Spend,
    ConversionRate,
    CostPerConversion
FROM marketing_campaigns
WHERE Spend > 300 
  AND ConversionRate < 30
ORDER BY Spend DESC;


-- QUERY 8: Best ROI Days
-- Find dates with best return on investment
-- ============================================================================
SELECT TOP 10
    Date,
    SUM(Conversions) as TotalConversions,
    SUM(Spend) as TotalSpend,
    ROUND(SUM(Conversions) * 100.0 / SUM(Spend), 2) as ConversionsPerDollar,
    COUNT(DISTINCT CampaignName) as NumberOfCampaigns
FROM marketing_campaigns
GROUP BY Date
HAVING SUM(Conversions) > 0
ORDER BY ConversionsPerDollar DESC

-- QUERY 9: Campaign Comparison - Above vs Below Average
-- Compare each campaign to overall average
-- ============================================================================
WITH avg_metrics AS (
    SELECT 
        AVG(ConversionRate) as avg_conversion_rate,
        AVG(CostPerLead) as avg_cost_per_lead
    FROM marketing_campaigns
)
SELECT 
    mc.CampaignName,
    ROUND(AVG(mc.ConversionRate), 2) as CampaignConversionRate,
    ROUND(am.avg_conversion_rate, 2) as OverallAvgConversionRate,
    CASE 
        WHEN AVG(mc.ConversionRate) > am.avg_conversion_rate THEN 'Above Average'
        ELSE 'Below Average'
    END as Performance,
    ROUND(AVG(mc.CostPerLead), 2) as CampaignCostPerLead,
    ROUND(am.avg_cost_per_lead, 2) as OverallAvgCostPerLead
FROM marketing_campaigns mc
CROSS JOIN avg_metrics am
GROUP BY mc.CampaignName, am.avg_conversion_rate, am.avg_cost_per_lead
ORDER BY CampaignConversionRate DESC;


-- QUERY 10: Monthly Summary
-- High-level monthly overview
-- ============================================================================
SELECT
    CONCAT(
        DATEPART(YEAR, Date),
        '-M',
        RIGHT('0' + CAST(DATEPART(MONTH, Date) AS VARCHAR(2)), 2)
    ) AS Month,
    COUNT(*) AS TotalCampaignRuns,
    SUM(Leads) AS TotalLeads,
    SUM(Conversions) AS TotalConversions,
    SUM(Spend) AS TotalSpend,
    ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Leads), 0), 2) AS MonthlyConversionRate,
    ROUND(SUM(Spend) / NULLIF(SUM(Leads), 0), 2) AS MonthlyCostPerLead
FROM marketing_campaigns
GROUP BY 
    CONCAT(
        DATEPART(YEAR, Date),
        '-M',
        RIGHT('0' + CAST(DATEPART(MONTH, Date) AS VARCHAR(2)), 2)
    )
ORDER BY Month DESC;
