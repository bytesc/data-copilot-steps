import os

import pandas as pd
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from ask_ai.ask_ai_for_echart import get_ask_echart_file_prompt, get_ask_echart_block_prompt
from ask_ai.ask_ai_for_graph import get_ask_graph_prompt
from ask_ai.ask_ai_for_sql import get_sql_code
from ask_ai.ask_python import get_final_prompt, get_py_code
from ask_ai.input_process import get_chart_type
from config.get_config import config_data
from data_access.read_db import execute_select, get_all_table_names, get_rows_from_all_tables
from llm_access import call_llm_test
from llm_access.LLM import get_llm
from llm_access.call_llm_test import call_llm
from utils.exe.code_executor import execute_code
from utils.output_parsing import parse_output

from pywebio.input import input, TEXT, actions, textarea
from pywebio.output import put_html, put_text, put_table, put_markdown, put_image, put_code, put_loading, put_collapse, \
    toast, put_info
from pywebio import start_server


class AskRequest(BaseModel):
    question: str
    concurrent: int
    retries: int


llm = get_llm()


def main():
    put_markdown("# DATA COPILOT")
    # put_info("示例问题：\n"
    #          "统计房价数据最多的10个区的数据数量比例\n"
    #          "统计平均房价最高的三个区域的平均房价变化情况，2000-2020\n"
    #          "列出距离LORONG 7 TOA PAYOH最近的5个车站的名字和距离")

    table_names = get_all_table_names()
    # put_text("数据库：")
    # put_table([table_names])

    first_five_rows = get_rows_from_all_tables()
    # print(first_five_rows)
    with put_collapse(f"数据表："):
        for table_name, rows in first_five_rows.items():
            with put_collapse(f"表 {table_name}"):
                put_text(f"表 {table_name} 的前5行数据:")
                put_table([rows.columns.tolist()] + rows.values.tolist())

    while 1:
        question = textarea("请输入你的问题：", required=True)
        ask_request = AskRequest(question=question, concurrent=1, retries=3)
        put_text("你的问题：" + question)

        # 生成 SQL 代码
        with put_loading():
            sql_code = get_sql_code(ask_request.question, llm)
        # put_text("生成的 SQL 代码：")
        # put_text(sql_code)

        while 1:
            sql_code = textarea("请编辑 SQL 代码并确认执行：", value=sql_code, rows=10, code=True)
            put_text("执行 SQL 代码：")
            put_code(sql_code, language="sql")
            mid_notes = ""

            # 执行 SQL 查询
            with put_loading():
                ans_pd = execute_select(sql_code)
            if isinstance(ans_pd, pd.DataFrame):
                put_text("查询结果：")
                if len(ans_pd) > 100:
                    put_text("数据超过100行，仅显示前100行")
                    ans_pd = ans_pd.head(100)
                if not ans_pd.empty:
                    html = f"""
                           <div style="min-height: 200px; max-height: 400px; overflow-y: auto;">
                               {ans_pd.to_html(index=False)}
                           </div>
                           """
                    put_html(html)
                else:
                    put_text("查询结果为空\n")
            elif isinstance(ans_pd, SQLAlchemyError):
                put_text(f"查询失败，错误类型：{type(ans_pd).__name__}，错误信息：{str(ans_pd)}")
                mid_notes = "Code:\n```sql\n" + sql_code + "\n```\nError: " + str(ans_pd)
            else:
                put_text("未知错误，查询失败。")

            # 让用户选择是否接受结果或重新查询
            if isinstance(ans_pd, pd.DataFrame) and not ans_pd.empty:
                user_choice = actions("请选择：", [
                    {'label': '继续', 'value': 'accept', "color": "success"},
                    {'label': '重新编辑 SQL', 'value': 'retry'},
                    {'label': '重新生成 SQL', 'value': 'regen'}
                ])
            else:
                user_choice = actions("请选择：", [
                    {'label': '重新编辑 SQL', 'value': 'retry'},
                    {'label': '重新生成 SQL', 'value': 'regen'}
                ])

            if user_choice == 'accept':
                break  # 用户接受结果，跳出循环
            elif user_choice == 'retry':
                continue  # 用户选择重新编辑 SQL 代码
            elif user_choice == 'regen':
                mid_notes = textarea("请输入补充提示（如果需要）：", type=TEXT, value=mid_notes)
                with put_loading():
                    sql_code = get_sql_code(ask_request.question + mid_notes, llm)
                continue

        # print(ans_pd)

        # 获取图表类型
        with put_loading():
            graph_type = get_chart_type(ask_request.question, llm)
        edited_graph_type = input("请编辑图表类型（如果需要）：", type=TEXT, value=graph_type)
        if edited_graph_type.strip():
            graph_type = edited_graph_type

        ask_request.question = ask_request.question + graph_type

        draw_graph_prompt = get_ask_echart_block_prompt(ask_request)

        with put_loading():
            ans_code = get_py_code(ans_pd, ask_request.question + draw_graph_prompt, llm)

        while 1:
            ans_code = textarea("请编辑代码：", value=ans_code, rows=10, code=True)
            put_code(ans_code, language="python")
            mid_notes = ""
            try:
                result = execute_code(ans_code, ans_pd)
                put_html(result)
            except Exception as e:
                put_text(f"代码执行失败，错误信息：{str(e)}")
                mid_notes = "Code:\n```python\n" + ans_code + "\n```\nError: " + str(e)
            user_choice = actions("请选择：", [
                {'label': '继续', 'value': 'accept', "color": "success"},
                {'label': '重新编辑 Python', 'value': 'retry'},
                {'label': '重新生成 Python', 'value': 'regen'}
            ])
            if user_choice == 'accept':
                break
            elif user_choice == 'retry':
                continue
            elif user_choice == 'regen':
                mid_notes = textarea("请输入补充提示（如果需要）：", type=TEXT, value=mid_notes)
                with put_loading():
                    ans_code = get_py_code(ans_pd, ask_request.question + draw_graph_prompt + mid_notes, llm)
                continue


if __name__ == '__main__':
    start_server(main, port=config_data["server_port"])
