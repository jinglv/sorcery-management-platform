import request from '@/utils/request'

export function createEnvs(data) {
  return request({
    url: '/api/env/create',
    method: 'post',
    data
  })
}

export function getEnvsInfo(env_id) {
  return request({
    url: '/api/env/detail/' + env_id,
    method: 'get'
  })
}

export function updateEnvs(env_id, data) {
  return request({
    url: '/api/env/update/' + env_id,
    method: 'put',
    data
  })
}

export function envsListByProject(product_id) {
  return request({
    url: '/api/env/' + product_id + '/list',
    method: 'get'
  })
}

export function envsList(params, data) {
  return request({
    url: '/api/env/list',
    method: 'post',
    params,
    data
  })
}

export function deleteEnvs(id) {
  return request({
    url: '/api/env/' + id,
    method: 'delete'
  })
}
