<template>
  <div class="app-container">
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="操作人员">
        <el-input v-model="formInline.user" placeholder="请输入用户名称" style="width: 240px;"></el-input>
      </el-form-item>
      <el-form-item label="操作类型">
        <el-select v-model="formInline.opType" placeholder="登录类型">
          <el-option label="导入" value="upload"></el-option>
          <el-option label="导出" value="download"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="操作状态">
        <el-select v-model="formInline.region" placeholder="登录状态">
          <el-option label="成功" value="successful"></el-option>
          <el-option label="失败" value="failed"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="操作时间">
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
      <el-table-column prop="number" label="日志编号"></el-table-column>
      <el-table-column prop="name" label="操作人员"></el-table-column>
      <el-table-column prop="opType" label="操作类型" show-overflow-tooltip></el-table-column>
      <el-table-column prop="opMethod" label="请求方式" show-overflow-tooltip></el-table-column>
      <el-table-column prop="hostip" label="主机" show-overflow-tooltip></el-table-column>
      <el-table-column prop="addr" label="操作地点" show-overflow-tooltip></el-table-column>
      <el-table-column prop="status" label="操作状态" show-overflow-tooltip></el-table-column>
      <el-table-column label="操作时间" show-overflow-tooltip>
        <template slot-scope="scope">{{ scope.row.date }}</template>
      </el-table-column>
      <el-table-column prop="operate" label="操作" show-overflow-tooltip>
        <el-button @click="dialogVisible = true" type="text" size="small" icon="el-icon-view">详细</el-button>
      </el-table-column>
    </el-table>
    <div style="right: 0;position: absolute;margin-top: 20px;">
      <el-pagination background layout="total, sizes, prev, pager, next" :total="100"></el-pagination>
    </div>
    <el-dialog title="操作详细" :visible.sync="dialogVisible" width="50%" :before-close="handleClose">
      <span>请求参数：</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogVisible: false,
      formInline: {
        user: "",
        region: ""
      },
      value1: [new Date(2000, 10, 10, 10, 10), new Date(2000, 10, 11, 10, 10)],
      tableData: [
        {
          number: "1",
          name: "admin",
          opType: "导出",
          opMethod: "GET",
          hostip: "132.23.333.156",
          addr: "上海市",
          status: "操作成功",
          date: "2016-05-03"
        }
      ]
    };
  },
  methods: {
    onSubmit() {
      console.log("submit!");
    },
    methods: {
      handleClose(done) {
        this.$confirm("确认关闭？")
          .then(_ => {
            done();
          })
          .catch(_ => {});
      }
    }
  }
};
</script>