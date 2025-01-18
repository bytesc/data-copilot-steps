from data_access.read_db import execute_sql, execute_select
from data_access.db_conn import engine
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Integer

# 读取CSV文件
csv_file_path = '../../data-source/Data-Copilot/Data-Copilot/CityPlanning/BusStop_converted.csv'


df = pd.read_csv(csv_file_path)

# 定义数据库表的名称
table_name = 'BusStop'

# 创建表结构（如果尚不存在）
metadata = MetaData()
table = Table(
    table_name, metadata,
    Column('X', Float()),
    Column('Y', Float()),
    Column('bus_stop_n', String(255)),
    Column('loc_desc', String(255)),
)

# 创建表（如果不存在）
metadata.create_all(engine)


# 准备插入数据的SQL语句
insert_query = f'INSERT INTO {table_name} (X, Y,bus_stop_n,loc_desc) VALUES (%s, %s,"%s", "%s")'

# 插入数据
for index, row in df.iterrows():
    if 1:
        sql = insert_query % (row['X'], row['Y'],row['BUS_STOP_N'], row['LOC_DESC'])
        execute_sql(sql)

print("Data has been written to the database.")

