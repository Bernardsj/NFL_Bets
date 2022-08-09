# Script to updated local mysql db with weekly nfl data from nfl_data_py 
import nfl_data_py as nfl
import pandas as pd
import numpy as np

# pull data
df_qbr = nfl.import_qbr(2022)
df_qbr.rename(columns={'rank':'qb_rank'})

# Push data to MySQL database
## Connect to DB
from sqlalchemy import create_engine
engine = create_engine("mysql://root:eK5ERE<Sqv+j[0o@localhost/nfl_bets")

# Push scraped data
df_qbr(con = engine, name = 'schedules', if_exists='append',index=False)
