from llm_access.call_llm_test import call_llm

charts = {
    "Bar Chart": "Used for comparing different categories or showing changes over time. ",
    "Pie Chart": "Used for showing the proportion of each part in relation to the whole. ",
    "Line Graph": "Used for illustrating trends over time or other continuous variables. ",
    "Scatter Plot": "Used for showing the relationship or distribution between two variables. "
}

chart_types = ", ".join(charts.keys())
charts_string = str(charts)
# print(chart_types, charts)


def get_chart_type(question, llm):
    graph_type = call_llm(question + "Based on the task described, which is most suitable: " +
                          chart_types + ". "
                                        "You can only choice one of them without any explanation. "
                                        "If you really not sure, return Bar Chart without any explanation, "
                                        "Please output only the chart type names without any explanation. " +
                          charts_string, llm)
    return ", please draw " + graph_type.content



