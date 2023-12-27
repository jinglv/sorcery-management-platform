import codecs
import json

from backend.common import response, Error


def read_har_file(har_file):
    """
    读取上传的har文件
    """
    # 判断文件后缀名
    suffix = har_file.split('.')[1]
    if suffix not in "har":
        return response(error=Error.HAR_SUFFIX_ERROR)
    data_har = codecs.open(har_file, mode='r', encoding='utf-8-sig')
    # 读取entries文件
    return json.load(data_har)['log']['entries']


def get_header_or_query(request_header):
    """
    提取header或者query通用方法
    """
    headers = []
    for i in request_header:
        if i['name'] in headers:
            continue
        else:
            header = {
                'name': i['name'],
                'value': i['value']
            }
            headers.append(header)
    return headers


def get_post_data(request_post_data):
    """
    提取postData
    """
    post_data = {
        'mimeType': request_post_data['mimeType'],
        'request_body': json.loads(request_post_data['text'])
    }
    return post_data


def get_response_context(response_data):
    """
    提取响应内容的文本
    """
    response_body = {
        'mimeType': response_data['mimeType'],
        'text': json.loads(response_data['text'])
    }
    return response_body


def api_info(har_file):
    """
    接口信息处理
    """
    entries = read_har_file(har_file)
    # print(json.dumps(entries))
    result = []
    for i in entries:
        # 请求参数信息
        request_info = i['request']
        # 响应参数信息
        response_info = i['response']
        # 请求参数处理
        req_header = request_info['headers']
        request_headers = get_header_or_query(req_header)
        request_params = get_header_or_query(request_info['queryString'])
        request_body = ''
        if 'postData' in request_info:
            req_body = request_info['postData']
            # application/x-www-form-urlencoded
            if req_body['mimeType'] == 'application/x-www-form-urlencoded' or 'multipart/form-data' in req_body[
                'mimeType']:
                params = []
                for i in req_body['params']:
                    param = {
                        'name': i['name'],
                        'value': i['value']
                    }
                    params.append(param)
                # request_body = {
                #     'mimeType': req_body['mimeType'],
                #     'request_params': params
                # }
                request_body = params
            # elif 'multipart/form-data' in req_body['mimeType']:
            #     request_body = req_body
            else:
                # request_body = {
                #     'mimeType': req_body['mimeType'],
                #     'text': json.loads(req_body['text'])
                # }
                request_body = json.loads(req_body['text'])
        # 响应参数处理
        res_header = response_info['headers']
        response_headers = get_header_or_query(res_header)
        response_body = response_info['content']
        if 'text' in response_body:
            response_body = response_info['content']['text']
        result_info = {
            'url': request_info['url'],
            'method': request_info['method'],
            'request_headers': request_headers,
            'request_params': request_params,
            'request_body': request_body,
            'response_headers': response_headers,
            'response_body': response_body
        }
        result.append(result_info)
    return result
