# exemplo_05.py
import yfinance as yf
import pandas as pd
from datetime import datetime

def get_commodities_df() -> pd.DataFrame:
    symbols = ["GC=F", "CL=F", "SI=F"]
    dfs = []
    for sym in symbols:
        ultimo_df = yf.Ticker(sym).history(period='1d', interval='1m')[['Close']].tail(1)
        ultimo_df = ultimo_df.rename(columns={'Close': 'preco'})
        ultimo_df['ativo'] = sym
        ultimo_df['moeda'] = 'USD'
        ultimo_df['horario_coleta'] = datetime.now()
        ultimo_df = ultimo_df[['ativo', 'preco', 'moeda', 'horario_coleta']]
        dfs.append(ultimo_df)
    return pd.concat(dfs, ignore_index=True)

if __name__ == "__main__":
    df = get_commodities_df()
    print(df)
