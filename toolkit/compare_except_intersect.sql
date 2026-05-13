/* ============================================================
   Source vs Target Data Consistency Validation
   Purpose:
       Validate that Source and Target datasets contain identical
       records. Categorize discrepancies into QA-friendly buckets:
       - MissingInTarget
       - ExtraInTarget
       - Match (expected)
       Provide row-count diagnostics for quick triage. 
   ============================================================ */

-----------------------------------------
-- Test Result Set: Full Comparison
-----------------------------------------
SELECT 'MissingInTarget' AS IssueType,
    TRY_CONVERT(BIGINT, TRIM(s.ID))                 AS ID,
    TRY_CONVERT(DATE,   TRIM(s.DATE_FIELD))         AS DATE_FIELD,
    TRY_CONVERT(INT,    TRIM(s.ACCOUNT_NUMBER))     AS ACCOUNT_NUMBER,
    TRY_CONVERT(VARCHAR(20), TRIM(s.COLUMN_4))      AS COLUMN_4,
    TRY_CONVERT(VARCHAR(20), TRIM(s.COLUMN_5))      AS COLUMN_5
FROM SourceTable s
EXCEPT
SELECT
    t.ID,
    t.DATE_FIELD,
    t.ACCOUNT_NUMBER,
    t.COLUMN_4,
    t.COLUMN_5
FROM TargetTable t

UNION ALL

SELECT 'ExtraInTarget' AS IssueType,
    t.ID,
    t.DATE_FIELD,
    t.ACCOUNT_NUMBER,
    t.COLUMN_4,
    t.COLUMN_5
FROM TargetTable t
EXCEPT
SELECT
    TRY_CONVERT(BIGINT, TRIM(s.ID)),
    TRY_CONVERT(DATE,   TRIM(s.DATE_FIELD)),
    TRY_CONVERT(INT,    TRIM(s.ACCOUNT_NUMBER)),
    TRY_CONVERT(VARCHAR(20), TRIM(s.COLUMN_4)),
    TRY_CONVERT(VARCHAR(20), TRIM(s.COLUMN_5))
FROM SourceTable s

UNION ALL

SELECT 'Match' AS IssueType,
    TRY_CONVERT(BIGINT, TRIM(s.ID))                 AS ID,
    TRY_CONVERT(DATE,   TRIM(s.DATE_FIELD))         AS DATE_FIELD,
    TRY_CONVERT(INT,    TRIM(s.ACCOUNT_NUMBER))     AS ACCOUNT_NUMBER,
    TRY_CONVERT(VARCHAR(20), TRIM(s.COLUMN_4))      AS COLUMN_4,
    TRY_CONVERT(VARCHAR(20), TRIM(s.COLUMN_5))      AS COLUMN_5
FROM SourceTable s
INTERSECT
SELECT
    t.ID,
    t.DATE_FIELD,
    t.ACCOUNT_NUMBER,
    t.COLUMN_4,
    t.COLUMN_5
FROM TargetTable t;

-----------------------------------------
-- Row Counts
-----------------------------------------
SELECT 'Source Count' AS Metric, COUNT(*) AS [RowCount]
FROM SourceTable

UNION ALL
SELECT 'Target Count' AS Metric, COUNT(*) AS [RowCount]
FROM TargetTable

UNION ALL
SELECT 'MissingInTarget' AS Metric, COUNT(*) AS [RowCount]
FROM (
    SELECT * FROM SourceTable
    EXCEPT
    SELECT * FROM TargetTable
) x

UNION ALL
SELECT 'ExtraInTarget' AS Metric, COUNT(*) AS [RowCount]
FROM (
    SELECT * FROM TargetTable
    EXCEPT
    SELECT * FROM SourceTable
) x

UNION ALL
SELECT 'ExactMatches' AS Metric, COUNT(*) AS [RowCount]
FROM (
    SELECT * FROM SourceTable
    INTERSECT
    SELECT * FROM TargetTable
) 
