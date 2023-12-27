import request from '@/utils/request'

export function getTestData(data) {
  return request({
    url: '/api/test/data',
    method: 'post',
    data
  })
}

export function getDataSearchList(data) {
  return request({
    url: '/api/test/data/search',
    method: 'post',
    data
  })
}

export function getTimeData(data) {
  return request({
    url: '/api/test/data/time/' + data,
    method: 'get'
  })
}

export function getRandomNumberData(data) {
  return request({
    url: '/api/test/data/number/' + data,
    method: 'get'
  })
}

export function getRandomCnData(data) {
  return request({
    url: '/api/test/data/cn/' + data,
    method: 'get'
  })
}

export function getRandomLetterData(data) {
  return request({
    url: '/api/test/data/letter/' + data,
    method: 'get'
  })
}
