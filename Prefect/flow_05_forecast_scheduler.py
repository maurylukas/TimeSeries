import pandas as pd
import yfinance as yf
from prefect import task, flow

from modeltime_forecast import make_modeltime_forecast
from multiprocessing import Process

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

@task(
    name="Forecast BTC prices"
)
def load_btc_forecasts(path1: str, path2: str) -> None:
    r_process = Process(
        target=make_modeltime_forecast,
        kwargs=dict(path1=path1, path2=path2)
    )
    r_process.start()

@flow(
    name="BTC price pipeline"
)
def main_fc_flow(tickers: str, period: str, interval: str, path1: str, path2: str):
    print(">>> Extracting BTC prices <<<")
    df = extract_btc_prices(tickers=tickers, period=period, interval=interval)
    print(">>> Transforming <<<")
    df = transform(df)
    print(">>> Storing BTC prices <<<")
    load_btc_prices(
        data=df,
        path=path1
    )
    print(f">>> Successfully saved here: {path1} <<<")
    print(f">>> Forecasting BTC prices <<<")
    load_btc_forecasts(
        path1=path1,
        path2=path2
    )
    print(f">>> Successfully saved here: {path2} <<<")
    
if __name__ == "__main__":
    main_fc_flow(
        tickers="BTC-USD",
        period="30d",
        interval="5m",
        path1=r'./Data/btc_prices.csv',
        path2=r'./Data/btc_prices_forecast.csv'
    )


# TESTING
#   python Prefect/flow_05_forecast_scheduler.py

# DEPLOYMENT STEPS & CLI COMMANDS:
# 1. BUILD:
#   prefect deployment build ./Prefect/flow_05_forecast_scheduler.py:main_fc_flow --name btc_fc_flow --interval 60
# 2. MANUALLY ADD PARAMETERS IN YAML FILE:
# path1: '/Users/anapa/OneDrive/Documentos/GitHub/TimeSeries/Data/btc_prices.csv'
# path2: '/Users/anapa/OneDrive/Documentos/GitHub/TimeSeries/Data/btc_prices_forecast.csv'
# 3. APPLY:
#   prefect deployment apply main_fc_flow-deployment.yaml
# 4. LIST DEPLOYMENTS:
#   prefect deployment ls
# 5. RUN:
#   prefect deployment run "BTC price pipeline/btc_fc_flow"
# 6. ORION GUI:
#   prefect orion start
# 7. AGENT START:
#   prefect agent start --work-queue "default"
# 8. EXIT:
# Hold CTRL and press C
