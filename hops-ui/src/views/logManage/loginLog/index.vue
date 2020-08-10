<template>
  <div class="app-container">
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="登录地址">
        <el-input v-model="formInline.loginaddr" placeholder="请输入登录ip" style="width: 240px;"></el-input>
      </el-form-item>
      <el-form-item label="用户名称">
        <el-input v-model="formInline.user" placeholder="请输入用户名称" style="width: 240px;"></el-input>
      </el-form-item>
      <el-form-item label="登录状态">
        <el-select v-model="formInline.region" placeholder="登录状态">
          <el-option label="成功" value="successful"></el-option>
          <el-option label="失败" value="failed"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="登录时间">
        <el-date-picker
          v-model="value1"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit" icon="el-icon-search">查询</el-button>
      </el-form-item>
    </el-form>
    <el-row>
      <el-button type="warning" class="el-icon-delete">删除</el-button>
      <el-button type="danger" disabled class="el-icon-delete">清空</el-button>
      <el-button type="primary" class="el-icon-download">导出</el-button>
    </el-row>
    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="number" label="访问编号" width="120"></el-table-column>
      <el-table-column prop="name" label="用户名称" width="120"></el-table-column>
      <el-table-column prop="ipaddr" label="登录地址" show-overflow-tooltip></el-table-column>
      <el-table-column prop="addr" label="登录地点" show-overflow-tooltip></el-table-column>
      <el-table-column prop="browser" label="浏览器" show-overflow-tooltip></el-table-column>
      <el-table-column prop="os" label="操作系统" show-overflow-tooltip></el-table-column>
      <el-table-column prop="loginStatus" label="登录状态" show-overflow-tooltip></el-table-column>
      <el-table-column label="登录时间" show-overflow-tooltip>
        <template slot-scope="scope">{{ scope.row.date }}</template>
      </el-table-column>
    </el-table>
    <div style="right: 0;position: absolute;margin-top: 20px;">
            <el-pagination background layout="total, sizes, prev, pager, next" :total="100"></el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formInline: {
        user: "",
        region: ""
      },
      value1: [new Date(2000, 10, 10, 10, 10), new Date(2000, 10, 11, 10, 10)],
      tableData: [{
          number: '1',
          name: 'admin',
          ipaddr: '132.23.333.156',
          addr: '上海市',
          browser: 'Chrome',
          os:'MacOS',
          loginStatus: '登录成功',
          date: '2016-05-03'
        }]
    };
  },
  methods: {
    onSubmit() {
      console.log("submit!");
    }
  }
};
</script>