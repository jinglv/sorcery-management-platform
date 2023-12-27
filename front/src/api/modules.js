import request from '@/utils/request'

export function getModuleTree(id) {
  return request({
    url: '/api/modules/tree?project_id=' + id,
    method: 'get'
  })
}

export function createModule(data) {
  return request({
    url: '/api/modules/create',
    method: 'post',
    data
  })
}

export function deleteModule(id) {
  return request({
    url: '/api/modules/' + id,
    method: 'delete'
  })
}

export function getModuleCase(id) {
  return request({
    url: '/api/cases/module/' + id,
    method: 'get'
  })
}
