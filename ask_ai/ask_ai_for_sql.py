from data_access.read_db import get_table_creation_statements
from llm_access.call_llm_test import call_llm
from utils.output_parsing.parse_output import parse_sql_code


def get_sql_code(question, llm, retries=3):
    table_struct = get_table_creation_statements()
    retries_times = 0
    result_sql = None
    while retries_times <= retries:
        retries_times += 1
        ans = call_llm(question + "please write sql to select the data needed, "
                                  "here is the structure of the database:"
                       + str(table_struct) + """
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

