from ninja import Schema


class TestDataType(Schema):
    """
    测试数据类型入参
    """
    data_type: str


class SearchData(Schema):
    """
    查询条件传入
    """
    search_data_key: str
    search_data_value: str
