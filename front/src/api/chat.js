import request from '@/utils/request'

export function chatgpt(data) {
  return request({
    url: '/api/ai/chatgpt',
    method: 'post',
    data
  })
}
