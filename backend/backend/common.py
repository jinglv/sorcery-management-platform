from itertools import chain


class Error:
    """
    预定义错误码与错误信息
    """
    """ 用户相关，定义的错误码与错误信息 """
    USERNAME_IS_NULL = {"10015": "用户名不能为空"}
    USER_OR_PWD_NULL = {"10010": "用户名或密码为空"}
    USER_OR_PWD_ERROR = {"10011": "用户名或密码错误"}
    PWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户名已被注册"}
    USER_NOT_LOGIN = {"10014": "用户未登录"}

    """ 产品相关，定义的错误码与错误信息 """
    PROJECT_NAME_EXIST = {"10021": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"10022": "项目不存在"}
    PROJECT_IS_DELETE = {"10023": "项目已删除"}
    IMAGE_SUFFIX_ERROR = {"10024": "上传图片格式错误"}
    IMAGE_SIZE_ERROR = {"10025": "图片大小不能超过2MB"}
    JSONPATH_ERROR = {"10026": "JsonPath未能匹配到值"}
    HAR_SUFFIX_ERROR = {"10027": "上传HAR文件格式错误"}

    MODULE_NAME_EXIST = {"10031": "项目中已存在模块名称"}
    MODULE_NO_EXIST = {"10032": "项目中模块不存在"}
    MODULE_IS_DELETE = {"10033": "项目模块已删除"}

    API_PARAMS_ERROR = {"10041": "接口传入参数类型错误"}
    API_IS_DELETE = {"10042": "接口信息已删除"}
    CASE_EXTRACT_ERROR = {"10043": "提取器校验失败"}
    CASE_URL_PATH_ERROR = {"10044": "请求地址有误！请选择执行环境！"}
    CASE_SUITE_NAME_EXIST = {"10045": "测试集已存在"}
    CASE_SUITE_IS_NULL = {"10046": "测试用例集不存在"}
    DEMAND_INFO_NAME_EXIST = {"10141": "需求信息已存在"}
    DEMAND_INFO_IS_NULL = {"10142": "需求信息不存在"}
    DEMAND_IS_DELETE = {"10143": "项目已删除"}
    TEST_CASE_IS_NULL = {"10241": "测试用例不存在"}

    BASE_DATA_TYPE_ERROR = {"10051": "基础数据类型不存在"}
    NUMBER_DATA_TYPE_ERROR = {"10052": "传入的数据不能为空或者0"}

    TASK_IS_DELETE = {"10061": "测试任务已删除"}
    CASE_NOT_EXIST = {"10062": "测试用例不存在"}

    YAPI_API_LIST_IS_EMPTY = {"10071": "该分类下的接口列表为空"}
    HAR_FILE_IS_ERROR = {"10072": "Har文件不存在"}

    ENV_IS_NULL = {"10081": "环境信息不存在"}

    YAML_IS_FAIL = {"10091": "yaml文件生成失败"}


def model_to_dict(instance: object) -> dict:
    """
    对象转字典
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    return data


def response(success: bool = True, error=None, item=None) -> dict:
    """
    定义统一返回格式
    """
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    if item is None:
        item = {}
    elif isinstance(item, str):
        item = item
    elif isinstance(item, dict):
        item = item
    elif isinstance(item, list):
        item = item
    elif isinstance(item, object):
        item = model_to_dict(item)
    else:
        item = {}

    resp_data = {
        "success": success,
        "error": {
            "code": error_code,
            "message": error_msg
        },
        "result": item
    }
    return resp_data
