const data = {
  items: [
    {
      id: 1,
      label: '葫芦兄弟',
      status: '已上线',
      children: [
        {
          id: 4,
          label: '葫芦兄弟',
          status: '已上线'
        },
        {
          id: 9,
          label: '葫芦兄弟小Y',
          status: '已上线'
        }
      ]
    },
    {
      id: 2,
      label: '天生不凡',
      status: '已上线',
      children: [
        {
          id: 5,
          label: '封神纪元',
          status: '已上线'
        },
        {
          id: 6,
          label: '天生不凡海外',
          status: '已上线'
        }
      ]
    },
    {
      id: 3,
      label: '时空之旅',
      status: '已上线'
    }
  ]
}

export default [
  {
    url: '/vue-admin-template/api/productlist',
    type: 'get',
    response: config => {
      const items = data.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  }
]
