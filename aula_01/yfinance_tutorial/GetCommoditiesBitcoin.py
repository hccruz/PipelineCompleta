import pandas as pd
import yfinance as yf
from pathlib import Path

SYMBOLS = ["GC=F", "CL=F", "SI=F", "BTC-USD"]
MOEDA = "USD"
START = "2024-01-01"
END_INCLUSIVE = "2025-12-31"
INTERVAL = "1h"
OUT_CSV = Path("data_bronze/bronze_cotacoes.csv")

def end_exclusive(end_inclusive: str) -> str:
    return (pd.Timestamp(end_inclusive, tz="UTC") + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

def ensure_utc(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    return idx.tz_localize("UTC") if idx.tz is None else idx.tz_convert("UTC")

def extract_close(raw: pd.DataFrame, symbol: str) -> pd.Series:
    if raw.empty:
        return pd.Series(dtype="float64")
    if isinstance(raw.columns, pd.MultiIndex):
        # tenta Close no último nível
        if "Close" in raw.columns.get_level_values(-1):
            df = raw.xs("Close", level=-1, axis=1)
            return df.get(symbol, df.iloc[:, 0])
        # tenta Close no primeiro nível
        if "Close" in raw.columns.get_level_values(0):
            df = raw.xs("Close", level=0, axis=1)
            return df.get(symbol, df.iloc[:, 0])
        # fallback: achata colunas e pega *_Close
        flat = ["_".join([str(x) for x in t if x is not None]) for t in raw.columns]
        raw.columns = flat
        cands = [c for c in raw.columns if c.endswith("_Close") or c == "Close"]
        return raw[cands[0]] if cands else pd.Series(dtype="float64")
    return raw["Close"] if "Close" in raw.columns else pd.Series(dtype="float64")

def get_assets_df() -> pd.DataFrame:
    frames = []
    for sym in SYMBOLS:
        print(f"Baixando {sym}…")
        raw = yf.download(
            tickers=sym,
            start=START,
            end=end_exclusive(END_INCLUSIVE),   # END exclusivo no yfinance
            interval=INTERVAL,
            progress=False,
            group_by="column",
            auto_adjust=False,
            threads=False,
        )
        close = extract_close(raw, sym)
        if close.empty:
            print(f"⚠️  Sem dados para {sym}.")
            continue

        # 1) garante UTC no índice  2) não usa now()  3) transforma índice em coluna horário
        close.index = ensure_utc(close.index)
        df = (close
              .to_frame("preco")
              .reset_index(names="horario_coleta"))     # <- pega o timestamp do candle

        # (opcional) normaliza para hora cheia
        df["horario_coleta"] = pd.to_datetime(df["horario_coleta"], utc=True).dt.floor("H")

        df["ativo"] = sym
        df["moeda"] = MOEDA
        df = df.sort_values(["ativo", "horario_coleta"]).drop_duplicates(["ativo", "horario_coleta"], keep="last")
        df = df[["ativo", "preco", "moeda", "horario_coleta"]]
        frames.append(df)

    if not frames:
        return pd.DataFrame(columns=["ativo", "preco", "moeda", "horario_coleta"])
    return pd.concat(frames, ignore_index=True)

if __name__ == "__main__":
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_final = get_assets_df()
    # Verificação rápida antes de salvar (para garantir que horários variam)
    print(df_final.groupby("ativo")["horario_coleta"].agg(["min","max","nunique"]).reset_index().head())
    df_final.to_csv(OUT_CSV, index=False)
    print(f"✅ Gerado: {OUT_CSV.resolve()} ({len(df_final)} linhas)")
