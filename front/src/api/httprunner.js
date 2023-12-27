import request from '@/utils/request'

export function run(data) {
  return request({
    url: '/api/httprunner/code/run',
    method: 'post',
    data
  })
}

export function httpRunnerProjectList(params) {
  return request({
    url: '/api/httprunner/projects',
    method: 'get',
    params
  })
}

export function createHttpRunnerProject(data) {
  return request({
    url: '/api/httprunner/project/create',
    method: 'post',
    data
  })
}

export function updateHttpRunnerProject(httprunner_project_id, data) {
  return request({
    url: '/api/httprunner/project/' + httprunner_project_id,
    method: 'put',
    data
  })
}

export function getHttpRunnerApiList(params, data) {
  return request({
    url: '/api/httprunner/apis/list',
    method: 'post',
    params,
    data
  })
}

export function getHttpRunnerApiIds(projectId) {
  return request({
    url: '/api/httprunner/apis/ids/' + projectId,
    method: 'get'
  })
}

export function createHttpRunnerApi(data) {
  return request({
    url: '/api/httprunner/apis/create',
    method: 'post',
    data
  })
}

export function httpRunnerRunApi(data) {
  return request({
    url: '/api/httprunner/apis/run',
    method: 'post',
    data
  })
}

export function httpRunnerRunResult(params, type) {
  return request({
    url: '/api/httprunner/apis/result/list/' + type,
    method: 'get',
    params
  })
}

export function httpRunnerRenderReportApi(name) {
  return request({
    url: '/api/httprunner/report/render/' + name,
    method: 'get'
  })
}

export function httpRunnerApiDetail(id) {
  return request({
    url: '/api/httprunner/apis/detail/' + id,
    method: 'get'
  })
}

export function updateHttpRunnerApi(id, data) {
  return request({
    url: '/api/httprunner/apis/update/' + id,
    method: 'put',
    data
  })
}

export function deleteHttpRunnerApi(id) {
  return request({
    url: '/api/httprunner/apis/delete/' + id,
    method: 'delete'
  })
}

export function getHttpRunnerCasesList(params, data) {
  return request({
    url: '/api/httprunner/cases/list',
    method: 'post',
    params,
    data
  })
}

export function createHttpRunnerTestCase(data) {
  return request({
    url: '/api/httprunner/cases/create',
    method: 'post',
    data
  })
}

export function httpRunnerRunCases(data) {
  return request({
    url: '/api/httprunner/cases/run',
    method: 'post',
    data
  })
}

export function httpRunnerTestCaseDetail(id) {
  return request({
    url: '/api/httprunner/cases/detail/' + id,
    method: 'get'
  })
}

export function updateHttpRunnerTestCase(id, data) {
  return request({
    url: '/api/httprunner/cases/update/' + id,
    method: 'put',
    data
  })
}

export function deleteHttpRunnerTestCase(id) {
  return request({
    url: '/api/httprunner/cases/delete/' + id,
    method: 'delete'
  })
}

export function getHttpRunnerTestCaseIds(projectId) {
  return request({
    url: '/api/httprunner/cases/ids/' + projectId,
    method: 'get'
  })
}

export function getHttpRunnerSuiteList(params, data) {
  return request({
    url: '/api/httprunner/suite/list',
    method: 'post',
    params,
    data
  })
}

export function httpRunnerRunSuite(data) {
  return request({
    url: '/api/httprunner/suite/run',
    method: 'post',
    data
  })
}

export function createHttpRunnerSuite(data) {
  return request({
    url: '/api/httprunner/suite/create',
    method: 'post',
    data
  })
}

export function httpRunnerSuiteDetail(id) {
  return request({
    url: '/api/httprunner/suite/detail/' + id,
    method: 'get'
  })
}

export function updateHttpRunnerSuite(id, data) {
  return request({
    url: '/api/httprunner/suite/update/' + id,
    method: 'put',
    data
  })
}

export function deleteHttpRunnerSuite(id) {
  return request({
    url: '/api/httprunner/suite/delete/' + id,
    method: 'delete'
  })
}
