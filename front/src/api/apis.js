import request from '@/utils/request'

export function getApisList(id, data) {
  return request({
    url: '/api/apis/module/' + id,
    method: 'get',
    data
  })
}

export function debugApi(data) {
  return request({
    url: '/api/apis/debug',
    method: 'post',
    data
  })
}

export function getApiDetail(id) {
  return request({
    url: '/api/apis/' + id,
    method: 'get'
  })
}

export function assertApi(data) {
  return request({
    url: '/api/apis/assert',
    method: 'post',
    data
  })
}

export function createApi(data) {
  return request({
    url: '/api/apis/create',
    method: 'post',
    data
  })
}

export function updateApi(id, data) {
  return request({
    url: '/api/apis/' + id,
    method: 'put',
    data
  })
}

export function deleteApi(id) {
  return request({
    url: '/api/apis/' + id,
    method: 'delete'
  })
}

export function checkExtract(data) {
  return request({
    url: '/api/apis/extract',
    method: 'post',
    data
  })
}

export function getAllApisList(params, data) {
  return request({
    url: '/api/apis/all/list',
    method: 'post',
    params,
    data
  })
}
