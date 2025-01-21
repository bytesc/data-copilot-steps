from pydantic import BaseModel

from ask_ai.ask_ai_for_echart import ask_echart_file, get_ask_echart_file_prompt
from ask_ai.ask_ai_for_sql import get_sql_code
from ask_ai.ask_api import ask_py
from ask_ai.input_process import get_chart_type
from data_access.read_db import execute_select
from llm_access.LLM import get_llm
from llm_access.call_llm_test import call_llm
from utils.output_parsing import parse_output


class AskRequest(BaseModel):
    question: str
    concurrent: int
    retries: int


llm = get_llm()

test_ask_request = AskRequest(
    question="how many flats are brought each year",
    concurrent=1,
    retries=3
)

sql_code = get_sql_code(test_ask_request.question, llm)

ans_pd = execute_select(sql_code)

graph_type = get_chart_type(test_ask_request.question, llm)
test_ask_request.question = test_ask_request.question + graph_type

result = ask_py(ans_pd, get_ask_echart_file_prompt(test_ask_request),
                llm, parse_output.assert_html_file, test_ask_request.retries)

print(result)

