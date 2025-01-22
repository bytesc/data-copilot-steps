import pandas as pd
from pywebio import start_server
from pywebio.output import put_html

data = {
    'year': ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"," 2023", "2024", "2025"],
    'average_resale_price': [
        434709.5578, 438838.9643, 443888.5204, 441282.0636, 432137.9128,
        452279.3848, 511381.2389, 549714.3304, 571803.9960, 612479.2338, 625161.8071
    ]
}

# 创建DataFrame
df = pd.DataFrame(data)

# def create_line_chart(data):
#         import pandas as pd
#         from pyecharts.charts import Line
#         from pyecharts import options as opts
#         line = Line()
#         line.add_xaxis(data['year'].tolist())
#         line.add_yaxis("", data['average_resale_price'].tolist())
#         line.set_global_opts()
#         html_string = line.render_notebook()
#         return html_string


def create_line_chart(data):
    import pandas as pd
    from pyecharts.charts import Line
    from pyecharts import options as opts
    line = Line()
    line.add_xaxis(data['year'].tolist())
    line.add_yaxis("平均转售价格", data['average_resale_price'].tolist())
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="平均转售价格趋势"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="价格")
    )
    html_string = line.render_notebook()
    return html_string


def main():
    # 生成折线图
    chart_html = create_line_chart(df)

    # 将图表嵌入到 PyWebIO 页面中
    put_html(chart_html)


if __name__ == '__main__':
    # 启动 Web 应用
    start_server(main, port=8080)
