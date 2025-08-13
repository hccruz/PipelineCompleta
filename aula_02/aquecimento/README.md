# Aquecimento de SQL (15 min)

## O que é SQL (rapidinho)

SQL (*Structured Query Language*) é a linguagem padrão para trabalhar com **bancos relacionais**. É **declarativa**: você diz *o que quer* (o resultado), e o banco decide *como fazer*.

### Famílias de comandos

* **DDL** (definir estrutura): `CREATE`, `ALTER`, `DROP`
* **DML** (manipular dados): `INSERT`, `UPDATE`, `DELETE`
* **DQL** (consultar dados): `SELECT` (+ `WHERE`, `ORDER BY`, `GROUP BY`, `JOIN`, `LIMIT`, …)
* **DCL/TCL** (permissões/transações): `GRANT`, `COMMIT`, `ROLLBACK` (não usamos no aquecimento)

---

## 1) Criando a tabela (DDL)

```sql
-- Tabela simples para “popularidade de ferramentas de dados” em 2025
DROP TABLE IF EXISTS ferramentas_dados;

CREATE TABLE ferramentas_dados (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    categoria       VARCHAR(50),
    popularidade    INT CHECK (popularidade BETWEEN 0 AND 100),
    ano             INT NOT NULL DEFAULT 2025
);
```

**Por quê assim?**

* `SERIAL PRIMARY KEY`: id auto-incremento
* `CHECK (0–100)`: garante popularidade válida
* `ano`: fixamos 2025 (tema do aquecimento)

---

## 2) Inserindo dados (DML)

> Mantendo sua lista, **acrescentando** `n8n = 92` e `Python = 99`.
> A ordem é crescente de popularidade, culminando em **SQL = 100**.

```sql
INSERT INTO ferramentas_dados (nome, categoria, popularidade, ano) VALUES
('Talend', 'ETL', 5, 2025),
('Pentaho', 'ETL', 10, 2025),
('Matillion', 'ETL', 15, 2025),
('Apache NiFi', 'ETL', 18, 2025),
('Informatica PowerCenter', 'ETL', 20, 2025),
('Apache Flink', 'Streaming', 25, 2025),
('Luigi', 'Orquestração', 30, 2025),
('Apache Storm', 'Streaming', 35, 2025),
('Singer', 'ELT', 40, 2025),
('Prefect', 'Orquestração', 45, 2025),
('Airbyte', 'ELT', 50, 2025),
('Apache Beam', 'Streaming', 55, 2025),
('Dagster', 'Orquestração', 60, 2025),
('AWS Glue', 'ETL', 70, 2025),
('Fivetran', 'ELT', 75, 2025),
('dbt', 'Transformação', 80, 2025),
('Kafka', 'Streaming', 85, 2025),
('Airflow', 'Orquestração', 90, 2025),
('n8n', 'Orquestração', 92, 2025),
('Power BI', 'Visualização', 95, 2025),
('Python', 'Linguagem', 99, 2025),
('SQL', 'Linguagem', 100, 2025);
```

---

## 3) Consultas básicas (DQL)

### 3.1 SELECT — ver dados

```sql
-- Tudo
SELECT * FROM ferramentas_dados;

-- Algumas colunas
SELECT nome, categoria, popularidade FROM ferramentas_dados;
```

### 3.2 WHERE — filtrar linhas

```sql
-- Ferramentas de ETL
SELECT * FROM ferramentas_dados
WHERE categoria = 'ETL';

-- Populares (>= 80)
SELECT nome, popularidade
FROM ferramentas_dados
WHERE popularidade >= 80;
```

### 3.3 ORDER BY — ordenar resultados

```sql
-- Do mais popular para o menos
SELECT nome, categoria, popularidade
FROM ferramentas_dados
ORDER BY popularidade DESC;
```

### 3.4 LIMIT — limitar quantidade

```sql
-- Top 5 por popularidade
SELECT nome, popularidade
FROM ferramentas_dados
ORDER BY popularidade DESC
LIMIT 5;
```

### 3.5 DISTINCT — valores únicos

```sql
-- Quais categorias existem?
SELECT DISTINCT categoria
FROM ferramentas_dados
ORDER BY categoria;
```

### 3.6 LIKE / ILIKE — busca por padrão (ILIKE ignora maiúsculas/minúsculas no Postgres)

```sql
-- Ferramentas cujo nome contém 'Apache'
SELECT *
FROM ferramentas_dados
WHERE nome ILIKE '%Apache%';
```

### 3.7 IN — múltiplos valores

```sql
-- Filtrar por um conjunto de categorias
SELECT nome, categoria, popularidade
FROM ferramentas_dados
WHERE categoria IN ('Orquestração', 'ELT', 'ETL');
```

### 3.8 BETWEEN — intervalos

```sql
-- Popularidade entre 70 e 95
SELECT nome, popularidade
FROM ferramentas_dados
WHERE popularidade BETWEEN 70 AND 95
ORDER BY popularidade DESC;
```

---

## 4) (Bônus rápido) UPDATE e DELETE (DML)

```sql
-- UPDATE: corrigir uma categoria (exemplo)
UPDATE ferramentas_dados
SET categoria = 'Orquestração'
WHERE nome = 'Airflow';

-- DELETE: remover um registro (exemplo)
DELETE FROM ferramentas_dados
WHERE nome = 'Pentaho';
```

> 💡 Dica didática: Rodar `SELECT *` antes e depois do `UPDATE/DELETE` para ver o efeito.

---

## 5) Mini-desafios (2 minutos cada)

* **Top 3** mais populares com categoria.
* Todas as ferramentas com nome começando por “A”.
* Média de popularidade por **categoria**:

  ```sql
  SELECT categoria, ROUND(AVG(popularidade),2) AS media_pop
  FROM ferramentas_dados
  GROUP BY categoria
  ORDER BY media_pop DESC;
  ```

---

### Conexão com o restante do curso

* Você acabou de usar **DDL** (criar tabela) e **DML** (inserir/atualizar/apagar) e **DQL** (consultar).
* Na próxima parte, repetimos esses fundamentos nas suas bases **Bronze → Silver → Gold** (joins, agregações, normalização), para chegar aos **KPIs** de negócio.

Se quiser, organizo isso num **README** com seções e “caixas de código” já formatadas para o repositório da aula.
