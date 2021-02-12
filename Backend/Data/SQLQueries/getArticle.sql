WITH NewTable AS
(
    SELECT *,
    ROW_NUMBER() OVER (ORDER BY Score, Headline DESC) AS RowNumber
    FROM ArticleInfo2
    WHERE Category=@Category
)
SELECT TOP 10 * FROM NewTable
WHERE RowNumber>@minRow
ORDER BY RowNumber ASC;