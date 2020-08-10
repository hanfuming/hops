import request from '@/utils/request'

export function getProductList(params) {
  return request({
    url: '/asset/product',
    method: 'get',
    params
  })
}

// 查询详细
export function getProduct(proId) {
  return request({
    url: '/asset/product/' + praseStrEmpty(proId),
    method: 'get'
  })
}

export function productAdd(data) {
  return request({
    url: '/asset/product',
    method: 'post',
    data
  })
}

export function productDel(data) {
  return request({
    url: '/asset/product',
    method: 'delete',
    data
  })
}

export function productUpdate(data) {
  return request({
    url: '/asset/product',
    method: 'put',
    data
  })
}