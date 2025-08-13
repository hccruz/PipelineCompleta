# **Carga de Dados Bronze no PostgreSQL**

Este processo realiza o **carregamento de CSVs da camada Bronze** diretamente no banco de dados PostgreSQL, usando como nome de tabela o mesmo nome do arquivo.

---

## **1. Criar as tabelas no banco**

Antes de rodar o script Python, execute o SQL abaixo no seu banco PostgreSQL para criar as tabelas da camada Bronze:

```sql
-- ============================================
-- BRONZE • COTAÇÕES (base fornecida)
-- ============================================
CREATE TABLE IF NOT EXISTS bronze_cotacoes (
  id              BIGSERIAL PRIMARY KEY,
  ativo           TEXT NOT NULL,           -- Ex.: BTC-USD, GC=F, CL=F, SI=F
  preco           NUMERIC(18,6) NOT NULL,  -- Preço coletado
  moeda           CHAR(3) NOT NULL DEFAULT 'USD',
  horario_coleta  TIMESTAMPTZ NOT NULL,    -- Quando o script coletou
  inserido_em     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- BRONZE • CLIENTES
-- ============================================
CREATE TABLE IF NOT EXISTS bronze_customers (
  bronze_customer_id BIGSERIAL PRIMARY KEY,
  customer_id        TEXT NOT NULL,
  customer_name      VARCHAR(200) NOT NULL,
  documento          VARCHAR(32),
  segmento           VARCHAR(64),
  pais               VARCHAR(64),
  estado             VARCHAR(16),
  cidade             VARCHAR(100),
  created_at         TIMESTAMPTZ NOT NULL
);

-- ============================================
-- BRONZE • VENDAS BTC (sem preço unitário)
-- ============================================
CREATE TABLE IF NOT EXISTS bronze_sales_btc_excel (
  bronze_sales_btc_id BIGSERIAL PRIMARY KEY,
  transaction_id      TEXT NOT NULL,
  data_hora           TIMESTAMPTZ NOT NULL,
  ativo               VARCHAR(16) NOT NULL,
  quantidade          NUMERIC(18,6) NOT NULL CHECK (quantidade > 0),
  tipo_operacao       VARCHAR(10) NOT NULL CHECK (tipo_operacao IN ('COMPRA','VENDA')),
  moeda               VARCHAR(10) NOT NULL,
  cliente_id          TEXT,
  canal               VARCHAR(32),
  mercado             VARCHAR(8),
  arquivo_origem      VARCHAR(256),
  importado_em        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- BRONZE • VENDAS COMMODITIES (sem preço unitário)
-- ============================================
CREATE TABLE IF NOT EXISTS bronze_sales_commodities_sql (
  bronze_sales_comm_id BIGSERIAL PRIMARY KEY,
  transaction_id       TEXT NOT NULL,
  data_hora            TIMESTAMPTZ NOT NULL,
  commodity_code       VARCHAR(20) NOT NULL,
  quantidade           NUMERIC(18,6) NOT NULL CHECK (quantidade > 0),
  tipo_operacao        VARCHAR(10) NOT NULL CHECK (tipo_operacao IN ('COMPRA','VENDA')),
  unidade              VARCHAR(16) NOT NULL,
  moeda                VARCHAR(10) NOT NULL,
  cliente_id           TEXT,
  canal                VARCHAR(32),
  mercado              VARCHAR(8),
  arquivo_origem       VARCHAR(256),
  importado_em         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## **2. Preparar o ambiente**

1. **Instalar dependências**

   ```bash
   pip install pandas sqlalchemy psycopg2-binary python-dotenv
   ```

2. **Criar arquivo `.env`** na raiz do projeto com os dados de conexão:

   ```env
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=seu_banco
   ```

3. **Criar pasta `data_bronze/`** e colocar nela todos os CSVs:

   ```
   data_bronze/
   ├── bronze_cotacoes.csv
   ├── bronze_customers.csv
   ├── bronze_sales_btc_excel.csv
   └── bronze_sales_commodities_sql.csv
   ```

---

## **3. Executar o script de carga**

Para rodar:

```bash
python load_bronze.py
```

O script vai:

* Ler todos os arquivos `.csv` da pasta `data_bronze/`
* Criar um `DataFrame` para cada um
* Inserir no PostgreSQL usando **append**
* Usar o **nome do arquivo** como nome da tabela

---

## **4. Observações**

* O processo é **append-only** (não altera ou deleta registros existentes)
* As tabelas têm **PK própria** na camada Bronze (BIGSERIAL)
* Se necessário, adicione **constraints de unicidade** para evitar duplicação de registros da mesma origem
* Caso o schema do CSV não bata com o da tabela, ajuste o CSV ou altere o script para reordenar as colunas

Segue um esqueleto de README para a **aula de SQL** usando as suas tabelas Bronze como base, já estruturado para ensino, com exemplos práticos para cada comando.

---

# *Aula: 2 Principais Comandos SQL de Consulta**

> **Objetivo**: aprender e praticar os principais comandos de consulta em SQL usando nossas tabelas da camada Bronze no PostgreSQL.

## **1. SELECT — Selecionando dados**

```sql
-- Todos os registros da tabela de cotações
SELECT * 
FROM bronze_cotacoes;

-- Selecionar colunas específicas
SELECT ativo, preco, horario_coleta 
FROM bronze_cotacoes;
```

---

## **2. WHERE — Filtrando resultados**

```sql
-- Filtrar vendas de BTC
SELECT *
FROM bronze_sales_btc_excel
WHERE ativo = 'BTC-USD';

-- Cotações com preço acima de 2000
SELECT ativo, preco
FROM bronze_cotacoes
WHERE preco > 2000;
```

---

## **3. ORDER BY — Ordenando resultados**

```sql
-- Cotações mais recentes primeiro
SELECT ativo, preco, horario_coleta
FROM bronze_cotacoes
ORDER BY horario_coleta DESC;

-- Top 5 vendas com maior quantidade
SELECT *
FROM bronze_sales_commodities_sql
ORDER BY quantidade DESC
LIMIT 5;
```

---

## **4. LIMIT — Restringindo o número de linhas**

```sql
-- Apenas 10 primeiras linhas
SELECT *
FROM bronze_customers
LIMIT 10;
```

---

## **5. DISTINCT — Eliminando duplicados**

```sql
-- Lista de ativos únicos
SELECT DISTINCT ativo
FROM bronze_cotacoes;

-- Lista de países cadastrados
SELECT DISTINCT pais
FROM bronze_customers;
```

---

## **6. LIKE — Pesquisa por padrão**

```sql
-- Clientes com nome contendo 'SILVA'
SELECT *
FROM bronze_customers
WHERE customer_name ILIKE '%SILVA%';

-- Ativos que começam com 'GC'
SELECT *
FROM bronze_cotacoes
WHERE ativo LIKE 'GC%';
```

---

## **7. IN — Filtrando por múltiplos valores**

```sql
-- Vendas apenas de Ouro e Prata
SELECT *
FROM bronze_sales_commodities_sql
WHERE commodity_code IN ('GOLD', 'SILVER');

-- Clientes de estados específicos
SELECT *
FROM bronze_customers
WHERE estado IN ('SP', 'RJ');
```

---

## **8. BETWEEN — Intervalos**

```sql
-- Cotações entre duas datas
SELECT *
FROM bronze_cotacoes
WHERE horario_coleta BETWEEN '2025-08-01' AND '2025-08-10';

-- Vendas com quantidade entre 10 e 50
SELECT *
FROM bronze_sales_btc_excel
WHERE quantidade BETWEEN 10 AND 50;
```

---

## **9. JOIN — Unindo tabelas**

```sql
-- Juntar vendas BTC com dados de clientes
SELECT s.transaction_id, s.data_hora, c.customer_name
FROM bronze_sales_btc_excel s
JOIN bronze_customers c
  ON s.cliente_id = c.customer_id;

-- Juntar vendas de commodities com cotações
SELECT v.transaction_id, v.commodity_code, cot.preco
FROM bronze_sales_commodities_sql v
JOIN bronze_cotacoes cot
  ON v.commodity_code = cot.ativo;
```

---

## **10. GROUP BY + Aggregations — Agrupando e agregando**

```sql
-- Média de preço por ativo
SELECT ativo, AVG(preco) AS media_preco
FROM bronze_cotacoes
GROUP BY ativo;

-- Total vendido por commodity
SELECT commodity_code, SUM(quantidade) AS total_vendido
FROM bronze_sales_commodities_sql
GROUP BY commodity_code
ORDER BY total_vendido DESC;
```

---

## **Desafio final**

show! aqui vai um texto pronto, em linguagem de negócio, pra você colar no README e explicar suas **tabelas GOLD**.

---

# Visão de Negócio – Camada GOLD

## 1) `gold_last7_assets`

**O que é:** visão diária, por ativo, dos **últimos 7 dias** de operação. Mostra volume financeiro, fluxo líquido e número de transações por ativo, mesmo quando um dia não teve movimento (fica 0).

**Para que serve:**

* Acompanhar desempenho **recente** por ativo (BTC-USD, GC=F, CL=F, SI=F).
* Medir **tendência semanal** e apoiar decisões táticas (rebalanceamentos, campanhas, limites).
* Base simples para card de “**como fechou o dia**” no dashboard.

**Grão (grain):** 1 linha por **(data, ativo)**.
**Período coberto:** últimos 7 dias (rolling).
**Fonte:** `silver_sales_enriched` (transações já normalizadas e precificadas).
**Atualização:** recomendada diária (D+0) ou intradiária conforme a coleta de cotações.

**Colunas (definições de negócio):**

* `data` (DATE): dia calendário.
* `ativo` (TEXT): símbolo normalizado (ex.: `BTC-USD`, `GC=F`, `CL=F`, `SI=F`).
* `volume_gross_usd` (NUMERIC): **somatório do notional absoluto** do dia (VENDA e COMPRA entram como positivos).
* `fluxo_liquido_usd` (NUMERIC): **VENDA – COMPRA** em US\$ (Compras entram negativas, Vendas positivas).
* `transacoes` (INTEGER): quantidade de ordens no dia para o ativo.

**Exemplos de uso:**

* “Qual ativo mais movimentou nos últimos 7 dias?”
* “O fluxo líquido do BTC na semana está positivo ou negativo?”
* “Houve queda de atividade (nº de transações) em algum dia?”

**Exemplos de perguntas respondidas:**

* Top 1 ativo por **volume** ontem.
* Evolução do **fluxo líquido** do CL=F ao longo da semana.
* **Heatmap** de transações por ativo × dia.

**Regras/limitações importantes:**

* Considera só dias do calendário; se quiser **dias úteis**, ajustar a geração de datas.
* Preços vêm da camada silver com join “as-of/backward” (último preço ≤ hora), evitando uso de preço futuro.
* Se não houver transação no dia/ativo, os valores ficam **0** (linha existe por consistência de grade).

---

## 2) `gold_kpi_by_customer`

**O que é:** KPIs **consolidados por cliente** no período completo disponível (baseada na enriched).

**Para que serve:**

* Identificar **clientes chave** por **volume** e por **resultado líquido**.
* Suporte a **CRM/CS/Vendas** (priorização de atendimento, ofertas por comportamento).
* Base para ranking de clientes e análise de concentração.

**Grão (grain):** 1 linha por **cliente**.
**Período coberto:** todo o histórico carregado na `silver_sales_enriched` (pode ser filtrado por data no consumo).
**Fonte:** `silver_sales_enriched` (join com `bronze_customers` pelo `customer_id`).
**Atualização:** diária (D+0) após enrichment.

**Colunas (definições de negócio):**

* `customer_id` (TEXT): identificador do cliente.
* `customer_name` (TEXT): nome de exibição do cliente.
* `volume_gross_usd` (NUMERIC): **somatório do notional absoluto** no período (intensidade de relacionamento).
* `fluxo_liquido_usd` (NUMERIC): **VENDA – COMPRA** ao longo do período (proxy de “resultado” operacional da carteira do cliente).
* `transacoes` (INTEGER): quantidade total de ordens do cliente.

**Exemplos de uso:**

* “Top 10 clientes por **volume** no mês.”
* “Quem mais **ganhou/perdeu** (fluxo líquido) no trimestre?”
* “Distribuição de **nº de transações** por cliente (cauda longa).”

**Exemplos de perguntas respondidas:**

* **Quem mais ganhou** e **quem mais perdeu**: ordenar por `fluxo_liquido_usd` desc/asc.
* Qual cliente tem **maior engajamento** (transações) vs **maior volume**.
* **Concentração** de receita/volume (ex.: % Top 5).

**Regras/limitações importantes:**

* `fluxo_liquido_usd` depende do sentido da operação: VENDA (+), COMPRA (−).
* Para análises sazonais, **filtrar por `data_dia`** na `silver_sales_enriched` antes de agregar (ex.: mês corrente).
* Clientes sem transação não aparecem (podem ser incluídos via outer join com `bronze_customers` se necessário).