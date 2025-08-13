# exemplo_04.py
import yfinance as yf
from datetime import datetime

ultimo_df = yf.Ticker('GC=F').history(period='1d', interval='1m')[['Close']].tail(1)
ultimo_df = ultimo_df.rename(columns={'Close': 'preco'})
ultimo_df['ativo'] = 'GC=F'
ultimo_df['moeda'] = 'USD'
ultimo_df['horario_coleta'] = datetime.now()
ultimo_df = ultimo_df[['ativo', 'preco', 'moeda', 'horario_coleta']]

print(ultimo_df)
