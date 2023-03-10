library(modeltime)
library(tidymodels)
library(timetk)
library(tidyverse)

btc_prices_tbl <- read_csv("./Data/btc_prices.csv")

btc_prices_tbl %>%
    plot_time_series(Datetime, `Adj Close`)

data_prepared_tbl <- btc_prices_tbl %>%
    select(Datetime, `Adj Close`)

splits <- time_series_split(
    data_prepared_tbl,
    assess = 5,
    cumulative = TRUE
)

splits

wflw_fit <- workflow() %>%
    add_model(
        arima_reg() %>% set_engine("auto_arima")
    ) %>%
    add_recipe(
        recipe = recipe(`Adj Close` ~ `Datetime`, training(splits))
    ) %>%
    fit(training(splits))

model_tbl <- modeltime_table(wflw_fit)

calib_tbl <- model_tbl %>%
    modeltime_calibrate(testing(splits))

acc_tbl <- modeltime_accuracy(calib_tbl)

acc_tbl

acc_tbl %>% table_modeltime_accuracy()

test_forecast_tbl <- calib_tbl %>%
    modeltime_forecast(
        new_data = testing(splits),
        actual_data = data_prepared_tbl
    )

test_forecast_tbl %>% plot_modeltime_forecast()

future_forecast_tbl <- calib_tbl %>%
    modeltime_refit(data_prepared_tbl) %>%
    modeltime_forecast(
        h = 6,
        actual_data = data_prepared_tbl
    )

tail(future_forecast_tbl)

future_forecast_tbl %>% plot_modeltime_forecast()

future_forecast_tbl %>%
    select(.index:.conf_hi) %>%
    set_names(
        c("Datetime", "Adj Close", "Lower Bound", "Upper Bound")
    ) %>%
    write.csv("./Data/btc_prices_forecast.csv")
