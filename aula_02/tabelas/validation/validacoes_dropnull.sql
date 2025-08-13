-- total linhas por tabela
SELECT
  (SELECT COUNT(*) FROM silver_sales_normalized)  AS qt_norm,
  (SELECT COUNT(*) FROM silver_sales_enriched)    AS qt_enriched,
  (SELECT COUNT(*) FROM silver_sales_enriched WHERE preco_unitario_usd IS NOT NULL) AS qt_com_preco,
  ROUND(100.0 * (SELECT COUNT(*) FROM silver_sales_enriched WHERE preco_unitario_usd IS NOT NULL)
/ NULLIF((SELECT COUNT(*) FROM silver_sales_enriched),0), 2) AS pct_com_preco;
