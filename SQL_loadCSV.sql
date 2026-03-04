use marketing_dashboard

DROP TABLE IF EXISTS marketing_campaigns_v2;
GO

CREATE TABLE marketing_campaigns_v2 (
    Date VARCHAR(50),
    CampaignName VARCHAR(255),
    Leads VARCHAR(50),
    Conversions VARCHAR(50),
    Spend VARCHAR(50)
);
GO


BULK INSERT marketing_campaigns_v2
FROM 'C:\bootcamp\project1\marketing_data.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',  
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO
