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
