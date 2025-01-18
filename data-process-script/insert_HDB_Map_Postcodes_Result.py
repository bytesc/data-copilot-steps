from data_access.read_db import execute_sql, execute_select
from data_access.db_conn import engine
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String


# 读取CSV文件
csv_file_path = '../../data-source/postcode/HDB_Map_Postcodes_Result.csv'
df = pd.read_csv(csv_file_path)

# 定义数据库表的名称
table_name = 'HDB_Map_Postcodes'

# 创建表结构（如果尚不存在）
metadata = MetaData()
table = Table(
    table_name, metadata,
    Column('blk_no', String(255)),
    Column('street', String(255)),
    Column('PostCode', String(31))
)

# 创建表（如果不存在）
metadata.create_all(engine)


# 准备插入数据的SQL语句
insert_query = f'INSERT INTO {table_name} (blk_no, street, PostCode) VALUES ("%s", "%s", "%s")'

# 插入数据
for index, row in df.iterrows():
    if str(row["exceptions"]) == "nan" and float(row["similarity"])>=90:
        sql = insert_query % (row['matched_blk_no'], row['matched_Road_Name'], str(int(row['matched_PostCode'])))
        execute_sql(sql)

print("Data has been written to the database.")

