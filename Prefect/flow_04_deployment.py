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
    print(f">>> Successfully saved here: {path} <<<")
    
if __name__ == "__main__":
    main_flow(
        tickers="BTC-USD",
        period="3h",
        interval="5m",
        path=r'./Data/btc_prices.csv'
    )


# TESTING
#   python Prefect/flow_04_deployment.py

# DEPLOYMENT STEPS & CLI COMMANDS:
# 1. BUILD:
#   prefect deployment build ./Prefect/flow_04_deployment.py:main_flow --name btc_flow --interval 60
# 2. MANUALLY ADD PARAMETERS IN YAML FILE:
# path: '/Users/anapa/OneDrive/Documentos/GitHub/TimeSeries/Data/btc_prices.csv'
# 3. APPLY:
#   prefect deployment apply main_flow-deployment.yaml
# 4. LIST DEPLOYMENTS:
#   prefect deployment ls
# 5. RUN:
#   prefect deployment run "BTC price pipeline/btc_flow"
# 6. ORION GUI:
#   prefect orion start
# 7. AGENT START:
#   prefect agent start --work-queue "default"
# 8. EXIT:
# Hold CTRL and press C
