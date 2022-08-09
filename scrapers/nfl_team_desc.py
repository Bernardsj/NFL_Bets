# Script to updated local mysql db with weekly nfl data from nfl_data_py 
import nfl_data_py as nfl
import pandas as pd
import numpy as np

# pull data
df_team_desc = nfl.import_team_desc(2022)

# Push data to MySQL database
## Connect to DB
from sqlalchemy import create_engine
engine = create_engine("mysql://root:eK5ERE<Sqv+j[0o@localhost/nfl_bets")

# Push scraped data
df_team_desc(con = engine, name = 'team_desc', if_exists='append',index=False)