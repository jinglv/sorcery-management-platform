import json


def data_parser(api_info) -> dict:
    """
    解析接口详情，处理需要的接口格式
    接口名称(name)
    接口路径(path)
    请求方式(method)
    请求头(headers)
    请求主体类型(req_type json/params)
    请求主体(req_body)
    响应主体示例展示(res_body)
    :param api_info: 请求返回的接口详情
    :return:
    """
    name = api_info['title']
    path = api_info['path']
    method = api_info['method']
    # 处理header头信息
    headers = []
    if api_info['req_headers']:
        for h in api_info['req_headers']:
            header_info = {
                "name": h['name'],
                "value": h['value']
            }
            headers.append(header_info)
    # 处理请求类型
    if 'req_body_type' in api_info:
        if api_info['req_body_type'] == 'json':
            req_type = 'json'
        else:
            req_type = 'other'
    else:
        req_type = 'params'
    # 处理请求主体
    if 'req_body_other' in api_info:
        req_dict = json.loads(api_info['req_body_other'])
        req_body = body_parser(req_dict)
    else:
        req_body = ''
    # 处理相应主体示例
    if 'res_body' in api_info:
        res_dict = json.loads(api_info['res_body'])
        res_body = body_parser(res_dict)
    else:
        res_body = ''
    parser_body = {
        'name': name,
        'path': path,
        'method': method,
        'headers': headers,
        'req_type': req_type,
        'req_body': req_body,
        'res_body': res_body
    }
    return parser_body


def body_parser(data):
    result = []
    if data["type"] == "object" and "properties" in data:
        for key, value in data["properties"].items():
            if 'description' in value.keys():
                item = {"name": key, "type": value["type"], "description": value["description"]}
            else:
                item = {"name": key, "type": value["type"]}
            if "items" in value and value["type"] == "array":
                item["type"] = "array"
                if 'properties' in value["items"]:
                    item["field"] = body_parser(value["items"])
                else:
                    item["field"] = value["items"]
            if key in data.get("required", []):
                item["required"] = 1
            else:
                item["required"] = 0
            result.append(item)
    if data["type"] == "array" and "items" in data:
        body_parser(data['items'])
    return result
