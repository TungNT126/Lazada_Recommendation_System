import pandas as pd
import pymysql
from sqlalchemy import create_engine

host = "localhost"
user = "root"
password = "123456"
database = "lazada"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

file_path = "cleaned.csv"
df = pd.read_csv(file_path)

df.to_sql(name="products", con=engine, if_exists="replace", index=False)

print("Dữ liệu cập nhật thành công")