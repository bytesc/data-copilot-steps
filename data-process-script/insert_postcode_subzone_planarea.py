from data_access.read_db import execute_sql, execute_select
from data_access.db_conn import engine
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String


# 读取CSV文件
csv_file_path = '../../data-source/postcode/postcode_subzone_planarea.csv'
df = pd.read_csv(csv_file_path)

# 定义数据库表的名称
table_name = 'postcode_subzone_planarea'


# 创建表结构（如果尚不存在）
metadata = MetaData()
table = Table(
    table_name, metadata,
    Column('PostCode', String(31)),
    Column('subzone', String(255)),
    Column('planarea', String(255))
)

# 创建表（如果不存在）
metadata.create_all(engine)


# 准备插入数据的SQL语句
insert_query = f'INSERT INTO {table_name} (PostCode, subzone, planarea) VALUES ("%s", "%s", "%s")'

# 插入数据
for index, row in df.iterrows():
    if str(row["EXCEPTION"]) == "None":
        sql = insert_query % (str(int(row['POSTAL'])), row['SUBZONE_N'], row['PLN_AREA_N'])
        execute_sql(sql)

print("Data has been written to the database.")

