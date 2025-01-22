from config.get_config import config_data
from data_access.read_db import get_table_creation_statements, get_rows_from_all_tables, get_table_and_column_comments
from llm_access.call_llm_test import call_llm
from utils.output_parsing.parse_output import parse_sql_code

tries = config_data['ai']['tries']


def get_sql_code(question, llm, retries=tries):
    retries_times = 0
    result_sql = None
    # print(get_table_creation_statements())
    # print(get_table_and_column_comments())
    # print(get_foreign_keys())
    while retries_times <= retries:
        retries_times += 1
        ans = call_llm(question + "\nPlease write sql to select the data needed, "
                                + "Here is the structure of the database:\n"
                       + str(get_table_creation_statements())
                       + "Here is the table and column comments:\n"
                       + str(get_table_and_column_comments())
                       + "Here is data samples(just samples, do not mock any data):\n"
                       + str(get_rows_from_all_tables(num=3))
                       + """
                              code should only be in md code blocks: 
                                ```sql
                                    # some sql code
                                ```
                              """, llm)
        result_sql = parse_sql_code(ans.content)
        if result_sql is None:
            continue
        else:
            return result_sql
