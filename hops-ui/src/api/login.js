import request from '@/utils/request'

// 登录方法
export function login(data) {
  return request({
    url: '/system/login',
    method: 'post',
    data
  })
}

// 获取用户详细信息
export function getInfo() {
  return request({
    url: '/system/getInfo',
    method: 'get'
  })
}

// 退出登录
export function logout() {
  return request({
    url: '/system/logout',
    method: 'post'
  })
}

// 获取路由
export const getRouters = (roles) => {
  return request({
    url: '/system/getRouters',
    method: 'get',
    params: { roles }
  })
}
