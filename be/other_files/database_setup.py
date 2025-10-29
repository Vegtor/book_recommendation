import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:Admin_pass1@localhost:5432/books2_db"
engine = create_engine(DATABASE_URL)

csv_file = "nova_data/to_read.csv"
df = pd.read_csv(csv_file)


df.to_sql("to_read", engine, if_exists="append", index=False, chunksize=1000)
