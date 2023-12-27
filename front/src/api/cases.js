import request from '@/utils/request'

export function createCaseSuite(data) {
  return request({
    url: '/api/cases/suite/create',
    method: 'post',
    data
  })
}

export function getSuiteList(params, data) {
  return request({
    url: '/api/cases/suites',
    method: 'post',
    params,
    data
  })
}

export function getCaseSuiteDetail(id) {
  return request({
    url: '/api/cases/suite/' + id,
    method: 'get'
  })
}

export function deleteCaseSuite(id) {
  return request({
    url: '/api/cases/suite/' + id,
    method: 'delete'
  })
}

export function updateCaseSuite(id, data) {
  return request({
    url: '/api/cases/suite/' + id,
    method: 'put',
    data
  })
}

export function createTestCase(data) {
  return request({
    url: '/api/cases/create',
    method: 'post',
    data
  })
}

export function getCasesList(params, data) {
  return request({
    url: '/api/cases/list',
    method: 'post',
    params,
    data
  })
}

export function getTestCasesDetail(id) {
  return request({
    url: '/api/cases/detail/' + id,
    method: 'get'
  })
}

export function updateTestCase(id, data) {
  return request({
    url: '/api/cases/update/' + id,
    method: 'put',
    data
  })
}

export function createDemand(data) {
  return request({
    url: '/api/cases/demand/create',
    method: 'post',
    data
  })
}

export function getDemandList(params, data) {
  return request({
    url: '/api/cases/demand/list',
    method: 'post',
    params,
    data
  })
}

export function getDemandDetail(id) {
  return request({
    url: '/api/cases/demand/detail/' + id,
    method: 'get'
  })
}

export function updateDemandDetail(id, data) {
  return request({
    url: '/api/cases/demand/update/' + id,
    method: 'put',
    data
  })
}

export function deleteDemand(id) {
  return request({
    url: '/api/cases/demand/delete/' + id,
    method: 'delete'
  })
}
