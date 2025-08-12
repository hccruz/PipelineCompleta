import yfinance as yf

# Ouro (futuro)
ticker = yf.Ticker('GC=F')

# Buscar últimos dados do dia no intervalo de 1 minuto
df = ticker.history(period='1d', interval='1m')[['Close']]

# Pegar somente a última linha
ultimo_df = df.tail(1)

# Salvar no CSV
ultimo_df.to_csv('cotacao_ouro.csv', index_label='Date')

print("✅ Última cotação salva em cotacao_ouro.csv")
