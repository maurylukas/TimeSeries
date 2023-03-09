import pandas as pd
import yfinance as yf
from prefect import task, flow

@task(
    name="Extract BTC prices",
    retries=3,
    retry_delay_seconds=3
)
def extract_btc_prices(tickers: str, period: str, interval: str) -> pd.DataFrame:
    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval
    )
    return data

@task(
    name="Transform"
)
def transform(data: pd.DataFrame) -> pd.DataFrame:
    return data

@task(
    name="Save BTC prices as CSV"
)
def load_btc_prices(data: pd.DataFrame, path: str) -> None:
    data.to_csv(path_or_buf=path, index=True)

@flow(
    name="BTC price pipeline"
)
def main_flow(tickers: str, period: str, interval: str, path: str):
    print(">>> Extracting BTC prices <<<")
    df = extract_btc_prices(tickers=tickers, period=period, interval=interval)
    print(">>> Transforming <<<")
    df = transform(df)
    print(">>> Storing BTC prices <<<")
    load_btc_prices(
        data=df,
        path=path
    )

if __name__ == "__main__":
    main_flow(
        tickers="BTC-USD",
        period="3h",
        interval="5m",
        path=r'./Data/btc_prices.csv'
    )