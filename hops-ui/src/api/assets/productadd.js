import request from '@/utils/request'

export function getProductParent(params) {
  return request({
    url: '/cmdb/product',
    method: 'get',
    params
  })
}

export function ProductAdd(data) {
  return request({
    url: '/cmdb/product',
    method: 'post',
    data
  })
}
