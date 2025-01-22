import logging

from utils.output_parsing import parse_output


def execute_code(code, data, assert_func=parse_output.assert_skip):
    """
    执行生成的代码并返回结果。

    :param code: 生成的Python代码
    :param data: 输入数据
    :param assert_func: 断言函数，用于验证结果
    :return: 执行结果，如果执行成功且通过断言则返回结果，否则返回None
    """
    try:
        local_namespace = {'data': data, 'result': None}
        exec(code, globals(), local_namespace)
        result = local_namespace['draw_graph'](data)
        assert_result = assert_func(result)
        if assert_result:
            raise Exception(assert_result)
        return result
    except Exception as e:
        logging.error(f"An error occurred while executing the code: {type(e).__name__}: {str(e)}")
        raise
