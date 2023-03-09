import pandas as pd
import yfinance as yf

def extract_btc_prices() -> pd.DataFrame:
    data = yf.download(
        tickers="BTC-USD",
        period="3h",
        interval="5m"
    )
    return data

def transform(data: pd.DataFrame) -> pd.DataFrame:
    return data

def load_btc_prices(data: pd.DataFrame, path: str) -> None:
    data.to_csv(path_or_buf=path, index=True)
    
if __name__ == "__main__":
    df = extract_btc_prices()
    df = transform(df)
    load_btc_prices(data=df, path=r'./Data/btc_prices.csv')