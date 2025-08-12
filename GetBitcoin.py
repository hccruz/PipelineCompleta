# GetBitcoin.py
import requests
import pandas as pd
from datetime import datetime

def get_bitcoin_df() -> pd.DataFrame:
    # URL da API da Coinbase para o preço spot do Bitcoin
    url = "https://api.coinbase.com/v2/prices/spot"

    # Requisição GET
    response = requests.get(url)
    data = response.json()

    # Extrair dados relevantes
    preco = float(data['data']['amount'])
    ativo = data['data']['base']        # "BTC"
    moeda = data['data']['currency']    # "USD"
    horario_coleta = datetime.now()

    # Criar DataFrame no padrão em português
    df = pd.DataFrame([{
        'ativo': ativo,
        'preco': preco,
        'moeda': moeda,
        'horario_coleta': horario_coleta
    }])

    return df

if __name__ == "__main__":
    df = get_bitcoin_df()
    print(df)
    print("✅ Cotação do Bitcoin obtida com sucesso!")