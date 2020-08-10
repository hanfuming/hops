import request from '@/utils/request'

export function adduser(data) {
  return request({
    url: '/user/usermanage',
    method: 'post',
    data
  })
}

export function getUserList(params) {
  return request({
    url: '/user/usermanage',
    method: 'get',
    params
  })
}

export function delUser(data) {
  return request({
    url: '/user/usermanage',
    method: 'delete',
    data
  })
}

export function resetpasswd(data) {
  return request({
    url: '/user/resetpwd',
    method: 'post',
    data
  })
}

export function changUser(data) {
  return request({
    url: '/user/changuser',
    method: 'post',
    data
  })
}

export function changPass(data) {
  return request({
    url: '/user/changpass',
    method: 'post',
    data
  })
}

export function getRoleList(params) {
  return request({
    url: '/user/roles',
    method: 'get',
    params
  })
}
