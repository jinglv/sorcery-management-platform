import ast
import copy

import pystache
from faker import Faker

fake_ch = Faker(locale='zh_CN')


def list_to_dict(data_list):
    """
    列表转字典
    key：数组下标
    value：数组值
    :param data_list: list
    :return: dict
    """
    dict_data = {}
    for i in range(len(data_list)):
        dict_data[data_list[i]] = data_list[i]
    return dict_data


def list_merge_dict(data_key, data_value):
    """
    将两个list合并为字典
    :param data_key: key_list
    :param data_value: value_list
    :return:
    """
    return dict(zip(data_key, data_value))


def combine(data, l):
    """
    递归的方式，实现根据列表的长度，实现列表枚举所有情况
    """
    result = []
    tmp = [0] * l
    length = len(data)

    def next_num(li=0, ni=0):
        if ni == l:
            result.append(copy.copy(tmp))
            return
        for lj in range(li, length):
            tmp[ni] = data[lj]
            next_num(lj + 1, ni + 1)

    next_num()
    return result


def generate_template(data_list) -> str:
    """
    生成数据模板，将数据值处理为{{}}双花括号括起来的模板
    :param data_list:
    :return:
    """
    result = []
    for i in data_list:
        s = '{{' + str(i) + '}}'
        result.append(s)
    return '"' + str(result) + '"'


def generate_data_list(data_key, data_list) -> list:
    """
    生成数据列表
    """
    data_template = generate_template(data_list)
    result = []
    for i in range(len(data_list)):
        r = combine(data_list, i + 1)
        for j in r:
            d = list_to_dict(j)
            r = ast.literal_eval(pystache.render(data_template, d).strip('"'))
            # 对应数据合并字典，并追加到list中
            result.append(list_merge_dict(data_key, r))
    return result


def generate_data_info(data_key) -> dict:
    """
    根据传入的所需数据，生成对应的数据值
    """
    data_result = []
    for i in data_key:
        # 中文姓名
        if i == "name":
            data_result.append(fake_ch.name())
        # 电话号码
        elif i == "telephone":
            data_result.append(fake_ch.phone_number())
        # 地址
        elif i == "address":
            data_result.append(fake_ch.address())
        # 身份证号
        elif i == "id_card":
            data_result.append(fake_ch.ssn())
        # 国家
        elif i == "country":
            data_result.append(fake_ch.country())
        # 省
        elif i == "province":
            data_result.append(fake_ch.province())
        # 市
        elif i == "city":
            data_result.append(fake_ch.city())
        # 邮编
        elif i == "postcode":
            data_result.append(fake_ch.postcode())
    return list_merge_dict(data_key, data_result)
