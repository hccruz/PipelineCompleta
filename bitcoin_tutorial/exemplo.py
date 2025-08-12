import requests
import pandas as pd
from datetime import datetime

# URL da API da Coinbase para o preço spot do Bitcoin
url = "https://api.coinbase.com/v2/prices/spot"

# Requisição GET
response = requests.get(url)
data = response.json()

# Extrair dados relevantes
amount = float(data['data']['amount'])
base = data['data']['base']
currency = data['data']['currency']
timestamp = datetime.now()

# Criar DataFrame
df = pd.DataFrame([{
    'timestamp': timestamp,
    'base': base,
    'currency': currency,
    'amount': amount
}])

print(df)

# Salvar em CSV
df.to_csv('cotacao_bitcoin.csv', index=False)

print("✅ Cotação do Bitcoin salva em cotacao_bitcoin.csv")
