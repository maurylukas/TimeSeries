from rpy2.robjects.packages import importr

modeltime = importr('modeltime')
parsnip = importr('parsnip')
workflows = importr('workflows')
recipes = importr('recipes')
rsample = importr('rsample')
timetk = importr('timetk')
dplyr = importr('dplyr')
readr = importr('readr')
base = importr('base')
stats = importr('stats')
generics = importr('generics')

def make_modeltime_forecast(path1, path2) -> None:
    """Modeltime Forecasting Engine to interface with R via rpy2. Requires:
    - modeltime
    - parsnip
    - workflows
    - recipes
    - rsample
    - timetk
    - dplyr
    - readr
    - base
    - stats
    - generics"""