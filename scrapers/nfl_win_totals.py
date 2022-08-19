# Script to updated local mysql db with weekly nfl data from nfl_data_py 
import nfl_data_py as nfl
import pandas as pd
import numpy as np

# pull data
df_win_totals = nfl.import_win_totals([2021])

# Push data to MySQL database
## Connect to DB
from sqlalchemy import create_engine
engine = create_engine("mysql://root:eK5ERE<Sqv+j[0o@localhost/nfl_bets")

# Push scraped data
df_win_totals.to_sql(con = engine, name = 'win_totals', if_exists='append',index=False)
