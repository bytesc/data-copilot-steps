from data_access.read_db import execute_sql, execute_select
from data_access.db_conn import engine
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Integer

# 读取CSV文件
csv_file_path = '../../data-source/ResaleFlatPrices 2/ResaleFlatPrices/Resale Flat Prices (Based on Registration Date), From Jan 2015 to Dec 2016.csv'
#Resale Flat Prices (Based on Registration Date), From Jan 2015 to Dec 2016.csv
#Resale Flat Prices (Based on Registration Date), From Mar 2012 to Dec 2014.csv
#Resale flat prices based on registration date from Jan-2017 onwards.csv
#

df = pd.read_csv(csv_file_path)

# 定义数据库表的名称
table_name = 'Resale_Flat_Prices'

# 创建表结构（如果尚不存在）
metadata = MetaData()
table = Table(
    table_name, metadata,
    Column('month', String(255)),
    Column('town', String(255)),
    Column('flat_type', String(255)),
    Column('blk_no', String(255)),
    Column('street', String(255)),
    Column('storey_range', String(255)),
    Column('floor_area_sqm', Float()),
    Column('flat_model', String(255)),
    Column('lease_commence_date', Integer()),
    Column('resale_price', Integer()),
)

# 创建表（如果不存在）
metadata.create_all(engine)


# 准备插入数据的SQL语句
insert_query = f'INSERT INTO {table_name} (month, town,flat_type,blk_no, street,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) VALUES ("%s", "%s", "%s","%s", "%s","%s", %s,"%s", %s, %s)'

# 插入数据
for index, row in df.iterrows():
    if 1:
        sql = insert_query % (row['month'], row['town'],row['flat_type'], row['block'],
                              row['street_name'], row['storey_range'],
                              int(row['floor_area_sqm']), row['flat_model'],
                              int(row['lease_commence_date']),int(row['resale_price']))
        execute_sql(sql)

print("Data has been written to the database.")

