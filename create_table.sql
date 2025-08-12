CREATE TABLE IF NOT EXISTS public.cotacoes (
  id              BIGSERIAL PRIMARY KEY,
  ativo           TEXT NOT NULL,           -- Ex.: BTC-USD, GC=F, CL=F, SI=F
  preco           NUMERIC(18,6) NOT NULL,  -- Preço coletado
  moeda           CHAR(3) NOT NULL DEFAULT 'USD',
  horario_coleta  TIMESTAMPTZ NOT NULL,    -- Quando o script coletou
  inserido_em     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
