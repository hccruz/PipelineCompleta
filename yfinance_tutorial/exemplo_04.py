# exemplo_04.py
import yfinance as yf
import pandas as pd
from datetime import datetime

def get_ouro_df() -> pd.DataFrame:
    ultimo_df = yf.Ticker('GC=F').history(period='1d', interval='1m')[['Close']].tail(1)
    ultimo_df = ultimo_df.rename(columns={'Close': 'preco'})
    ultimo_df['ativo'] = 'GC=F'
    ultimo_df['moeda'] = 'USD'
    ultimo_df['horario_coleta'] = datetime.now()
    ultimo_df = ultimo_df[['ativo', 'preco', 'moeda', 'horario_coleta']]
    return ultimo_df

if __name__ == "__main__":
    df = get_ouro_df()
    print(df)
