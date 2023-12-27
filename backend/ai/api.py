import openai
from ninja import Router

from ai.schema import OpenAIIn
from backend.common import response
from backend.settings import OPENAI_API_KEY, OPENAI_API_BASE

router = Router(tags=["ai"])

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE


@router.post("/chatgpt")
def openai_chatgpt(request, data: OpenAIIn):
    """
    通过调用openai api使用chatgpt
    """
    if data.messages:
        messages = data.messages
        # 有上下文历史
        messages.append({
            'role': 'user',
            'content': data.question
        })
    else:
        # 第一次初始化
        messages = [{
            'role': 'user',
            'content': data.question
        }]
    # 提问信息初始化
    res = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
    result_len = len(res['choices']) - 1
    answer = res['choices'][result_len]['message']['content']
    result_info = {
        'messages': messages,
        'answer': answer
    }
    return response(item=result_info)
