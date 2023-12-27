import jsonpath
import requests


def z_request(yapi_base_url, api_path, param):
    """
    封装requests方法 统一调用yapi接口
    :param yapi_base_url: yapi url
    :param api_path: yapi 接口path地址
    :param param: 接口参数
    :return: 响应数据
    """
    response_data = ''
    i = 0
    while i < 3:
        try:
            response_data = requests.get(url=yapi_base_url + api_path, params=param, timeout=(60, 7))
            s = requests.session()
            s.keep_alive = False
            break
        except requests.exceptions.ConnectionError:
            i = i + 1
    return response_data


def get_response_data(response_data, json_path):
    """
    获取响应体中的值
    :param response_data: 接口响应数据
    :param json_path: JSON Path
    :return: 返回获取值
    """
    return jsonpath.jsonpath(response_data, json_path)
