<template>
  <div class="app-container">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="作业名称">
        <el-input v-model="searchForm.name" size="small" placeholder="作业名称" />
      </el-form-item>
      <el-form-item label="启动人">
        <el-input v-model="searchForm.user" size="small" placeholder="启动人" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="jobData" style="width: 100%">
      <el-table-column prop="jobId" label="任务ID" />
      <el-table-column prop="jobName" label="任务名称" />
      <el-table-column prop="user" label="启动人" />
      <el-table-column prop="status" label="执行状态">
        <template slot-scope="scope">
          <el-link :type="scope.row.status | statusFilter" :underline="false">{{ scope.row.status }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="startTime" label="开始时间" width="180" />
      <el-table-column prop="endTime" label="结束时间" width="180" />
      <el-table-column prop="totalTime" label="总耗时" />
      <el-table-column label="操作" width="300px;">
        <template slot-scope="scope">
          <el-button type="text" size="small">查看详情</el-button>
          <el-button type="text" size="small">再次执行</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        执行成功: 'success',
        执行失败: 'danger',
        正在执行: 'primary'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      searchForm: {
        name: '',
        user: ''
      },
      jobData: [
        {
          jobId: '111',
          jobName: '版本更新',
          user: 'admin',
          status: '执行成功',
          startTime: '2020-04-10-20:22',
          endTime: '2020-04-10-19:22',
          totalTime: '30s'
        },
        {
          jobId: '113',
          jobName: '版本更新',
          user: 'admin',
          status: '执行失败',
          startTime: '2020-04-10-20:22',
          endTime: '2020-04-10-19:22',
          totalTime: '30s'
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

