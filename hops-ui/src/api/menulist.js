import request from '@/utils/request'

export function getMenuList(params) {
  return request({
    url: '/user/menus',
    method: 'get',
    params
  })
}
