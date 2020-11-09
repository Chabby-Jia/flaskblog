import json
# 引入 ImmutableMultiDict 做数据类型判断
from werkzeug.datastructures import ImmutableMultiDict
from flask import current_app


def get_form_error_items(form):
    """
    获取表单验证失败的字段名称及错误信息
    :param form: 表单类实例
    :return: 验证失败的字段名称列表和错误信息列表组成的元祖
    """
    form_error_items = form.errors.items()
    fields_name = []
    fields_errors = []
    if form_error_items:
        for field_name, errors in form_error_items:
            fields_name.append(field_name)
            fields_errors += errors
    return fields_name, fields_errors


def check_ajax_request_data(data, target_model_name):
    """ajax 校验函数"""
    # 基本的失败数据格式
    failed_data = {'code': 0, 'msg': ''}

    # 判空
    if not data:
        failed_data['msg'] = '未接收到任何请求数据'
        return json.dumps(failed_data)
    if not (type(data) == dict or type(data) == ImmutableMultiDict):
        failed_data['msg'] = 'AJAX 请求数据格式不正确'
        return json.dumps(failed_data)

    model_name = data.get('modelName')
    data_id = data.get('id')

    # 判断 model_name 空值
    if not model_name:
        failed_data['msg'] = '未指定查询模型'
        return json.dumps(failed_data)

    # 判断 data_id 空值
    if not data_id:
        failed_data['msg'] = '未指定查询 id'
        return json.dumps(failed_data)

    # 判断 data_id 是否为整数
    if not type(data_id) == int:
        if not str(data_id).isdigit():
            failed_data['msg'] = '查询 id 不是数字'
            return json.dumps(failed_data)

    # 将 data_id 转换成整数
    data_id = int(data_id)

    # 获取配置文件中的 MODELS 配置项
    models = current_app.config['MODELS']
    # 判断指定的查询模型是否存在
    model = models.get(model_name)
    if not model:
        failed_data['msg'] = '指定查询模型不存在'
        return json.dumps(failed_data)

    # 判断模型名称是否与目标查询模型名称相符
    if model.__name__ != target_model_name:
        failed_data['msg'] = '指定查询模型与该查询不符'
        return json.dumps(failed_data)

    # 判断数据库查询记录是否存在
    record = model.query.get(data_id)
    if not record:
        failed_data['msg'] = '未查找到任何记录'
        return json.dumps(failed_data)
    return record