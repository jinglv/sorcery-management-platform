import request from '@/utils/request'

export function harApiInfo(data) {
  return request({
    url: '/api/info/har',
    method: 'post',
    data
  })
}

export function harFileList() {
  return request({
    url: '/api/info/har-file-list',
    method: 'get'
  })
}

export function saveApiInfo(data) {
  return request({
    url: '/api/info/save',
    method: 'post',
    data
  })
}

export function apiInfoList(params, filename) {
  return request({
    url: '/api/info/list/' + filename,
    method: 'get',
    params
  })
}

export function apiInfoDetail(id) {
  return request({
    url: '/api/info/' + id,
    method: 'get'
  })
}

export function getYapiProjectInfo(data) {
  return request({
    url: '/api/info/yapi/project/info',
    method: 'post',
    data
  })
}

export function getYapiCategoryList(data) {
  return request({
    url: '/api/info/yapi/category/list',
    method: 'post',
    data
  })
}

export function getYapiApiList(data) {
  return request({
    url: '/api/info/yapi/api/list',
    method: 'post',
    data
  })
}

export function getYapiApiDetail(data) {
  return request({
    url: '/api/info/yapi/api/detail',
    method: 'post',
    data
  })
}
