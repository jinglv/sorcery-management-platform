import request from '@/utils/request'

export function projectList(params, data) {
  return request({
    url: '/api/projects/list',
    method: 'post',
    params,
    data
  })
}

export function createProject(data) {
  return request({
    url: '/api/projects/create',
    method: 'post',
    data
  })
}

export function getProject(id) {
  return request({
    url: '/api/projects/' + id,
    method: 'get'
  })
}

export function updateProject(id, data) {
  return request({
    url: '/api/projects/' + id,
    method: 'put',
    data
  })
}

export function deleteProject(id) {
  return request({
    url: '/api/projects/' + id,
    method: 'delete'
  })
}

// export function updateImage(data) {
//   return request({
//     url: '/api/commons/upload',
//     method: 'post',
//     timeout: 20000,
//     data
//   })
// }
