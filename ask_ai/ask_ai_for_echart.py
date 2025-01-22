

from utils import path_tools


def get_ask_echart_block_prompt(req):
    graph_type = """
        use pyecharts 2.0. the Python function should only return a string of html. do not save it.
        no graph title no set theme! no theme! no theme ! 
        X label should be converted to str instead of int or float !!!
        X label should be converted to str instead of int or float !!!
        """

    example_code = """
        here is an example: 
        ```python
        def draw_graph(dataframe):
            import pandas as pd
            import math
            from pyecharts import #
            # do not set theme!!!
            # generate code to perform operations here

            html_string = chart.render_notebook() # this returns a html string
            # do not use render_embed(), please use render_notebook() !!!
            return html_string
        ```
        """
    return graph_type + example_code


def get_ask_echart_file_prompt(req, tmp_file=False):
    graph_type = """
            use pyecharts 2.0. the Python function should return a string file path in ./tmp_imgs/ only 
            and the graph html generated should be stored in that path. 
            no graph title no set theme! no theme! no theme ! 
            file path must be:
            """

    example_code = """
            here is an example: 
            ```python
            def draw_graph(dataframe):
                import pandas as pd
                import math
                from pyecharts import #
                # generate code to perform operations here
                chart.render(file_path)
                return file_path
            ```
            """
    if not tmp_file:
        return graph_type + path_tools.generate_html_path() + example_code
    else:
        return graph_type + "./tmp_imgs/tmp.html" + example_code



