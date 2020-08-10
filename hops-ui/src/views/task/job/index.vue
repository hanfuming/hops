<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="作业名称">
        <el-input v-model="searchForm.name" size="small" placeholder="作业名称" />
      </el-form-item>
      <el-form-item label="创建人">
        <el-input v-model="searchForm.user" size="small" placeholder="创建人" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="jobData" style="width: 100%">
      <el-table-column prop="jobName" label="作业名称" />
      <el-table-column prop="user" label="创建人" />
      <el-table-column prop="changeUser" label="最后修改人" />
      <el-table-column prop="createdate" label="创建时间" width="180" />
      <el-table-column prop="changeDate" label="最后修改时间" />
      <el-table-column label="操作" width="300px;">
        <template slot-scope="scope">
          <el-button type="text" size="small"><router-link to="/taskManager/jobdetails/jobdetail">立即执行</router-link></el-button>
          <el-button type="text" size="small">定时启动</el-button>
          <el-divider direction="vertical" />
          <el-button type="text" size="small">编辑</el-button>
          <el-button type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchForm: {
        name: '',
        user: ''
      },
      jobData: [{
        jobName: '版本更新',
        user: 'admin',
        changeUser: 'user1',
        createdate: '2020-04-10',
        changeDate: '2020-04-10'
      }
      ],
      listLoading: true
    }
  },
  // created() {
  //   this.productData()
  // },
  methods: {
    // productData() {
    //   this.listLoading = true
    //   getProductList().then(response => {
    //     this.deptOptions = response.data.items
    //     this.listLoading = false
    //   })
    // },
    onSubmit() {
      console.log('submit!')
    }
    // handleClick(row) {
    //   console.log(row)
    // }
  }
}
</script>

