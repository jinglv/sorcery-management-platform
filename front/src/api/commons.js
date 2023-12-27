import request from '@/utils/request'

export function uploadFile(data) {
  return request({
    url: '/api/commons/file',
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 20000,
    data
  })
}

export function editorUploadFile(data) {
  return request({
    url: '/api/commons/editor/file',
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 20000,
    data
  })
}

export function updateImage(data) {
  return request({
    url: '/api/commons/upload',
    method: 'post',
    timeout: 20000,
    data
  })
}

export function getStatisticsList() {
  return request({
    url: '/api/commons/statistics/hr',
    method: 'get'
  })
}

export function getStatisticsTotal() {
  return request({
    url: '/api/commons/statistics/hr/total',
    method: 'get'
  })
}
