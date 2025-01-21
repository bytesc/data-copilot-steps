import os

import pandas as pd
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from ask_ai.ask_ai_for_echart import get_ask_echart_file_prompt, get_ask_echart_block_prompt
from ask_ai.ask_ai_for_graph import get_ask_graph_prompt
from ask_ai.ask_ai_for_sql import get_sql_code
from ask_ai.ask_api import ask_py, get_final_prompt, get_ans_code
from ask_ai.input_process import get_chart_type
from data_access.read_db import execute_select, get_all_table_names
from llm_access import call_llm_test
from llm_access.LLM import get_llm
from llm_access.call_llm_test import call_llm
from utils.exe.code_executor import execute_code
from utils.output_parsing import parse_output

from pywebio.input import input, TEXT, actions, textarea
from pywebio.output import put_html, put_text, put_table, put_markdown, put_image, put_code, put_loading
from pywebio import start_server


class AskRequest(BaseModel):
    question: str
    concurrent: int
    retries: int


llm = get_llm()

# test_ask_request = AskRequest(
#     question="统计价格平均房价最高的10个不同区域的房价占比",
#     concurrent=1,
#     retries=3
# )

# print(get_all_table_names())
#
# sql_code = get_sql_code(test_ask_request.question, llm)
#
# ans_pd = execute_select(sql_code)
#
# graph_type = get_chart_type(test_ask_request.question, llm)
# test_ask_request.question = test_ask_request.question + graph_type
#
# result = ask_py(ans_pd, get_ask_echart_file_prompt(test_ask_request),
#                 llm, parse_output.assert_html_file, test_ask_request.retries)
#
# print(result)


def main():
    put_markdown("# DATA COPILOT")

    table_names = get_all_table_names()
    put_text("数据库：")
    put_table([table_names])

    while 1:
        question = input("请输入你的问题：", type=TEXT)
        ask_request = AskRequest(question=question, concurrent=1, retries=3)
        put_text("你的问题："+question)

        # 生成 SQL 代码
        with put_loading():
            sql_code = get_sql_code(ask_request.question, llm)
        # put_text("生成的 SQL 代码：")
        # put_text(sql_code)

        while 1:
            edited_sql = textarea("请编辑 SQL 代码并确认执行：", value=sql_code, rows=10, code=True)
            put_text("执行 SQL 代码：")
            put_code(edited_sql, language="sql")

            # 执行 SQL 查询
            with put_loading():
                ans_pd = execute_select(edited_sql)
            if isinstance(ans_pd, pd.DataFrame):
                put_text("查询结果：")
                if len(ans_pd) > 20:
                    html = f"""
                           <div style="height: 400px; overflow-y: auto;">
                               {ans_pd.to_html(index=False)}
                           </div>
                           """
                    put_html(html)
                else:
                    put_table(ans_pd.to_dict('records'))
                # 让用户选择是否接受结果或重新查询
                user_choice = actions("请选择：", [
                    {'label': '继续', 'value': 'accept', "color": "success"},
                    {'label': '重新编辑 SQL', 'value': 'retry'},
                    {'label': '重新生成 SQL', 'value': 'regen'}
                ])

                if user_choice == 'accept':
                    break  # 用户接受结果，跳出循环
                elif user_choice == 'retry':
                    continue  # 用户选择重新编辑 SQL 代码
                elif user_choice == 'regen':
                    mid_notes = textarea("请输入你的问题（如要修改）：", value=ask_request.question, type=TEXT)
                    with put_loading():
                        sql_code = get_sql_code(ask_request.question + mid_notes, llm)
                    continue
            elif isinstance(ans_pd, SQLAlchemyError):
                put_text(f"查询失败，错误类型：{type(ans_pd).__name__}，错误信息：{str(ans_pd)}")
                put_text("请重新编辑 SQL 代码。")
            else:
                put_text("未知错误，查询失败。")
                put_text("请重新编辑 SQL 代码。")

        # 获取图表类型
        with put_loading():
            graph_type = get_chart_type(ask_request.question, llm)
        edited_graph_type = input("请编辑图表类型（如果需要）：", type=TEXT, value=graph_type)
        if edited_graph_type.strip():
            graph_type = edited_graph_type

        ask_request.question = ask_request.question + graph_type

        pre_prompt = get_ask_echart_block_prompt(ask_request)

        # 生成图表
        # result = ask_py(ans_pd, ask_request.question+pre_prompt,
        #                 llm, parse_output.assert_skip, ask_request.retries)
        # print(result)
        # if result[0] is None:
        #     while 1:
        #         edited_code = textarea("请编辑代码并重新执行：", value=result[4], rows=10, code=True)
        #         put_text(result[4])
        #         try:
        #             result[0] = execute_code(edited_code, ans_pd, parse_output.assert_str)
        #             put_html(result[0])
        #             break
        #         except Exception as e:
        #             put_text(f"代码执行失败，错误信息：{str(e)}")
        # else:
        #     put_html(result[0])

        final_prompt = get_final_prompt(ans_pd, ask_request.question + pre_prompt)
        with put_loading():
            ans_code = get_ans_code(final_prompt, llm)

        while 1:
            edited_code = textarea("请编辑代码：", value=ans_code, rows=10, code=True)
            put_code(ans_code, language="python")
            try:
                result = execute_code(edited_code, ans_pd)
                put_html(result)
            except Exception as e:
                put_text(f"代码执行失败，错误信息：{str(e)}")
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
                mid_notes = textarea("请输入你的问题（如要修改）：", value=ask_request.question, type=TEXT)
                with put_loading():
                    ans_code = get_ans_code(final_prompt + mid_notes, llm)
                continue


if __name__ == '__main__':
    start_server(main, port=8080)
