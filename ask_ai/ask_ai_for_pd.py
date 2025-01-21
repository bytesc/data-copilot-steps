
def get_ask_pd_prompt(req):
    question = req.question
    example_code = """ 
       the Python function should return a single pandas dataframe only!!! 
       do not draw any graph at this step, even if the question asked. do not save any thing. 
       you should join the tables and select cols based on the questions meaning.
       columns bound may have different columns names.
       here is an example: 
       ```python
       def process_data(dataframes_dict):
           import pandas as pd
           import math
           # generate code to perform operations here
           return result
       ```
       """
    return question + example_code


