# GetCommoditiesBitcoin_2024_1h.py
import pandas as pd
import yfinance as yf
from datetime import datetime, timezone
from pathlib import Path

SYMBOLS = ["GC=F", "CL=F", "SI=F", "BTC-USD"]
MOEDA = "USD"
START = "2024-01-01"
END = "2025-12-31"  # ou datetime.now().strftime("%Y-%m-%d")
INTERVAL = "1h"
OUT_CSV = Path("bronze_prices_2024_2025_1h.csv")

def _extract_close(raw: pd.DataFrame, symbol: str) -> pd.Series:
    if raw.empty:
        return pd.Series(dtype="float64")
    if not isinstance(raw.columns, pd.MultiIndex):
        return raw["Close"] if "Close" in raw.columns else pd.Series(dtype="float64")
    if "Close" in raw.columns.get_level_values(-1):
        close_df = raw.xs("Close", level=-1, axis=1)
        return close_df[symbol] if symbol in close_df.columns else close_df.iloc[:, 0]
    if "Close" in raw.columns.get_level_values(0):
        close_df = raw.xs("Close", level=0, axis=1)
        return close_df[symbol] if symbol in close_df.columns else close_df.iloc[:, 0]
    flat_cols = ["_".join([str(p) for p in tup if p is not None]) for tup in raw.columns]
    raw.columns = flat_cols
    candidates = [c for c in raw.columns if c.endswith("_Close") or c == "Close"]
    return raw[candidates[0]] if candidates else pd.Series(dtype="float64")

def get_assets_df() -> pd.DataFrame:
    all_rows = []
    coleta_ts = datetime.now(timezone.utc)
    for sym in SYMBOLS:
        print(f"Baixando {sym}...")
        raw = yf.download(
            tickers=sym,
            start=START,
            end=END,
            interval=INTERVAL,
            progress=False,
            group_by="column",
            auto_adjust=False,
            threads=False,
        )
        close = _extract_close(raw, sym)
        if close.empty:
            print(f"⚠️  Sem dados para {sym}.")
            continue
        df = close.to_frame("preco")
        df["ativo"] = sym
        df["moeda"] = MOEDA
        df["horario_coleta"] = coleta_ts
        all_rows.append(df[["ativo", "preco", "moeda", "horario_coleta"]].reset_index(drop=True))
    return pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame(columns=["ativo", "preco", "moeda", "horario_coleta"])

if __name__ == "__main__":
    df_final = get_assets_df()
    df_final.to_csv(OUT_CSV, index=False)
    print(f"✅ Arquivo gerado: {OUT_CSV.resolve()} com {len(df_final)} linhas")
