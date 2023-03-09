import pandas as pd
import yfinance as yf
from prefect import task, flow

@task
def extract_btc_prices() -> pd.DataFrame:
    data = yf.download(
        tickers="BTC-USD",
        period="3h",
        interval="5m"
    )
    return data

@task
def transform(data: pd.DataFrame) -> pd.DataFrame:
    return data

@task
def load_btc_prices(data: pd.DataFrame, path: str) -> None:
    data.to_csv(path_or_buf=path, index=True)

@flow
def main_flow(log_prints=True):
    print(">>> Extracting BTC prices <<<")
    df = extract_btc_prices()
    print(">>> Transforming <<<")
    df = transform(df)
    print(">>> Storing BTC prices <<<")
    load_btc_prices(
        data=df,
        path=r'./Data/btc_prices.csv'
    )

if __name__ == "__main__":
    main_flow()