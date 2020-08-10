import request from '@/utils/request'

export function getHostList(params) {
  return request({
    url: '/asset/host',
    method: 'get',
    params
  })
}

export function changeHostName(data) {
  return request({
    url: '/hostlist',
    method: 'post',
    data
  })
}
