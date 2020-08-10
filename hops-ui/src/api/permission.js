import request from '@/utils/request'

export function generateRoutes(params) {
  return request({
    url: '/user/menus',
    method: 'get',
    params
  })
}
