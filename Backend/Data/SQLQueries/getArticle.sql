WITH NewTable AS
(
    SELECT *,
    ROW_NUMBER() OVER (ORDER BY Score DESC) AS RowNumber
    FROM ArticleInfo
    WHERE Category=@Category
)
SELECT TOP 10 * FROM NewTable
WHERE RowNumber>@minRow
ORDER BY RowNumber ASC;