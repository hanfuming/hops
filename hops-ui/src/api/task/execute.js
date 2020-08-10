import request from '@/utils/request'

export function executeCmd(data) {
  return request({
    url: '/task/execute',
    method: 'post',
    data
  })
}

