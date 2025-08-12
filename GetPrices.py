# GetPrices.py
# Junta Bitcoin + Commodities em um único DataFrame e imprime (uma vez).

import pandas as pd
from GetBitcoin import get_bitcoin_df
from GetCommodities import get_commodities_df

if __name__ == "__main__":
    # Coleta
    df_btc = get_bitcoin_df()
    df_comm = get_commodities_df()

    # Junta tudo
    df = pd.concat([df_btc, df_comm], ignore_index=True)

    # Imprime
    print(df)
