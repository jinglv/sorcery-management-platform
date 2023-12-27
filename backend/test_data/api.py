import random
import string
import time

from faker import Faker
from ninja import Router

from backend.common import response
from test_data.schema import TestDataType, SearchData
from test_data.utils import generate_data_info, generate_data_list

router = Router(tags=["test"])

fake_ch = Faker(locale='zh_CN')


@router.get("/data/time/{data}")
def time_base_data(request, data: int):
    """
    时间相关数据生成
    """
    result = {}
    # 时间戳 秒
    if data == 1:
        result['time_data'] = int(time.time())
    # 时间戳 毫秒
    elif data == 2:
        result['time_data'] = int(time.time() * 1000)
    # 格式化时间 年-月-日 时:分:秒
    elif data == 3:
        result['time_data'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 格式化时间 年-月-日
    elif data == 4:
        result['time_data'] = time.strftime("%Y-%m-%d", time.localtime())
    else:
        return response(item='')
    return response(item=result)


@router.get("/data/number/{digit}")
def random_number(request, digit: int):
    """
    根据指定长度随即生成数字
    """
    if digit > 0:
        result = {'number': fake_ch.random_number(digit)}
    else:
        result = ''
    return response(item=result)


@router.get("/data/cn/{digit}")
def random_cn(request, digit: int):
    """
    根据指定长度随即生成汉字
    """
    if digit > 0:
        s = fake_ch.sentence(digit, variable_nb_words=False)[0:-1]
        l = int(len(s) / 2)
        result = {'cn': s[0:l]}
    else:
        result = ''
    return response(item=result)


@router.get("/data/letter/{digit}")
def random_letter(request, digit: int):
    """
    根据指定长度随即生成字母
    """
    if digit > 0:
        letters = string.ascii_letters + string.digits
        result = {'letters': ''.join(random.choice(letters) for i in range(digit))}
    else:
        result = ''
    return response(item=result)


@router.post("/data")
def generate_template_data(request, data: TestDataType):
    """
    根据模版生成数据
    """
    return response(item=generate_data_info(data.data_type.split(',')))


@router.post("/data/search")
def generate_search_data_list(request, data: SearchData):
    """
    生成查询条件，数据集合
    """
    return response(item=generate_data_list(data.search_data_key.split(','), data.search_data_value.split(',')))
