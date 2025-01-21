# from pywebio import start_server
# from pywebio.output import put_html
# from pyecharts.charts import Bar
# from pyecharts import options as opts
#
#
# def create_bar_chart():
#     # 创建一个柱状图
#     bar = Bar()
#     bar.add_xaxis(["A", "B", "C", "D", "E"])
#     bar.add_yaxis("系列1", [10, 20, 30, 40, 50])
#     bar.add_yaxis("系列2", [20, 30, 40, 50, 60])
#
#     # 设置图表标题和其他选项
#     bar.set_global_opts(
#         title_opts=opts.TitleOpts(title="示例柱状图"),
#         xaxis_opts=opts.AxisOpts(name="X轴"),
#         yaxis_opts=opts.AxisOpts(name="Y轴"),
#     )
#
#     # 将图表渲染为 HTML
#     return bar.render_notebook()
#
#
# def main():
#     # 生成图表
#     chart_html = create_bar_chart()
#
#     # 将图表嵌入到 PyWebIO 页面中
#     put_html(chart_html)
#
#
# if __name__ == '__main__':
#     # 启动 Web 应用
#     start_server(main, port=8080)

from pywebio import start_server
from pywebio.output import put_html
from pyecharts.charts import Line
from pyecharts import options as opts

def create_line_chart():
    # 创建一个折线图
    line = Line()

    # X 轴数据
    x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    # Y 轴数据
    y_data1 = [120, 132, 101, 134, 90, 230, 210]  # 系列1
    y_data2 = [220, 182, 191, 234, 290, 330, 310]  # 系列2

    # 添加数据到折线图
    line.add_xaxis(x_data)
    line.add_yaxis("系列1", y_data1)
    line.add_yaxis("系列2", y_data2)

    # 设置全局配置
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="每周数据折线图"),  # 标题
        xaxis_opts=opts.AxisOpts(name="星期"),  # X 轴名称
        yaxis_opts=opts.AxisOpts(name="数值"),  # Y 轴名称
        tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 提示框配置
    )

    # 将图表渲染为 HTML
    return line.render_notebook()

def main():
    # 生成折线图
    chart_html = create_line_chart()

    # 将图表嵌入到 PyWebIO 页面中
    put_html(chart_html)

if __name__ == '__main__':
    # 启动 Web 应用
    start_server(main, port=8080)
