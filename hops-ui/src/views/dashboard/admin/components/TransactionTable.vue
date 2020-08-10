<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="近期上线" prop="product" min-width="200"></el-table-column>
    <el-table-column label="负责人" prop="userName" width="195" align="center"></el-table-column>
    <el-table-column label="Status" prop="status" width="100" align="center">
      <template slot-scope="{row}">
        <el-tag :type="row.status | statusFilter">{{ row.status }}</el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
// import { transactionList } from '@/api/remote-search'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        已上线: "success",
        测试中: "warning",
        已下线: "danger"
      };
      return statusMap[status];
    }
    // orderNoFilter(str) {
    //   return str.substring(0, 30);
    // }
  },
  data() {
    return {
      list: [
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已上线"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "测试中"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已下线"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已上线"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已上线"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已上线"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已上线"
        },
        {
          product: "时空之旅",
          userName: "韩福明",
          status: "已上线"
        }
      ]
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      transactionList().then(response => {
        this.list = response.data.items.slice(0, 8);
      });
    }
  }
};
</script>
