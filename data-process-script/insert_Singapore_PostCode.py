from data_access.read_db import execute_sql, execute_select
from data_access.db_conn import engine
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float

# 读取CSV文件
csv_file_path = '../../data-source/postcode/Singapore_PostCode.csv'
df = pd.read_csv(csv_file_path)

# 定义数据库表的名称
table_name = 'Singapore_PostCode'

# 创建表结构（如果尚不存在）
metadata = MetaData()
table = Table(
    table_name, metadata,
    Column('blk_no', String(255)),
    Column('street', String(255)),
    Column('building', String(255)),
    Column('address', String(255)),
    Column('PostCode', String(31)),
    Column('X', Float()),
    Column('Y', Float()),
    Column('latitude', Float()),
    Column('longitude', Float()),
)

# 创建表（如果不存在）
metadata.create_all(engine)


# 准备插入数据的SQL语句
insert_query = f'INSERT INTO {table_name} (blk_no, street,building,address, PostCode,X,Y,latitude,longitude) VALUES ("%s", "%s", "%s","%s", "%s", %s,%s, %s, %s)'

# 插入数据
for index, row in df.iterrows():
    if 1:
        sql = insert_query % (row['BLK_NO'], row['ROAD_NAME'],row['BUILDING'], row['ADDRESS'],
                              str(int(row['POSTAL'])),
                              row['X'], row['Y'],row['LATITUDE'], row['LATITUDE'])
        execute_sql(sql)

print("Data has been written to the database.")

