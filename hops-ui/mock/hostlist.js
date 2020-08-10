import Mock from 'mockjs'
Mock.Random.natural()
Mock.Random.ip()
Mock.Random.string()
const data = Mock.mock({
  'items|30': [{
    HostID: '@id',
    'deptId|1': ['1', '2', '4'],
    hostName: '@string("lower", 5)',
    'os|1': ['CentOS', 'Ubuntu', 'Windows'],
    'status|1': ['运行中', '异常', '已下线'],
    configuration: '4核8G 500G',
    innerIP: '@ip',
    outerIP: '@ip',
    product: '封神纪元',
    cloud: '腾讯云',
    region: '广州四区',
    createTime: '@datetime'
  }]
})

export default [
  {
    url: '/hostlist\.*',
    type: 'get',
    response: config => {
      const items = data.items
      console.debug(config.query)
      const dpId = config.query.deptId
      const pageNum = config.query.pageNum
      const pageSize = config.query.pageSize
      const innerIP = config.query.innerIP
      if (dpId) {
        if (innerIP) {
          const items = data.items.find(items => items.innerIP === innerIP)
          var resdata = []
          resdata.push(items)
          return {
            code: 20000,
            data: {
              pNum: pageNum,
              pSize: pageSize,
              total: resdata.length,
              items: resdata
            }
          }
        }
        var datas = []
        // const items = data.items.find(items => items.deptId === info)
        data.items.forEach(items => {
          if (items.deptId === dpId) {
            datas.push(items)
          }
        })
        // var resdata = []
        // console.debug(datas)
        // resdata.push(items)
        return {
          code: 20000,
          data: {
            pNum: pageNum,
            pSize: pageSize,
            total: datas.length,
            items: datas
          }
        }
      }

      if (innerIP) {
        var innerIPdata = []
        // const items = data.items.find(items => items.deptId === info)
        data.items.forEach(items => {
          if (items.innerIP === innerIP) {
            innerIPdata.push(items)
          }
        })
        // var resdata = []
        // console.debug(datas)
        // resdata.push(items)
        return {
          code: 20000,
          data: {
            pNum: pageNum,
            pSize: pageSize,
            total: innerIPdata.length,
            items: innerIPdata
          }
        }
      }

      return {
        code: 20000,
        data: {
          pNum: pageNum,
          pSize: pageSize,
          total: items.length,
          items: items
        }
      }
    }
  }
]
