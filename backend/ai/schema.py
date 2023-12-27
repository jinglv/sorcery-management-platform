from ninja import Schema


class OpenAIIn(Schema):
    """
    问题请求入参
    """
    question: str
    messages: list = None
