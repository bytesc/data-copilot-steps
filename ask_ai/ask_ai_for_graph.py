

from utils import path_tools


def get_ask_graph_prompt(req, tmp_file=False):
    question = req.question
    graph_type = """
        use matplotlib. the Python function should return a string file path in ./tmp_imgs/ only 
        and the image generated should be stored in that path. 
        file path must be:
        """
    example_code = """
        here is an example: 
        ```python
        def draw_graph(dataframes_dict):
            import pandas as pd
            import math
            import matplotlib.pyplot as plt
            import matplotlib
            import PIL
            # generate code to perform operations here
            return path
        ```
        """
    if not tmp_file:
        return question + graph_type + path_tools.generate_img_path() + example_code
    else:
        return question + graph_type + "./tmp_imgs/tmp.png" + example_code



